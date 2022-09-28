import json
import queue
try:
    from GUI import GUI
    from camelot_error import CamelotError
    from camelot_error_manager import CamelotErrorManager
    from platform_IO_communication import PlatformIOCommunication
    from camelot_action import CamelotAction
    from camelot_world_state import CamelotWorldState
    from utilities import parse_json, replace_all, get_action_list, str2bool
    from camelot_input_multiplexer import CamelotInputMultiplexer
    from encounters_controller import EncountersController
    from conversation_controller import ConversationController
    import shared_variables
except (ModuleNotFoundError, ImportError):
    from .GUI import GUI
    from .camelot_error import CamelotError
    from .camelot_error_manager import CamelotErrorManager
    from .platform_IO_communication import PlatformIOCommunication
    from .camelot_action import CamelotAction
    from .camelot_world_state import CamelotWorldState
    from .utilities import parse_json, replace_all, get_action_list, str2bool
    from .camelot_input_multiplexer import CamelotInputMultiplexer
    from .encounters_controller import EncountersController
    from .conversation_controller import ConversationController
    from . import shared_variables
from ev_pddl.action import Action
from ev_pddl.PDDL import PDDL_Parser
from ev_pddl.domain import Domain
from ev_pddl.world_state import WorldState
import logging
import multiprocessing
import debugpy
import logging
import time
import jsonpickle
import copy
import re

class GameController:

    def __init__(self, GUI = True):
        self._domain_path, self._problem_path = shared_variables.get_domain_and_problem_path()
        shared_variables.action_list = get_action_list()
        self._parser = PDDL_Parser()
        self._domain = self._parser.parse_domain(domain_filename = self._domain_path)
        self._problem = self._parser.parse_problem(problem_filename = self._problem_path)
        self._camelot_action = CamelotAction()
        self._encounter_controller = EncountersController()
        self._conversation_controller = ConversationController()
        self._player = ''
        self.input_dict = {}
        self.current_state = None
        self.conversation_active = False
        self._menu_showing = False
        self.queueIn_GUI = multiprocessing.Queue()
        self.queueOut_GUI = multiprocessing.Queue()
        self._platform_communication = PlatformIOCommunication()
        self.active_GUI = GUI
        self.error_list = []
        self._received_action_from_platform = None
        
    
    def start_platform_communication(self):
        """
        A method that is used to start the platform communication. It follows the communication controller steps.
        """
        self._platform_communication.start()
        logging.info("Platform communication started")
        logging.info("Platform communication starting handshake phase 1")
        message = self._platform_communication.communication_protocol_phase_messages['PHASE_2']['message_3'] + "Camelot"
        logging.info("GameController: Sending message: " + message)
        result = self._platform_communication.send_message(message, inizialization=True)
        logging.info("GameController: received message: " + str(result))
        if result['text'] == self._platform_communication.communication_protocol_phase_messages['PHASE_2']['message_4']:
            logging.info("Platform communication handshake phase 1 finished")
            return True
        else:
            raise Exception("Platform communication failed")
    
    def _platform_communication_phase_3_4(self, domain: Domain, wolrd_state: WorldState):
        """
        A method that is used to handle phase 3 and 4 of the communication protocol.
        """
        logging.info("Platform communication starting handshake phase 3")
        logging.info("Platform communication waiting for phase 3 to start")
        while self._platform_communication.get_handshake_phase() != "PHASE_3":
            time.sleep(0.1)
        logging.info("Platform communication phase 3 started")
        debugpy.breakpoint()
        message_text = {
            "text" : self._platform_communication.communication_protocol_phase_messages['PHASE_3']['message_6'],
            "domain" : domain.to_PDDL(),
            "problem" : wolrd_state.to_PDDL(),
            "additional_data" : self._encounter_controller.get_encounters_message()
        } 
        logging.info("GameController: Sending message: " + str(message_text))
        result = self._platform_communication.send_message(message_text, inizialization=True)
        logging.info("GameController: received message: " + str(result))
        if result['text'] == self._platform_communication.communication_protocol_phase_messages['PHASE_4']['message_9']:
            self._platform_communication.send_message_link = result['add_message_url'].replace('/', '')
            logging.info("Send message link: /" + self._platform_communication.send_message_link)
            self._platform_communication.receive_message_link = result['get_message_url'].replace('/', '')
            logging.info("Receive message link: /" + self._platform_communication.receive_message_link)
            logging.info("Platform communication setting urls finished")
            logging.info("Platform communication handshake phase 4 finished")
            return True
        else:
            raise Exception("Platform communication failed")

    def _initialize(self):
        """
        This method is used to initialize the components of the game controller that we don-t want to initialize in the init method, 
        but after when the first stage of the communication handshake finished.
        """
        self.camelot_input_multiplex = CamelotInputMultiplexer()
        self.error_manager = CamelotErrorManager()
        
    
    def start_game(self, game_loop = True):
        """A method that is used to start the game loop
        
        Parameters
        ----------
        game_loop : default: True
            Variable used for debugging purposes.
        """
        self._initialize()
        initial_state = CamelotWorldState(self._domain, self._problem, wait_for_actions= game_loop)
        initial_state.create_camelot_env_from_problem()
        initial_state.check_domain_actions_available_to_use()

        self._platform_communication_phase_3_4(initial_state.domain, initial_state.world_state)

        self._player = initial_state.find_player(self._problem)
        self._create_ingame_actions(game_loop)
        self._camelot_action.action("ShowMenu", wait=game_loop)
        self.current_state = initial_state
        self.GUI_process = multiprocessing.Process(target=GUI, args=(self.queueIn_GUI, self.queueOut_GUI))
        if self.active_GUI:
            self.GUI_process.start()
        while game_loop:
            received = self.camelot_input_multiplex.get_input_message()

            if received == 'input Selected Start': 
                self._camelot_action.action("HideMenu")
                self._camelot_action.action('EnableInput')
                self._main_game_controller(game_loop)
    
    def _create_ingame_actions(self, game_loop = True):
        """A method that is used to create the actions that are used in the game.
        It parses the pddl_predicates_to_camelot.json and integrates the content in game.
        
        """
        json_p = parse_json("pddl_predicates_to_camelot")
        for item in self._problem.initial_state:
            if item.predicate.name in json_p:
                if item.predicate.name == "adjacent":
                    self._adjacent_predicate_handling(item, json_p, game_loop)
                elif item.predicate.name == "stored":
                    self._stored_predicate_handling(item, json_p)
                else:
                    sub_dict = {
                        '$param1$' : item.entities[0].name,
                        '$param2$' : self._player.name
                    }
                    # execute declaration part
                    for istr in json_p[item.predicate.name]['declaration']:
                        action_name, action_parameters, wait = self._get_camelot_action_parameters_from_json(istr, sub_dict)
                        self._camelot_action.action(action_name, action_parameters, wait=wait)
                    # prepare input dict
                    input_key = replace_all(json_p[item.predicate.name]['input']["message"], sub_dict)
                    self.input_dict[input_key] = []
                    # popolate input dict with istructions to use when input is called
                    for istr in json_p[item.predicate.name]['response']:
                        action_name, action_parameters, wait = self._get_camelot_action_parameters_from_json(istr, sub_dict)
                        action_dict = {
                            'action_name' : action_name,
                            'action_parameters' : action_parameters,
                            'wait' : wait
                        }
                        self.input_dict[input_key].append(action_dict)

    def _adjacent_predicate_handling(self, item, json_p, game_loop = True):
        """A method that is used to manage the places declared on the domain

        It declares the input function that is used from Camelot to enable an action to happen. In this case the action is the exit action. 
        It also creates the responce to the action, so when camelot triggers the input command the systems knows the responce.
        
        Parameters
        ----------
        game_loop : boolen, default - True
            boolean used for debugging porpuses.
        """
        
        sub_dict = {
            '$param1$' : item.entities[0].name,
            '$param2$' : self._player.name,
            '$param3$' : item.entities[1].name,
        }
        # execute declaration part
        for istr in json_p['adjacent']['declaration']:
            action_name, action_parameters, wait = self._get_camelot_action_parameters_from_json(istr, sub_dict)
            self._camelot_action.action(action_name, action_parameters, wait=wait)

        # prepare input dict
        loc, entry = item.entities[0].name.split('.')
        if 'end' in entry.lower():
            input_key = replace_all(json_p['adjacent']['input']['end'], sub_dict)
            self.input_dict[input_key] = []
        else:
            input_key = replace_all(json_p['adjacent']['input']['door'], sub_dict)
            self.input_dict[input_key] = []
        
        # popolate input dict with istructions to use when input is called
        for istr in json_p['adjacent']['response']:
            action_name, action_parameters, wait = self._get_camelot_action_parameters_from_json(istr, sub_dict)
            action_dict = {
                'action_name' : action_name,
                'action_parameters' : action_parameters,
                'wait' : wait
            }
            self.input_dict[input_key].append(action_dict)
    
    def _stored_predicate_handling(self, item, json_p):
        """A method that is used to popolate the input_dict with the actions that are used to manage the stored predicates.
        
        """
        sub_dict = {
            '$param1$' : item.entities[0].name,
            '$param2$' : self._player.name,
            '$param3$' : item.entities[1].name,
        }

        input_key = replace_all(json_p[item.predicate.name]['input']["message"], sub_dict)
        self.input_dict[input_key] = []

        for istr in json_p[item.predicate.name]['response']:
            action_name, action_parameters, wait = self._get_camelot_action_parameters_from_json(istr, sub_dict)
            action_dict = {
                'action_name' : action_name,
                'action_parameters' : action_parameters,
                'wait' : wait
            }
            self.input_dict[input_key].append(action_dict)
                
    def _get_camelot_action_parameters_from_json(self, istr : dict, sub_dict : dict):
        """
        Utility method used to create the parameters of the camelot action using the json file.
        """
        action_name = istr.get('action_name')
        action_parameters = []
        for item in istr.get('action_args'):
            if item in sub_dict.keys():
                action_parameters.append(sub_dict[item])
            elif any(k in item for k in sub_dict.keys()):
                action_parameters.append(replace_all(item, sub_dict))
            elif item == "TRUE":
                action_parameters.append(True)
            elif item == "FALSE":
                action_parameters.append(False)
            else:
                action_parameters.append(item)
        wait = str2bool(istr.get('wait'))
        return action_name, action_parameters, wait

    def _main_game_controller(self, game_loop = True):
        """A method that is used as main game controller
        
        Parameters
        ----------
        game_loop : boolen, default - True
            boolean used for debugging porpuses.
        """
        exit = game_loop
        if self._player != '':
            self._camelot_action.action("SetCameraFocus",[self._player.name])
        self._camelot_action.success_messages = queue.Queue()
        self._camelot_action.debug = True
        while exit:

            self._input_handler()

            self._success_message_handler()

            self._location_handler()

            self._incoming_messages_handler()

            self._check_error_messages()
        
        # self.queue_GUI.close()
        # self.queue_GUI.join_thread()
        # self.GUI_process.join()


    def _success_message_handler(self):
        """A method that is used to handle the success message and update the world state
        """
        try:
            received = self._camelot_action.success_messages.get_nowait()
            logging.info("GameController: Success message received: " + received)
            self._apply_camelot_message(received)
        except queue.Empty:
            return False
        return True       
    
    def _input_handler(self) -> bool:
        """
        A method that is used to handle the input from Camelot.

        Parameters
        ----------
        None

        Returns
        -------
        bool -> True if received message from input queue and responded to it; False if not.
        """
        try:
            received = str(self.camelot_input_multiplex.get_input_message(no_wait=True))
            logging.info("GameController: got input message \"%s\"" %( received ))

            if received in self.input_dict.keys():
                for item in self.input_dict[received]:
                    action_name = item['action_name']
                    action_parameters = item['action_parameters']
                    wait = item['wait']
                    self._camelot_action.action(action_name, action_parameters, wait=wait)
            elif received == "input Key Pause":
                if not self._menu_showing:
                    self._camelot_action.action("ShowMenu", [], True)
                    self._camelot_action.action("SetTitle", ["Pause Menu"], True)
                    self._menu_showing = True
            elif received in ("input Selected Resume", "input Close Menu"):
                self._camelot_action.action("HideMenu", [], True)
                if not self.conversation_active:
                    self._camelot_action.action("EnableInput", [], True)
                self._menu_showing = False
            elif received.startswith("input Selected"):
                selection = received.removeprefix("input Selected ")
                if selection.isdigit():
                    self._conversation_controller.continue_conversation_with_choice(int(selection))
                elif selection == 'next':
                    self._conversation_controller.continue_conversation()
                elif selection == 'end':
                    self._conversation_controller.end_conversation()
        except queue.Empty:
            return False
        return True
    
    def _location_handler(self):
        """
        A method that is used to handle the location inputs from Camelot.

        Parameters
        ----------
        None
        """
        try:
            #TODO: evolve to handle multiple location inputs
            received = self.camelot_input_multiplex.get_location_message(no_wait=True)
            logging.info("GameController: got location message \"%s\"" %( received ))
            if received.startswith(shared_variables.location_message_prefix[2:]):
                #self.queue_GUI.put(received)
                self._apply_camelot_message(received)
        except queue.Empty:
            return False
        except Exception as inst:
            logging.exception("GameController: Exception in location handler: %s" %( inst ))
            return False
        return True

    def _incoming_messages_handler(self):
        """
        A method that is used to handle the incoming messages that can come from the GUI or the evaluation platform.

        Parameters
        ----------
        None
        """
        try:
            received = self.queueOut_GUI.get_nowait()
            logging.debug("GameController: got external message \"%s\"" %( received ))

            if "CI" in received:
                # handle Camelot instruction
                message = received["CI"]
                self._camelot_action.send_camelot_instruction(message)
            elif "PA" in received:
                # handle PDDL action
                message = received["PA"]
                self._incoming_action_handler(message)
        except queue.Empty:
            pass
        
        action = self._platform_communication.receive_message()
        if action is not None:
            action_text = action[0]['text']
            logging.debug("GameController: got external message from platform: \"%s\"" %( action_text ))
            self._incoming_action_handler(action_text)
    
    def _check_error_messages(self):
        """
        This method is used to check if there are any error messages.
        """
        error_message = self.camelot_input_multiplex.get_error_message()
        if error_message is not None:
            error = CamelotError(error_message)
            self.error_list.append(error)

    
    def _incoming_action_handler(self, message : str):
        """
        This method is used to handle the message that represents an action. 
        It first creates a PDDL action, and then generates the camelot instructions that need to be sent to camelot for execution.

        Parameters
        ----------
        message: str
            The message that represents the action.
        """
        # move-between-location(luca, Blacksmith, AlchemyShop, Blacksmith.Door, AlchemyShop.Door)
        # start_conversation(luca, initial_narrative)
        message = message.replace(" ", "")
        if message.startswith("start_"):
            message_parts = re.split(r"\(|\)|,", message)
            if message.startswith("start_conversation"):
                character = message_parts[1]
                conversation = message_parts[2]
                if self._conversation_controller.check_conversation_exists(conversation):
                    self.conversation_active = True
                    self._conversation_controller.start_camelot_conversation(conversation_name=conversation, player_name=self._player.name, npc_name=character)
            elif message.startswith("start_encounter"):
                encounter_name = message_parts[1]
                self._encounter_controller.start_encounter(encounter_name)
        else:
            action = self.current_state.create_action_from_incoming_message(message)
            self._received_action_from_platform = copy.deepcopy(action)
            camelot_action_parameters = self._camelot_action.generate_camelot_action_parameters_from_action(action)
            success = self._camelot_action.actions(camelot_action_parameters)
            if success:
                changed_relations = self.current_state.apply_action(action)
                if action.name.startswith("instantiate_object"):
                    json_p = parse_json("pddl_predicates_to_camelot")
                    stored = [item[1] for item in changed_relations if item[0] == "new" and item[1].predicate.name == "stored"]
                    self._stored_predicate_handling(stored[0], json_p)
                self.queueIn_GUI.put(self.current_state.world_state)
                self._platform_communication.send_message(self._format_changed_relations_for_external_message(changed_relations))
    
    def _apply_camelot_message(self, message):
        """
        This method is used to apply a message that is received from Camelot to the current state.

        Parameters
        ----------
        message: str
            The message that will be applied.
        """
        changed_relations = self.current_state.apply_camelot_message(message, self._received_action_from_platform)
        if len(changed_relations) > 0:
            self.queueIn_GUI.put(self.current_state.world_state)
            self._platform_communication.send_message(self._format_changed_relations_for_external_message(changed_relations))

    def _format_changed_relations_for_external_message(self, changed_relations):
        """
        This method is used to format a message for the external communication.

        Parameters
        ----------
        message: list
            The list of relations that changed.
        """
        relation_list = []
        for item in changed_relations:
            if type(item) == list:
                for subitem in item:
                    i = (subitem[0], subitem[1].to_PDDL())
                    relation_list.append(i)
            elif type(item) == tuple and len(item) == 2:
                i = (item[0], item[1].to_PDDL())
                relation_list.append(i)
            else:
                logging.debug("GameController(_format_changed_relations_for_external_message): Invalid relation: %s" %( item ))
        json_message = jsonpickle.encode(relation_list)
        return json_message
import queue
try:
    from GUI import GUI
    from camelot_error import CamelotError
    from camelot_error_manager import CamelotErrorManager
    from platform_IO_communication import PlatformIOCommunication
    from camelot_action import CamelotAction
    from camelot_world_state import CamelotWorldState
    from utilities import parse_json, replace_all, get_action_list
    from camelot_input_multiplexer import CamelotInputMultiplexer
    import shared_variables
except (ModuleNotFoundError, ImportError):
    from .GUI import GUI
    from .camelot_error import CamelotError
    from .camelot_error_manager import CamelotErrorManager
    from .platform_IO_communication import PlatformIOCommunication
    from .camelot_action import CamelotAction
    from .camelot_world_state import CamelotWorldState
    from .utilities import parse_json, replace_all, get_action_list
    from .camelot_input_multiplexer import CamelotInputMultiplexer
    from . import shared_variables
from ev_pddl.action import Action
from ev_pddl.PDDL import PDDL_Parser
from ev_pddl.domain import Domain
from ev_pddl.world_state import WorldState
import logging
import multiprocessing
import debugpy
import logging
import re

class GameController:

    def __init__(self, GUI = True):
        self._domain_path, self._problem_path = shared_variables.get_domain_and_problem_path()
        shared_variables.action_list = get_action_list()
        self._parser = PDDL_Parser()
        self._domain = self._parser.parse_domain(self._domain_path)
        self._problem = self._parser.parse_problem(self._problem_path)
        self._camelot_action = CamelotAction()
        self._player = ''
        self.input_dict = {}
        self.camelot_input_multiplex = CamelotInputMultiplexer()
        self.current_state = None
        self.queueIn_GUI = multiprocessing.Queue()
        self.queueOut_GUI = multiprocessing.Queue()
        self._platform_communication = PlatformIOCommunication()
        self.error_manager = CamelotErrorManager()
        self.active_GUI = GUI
    
    def start_platform_communication(self):
        """A method that is used to start the platform communication. It follows the communication controller steps.
        """
        result = self._platform_communication.send_message(self._platform_communication.communication_protocol_phase_messages['PHASE_2']['message_3'] + "Camelot", inizialization=True)
        if result == self._platform_communication.communication_protocol_phase_messages['PHASE_2']['message_4']:
            return True
        else:
            raise Exception("Platform communication failed")
    
    def _platform_communication_phase_3_4(self, domain: Domain, wolrd_state: WorldState):
        """A method that is used to handle phase 3 and 4 of the communication protocol.
        """
        message_text = {
            "text" : self._platform_communication.communication_protocol_phase_messages['PHASE_3']['message_6'],
            "domain" : domain.to_PDDL(),
            "world_state" : wolrd_state.to_PDDL()
        } 
        result = self._platform_communication.send_message(message_text, inizialization=True)
        if result['text'] == self._platform_communication.communication_protocol_phase_messages['PHASE_4']['message_9']:
            self._platform_communication.send_message_link = result['add_message_url']
            self._platform_communication.receive_message_link = result['get_message_url']
            return True
        else:
            raise Exception("Platform communication failed")
        
    
    def start_game(self, game_loop = True):
        """A method that is used to start the game loop
        
        Parameters
        ----------
        game_loop : default: True
            Variable used for debugging purposes.
        """
        initial_state = CamelotWorldState(self._domain, self._problem, wait_for_actions= game_loop)
        initial_state.create_camelot_env_from_problem()

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
                    self._location_management(item, json_p, game_loop)
                    continue
                # debugpy.breakpoint()
                sub_dict = {
                    '$param1$' : item.entities[0].name,
                    '$param2$' : self._player.name,
                    '$wait$' : str(game_loop)
                }
                for istr in json_p[item.predicate.name]['declaration']:
                    istr_with_param = replace_all(istr, sub_dict)
                    exec(istr_with_param)
                input_key = replace_all(json_p[item.predicate.name]['input']["message"], sub_dict)
                self.input_dict[input_key] = ""
                for istr in json_p[item.predicate.name]['response']:
                    self.input_dict[input_key] += replace_all(istr, sub_dict) + '\n'

    def _location_management(self, item, json_p, game_loop = True):
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
            '$wait$' : str(game_loop)
        }
        for istr in json_p['adjacent']['declaration']:
            istr_with_param = replace_all(istr, sub_dict)
            exec(istr_with_param)
        loc, entry = item.entities[0].name.split('.')
        if 'end' in entry.lower():
            input_key = replace_all(json_p['adjacent']['input']['end'], sub_dict)
            self.input_dict[input_key] = ""
        else:
            input_key = replace_all(json_p['adjacent']['input']['door'], sub_dict)
            self.input_dict[input_key] = ""
            
        for istr in json_p['adjacent']['response']:
            self.input_dict[input_key] += replace_all(istr, sub_dict) + '\n'
                

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
            received = self.camelot_input_multiplex.get_input_message(no_wait=True)
            logging.info("GameController: got input message \"%s\"" %( received ))

            if received in self.input_dict.keys():
                exec(self.input_dict[received])
            elif received == "input Key Pause":
                pass
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
            received = self.camelot_input_multiplex.get_location_message(no_wait=True)
            logging.info("GameController: got location message \"%s\"" %( received ))
            if received.startswith(shared_variables.location_message_prefix[2:]):
                #self.queue_GUI.put(received)
                self._apply_camelot_message(received)
        except queue.Empty:
            return False
        except Exception as inst:
            debugpy.breakpoint()
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
        except queue.Empty:
            return
        
        if "CI" in received:
            # handle Camelot instruction
            message = received["CI"]
            self._camelot_action.send_camelot_instruction(message)
        elif "PA" in received:
            # handle PDDL action
            message = received["PA"]
            self._incoming_action_handler(message)
    
    def _check_error_messages(self):
        """
        This method is used to check if there are any error messages.
        """
        self.camelot_input_multiplex.get_error_message()
    
    def _incoming_action_handler(self, message):
        """
        This method is used to handle the message that represents an action. 
        It first creates a PDDL action, and then generates the camelot instructions that need to be sent to camelot for execution.

        Parameters
        ----------
        message: str
            The message that represents the action.
        """
        # move-between-location(luca, Blacksmith, AlchemyShop, Blacksmith.Door, AlchemyShop.Door)
        action = self.current_state.create_action_from_incoming_message(message)
        camelot_action_parameters = self._camelot_action.generate_camelot_action_parameters_from_action(action)
        success = self._camelot_action.actions(camelot_action_parameters)
        if success:
            debugpy.breakpoint()
            changed_relations = self.current_state.apply_action(action)
            self.queueIn_GUI.put(self.current_state.world_state)
    
    def _apply_camelot_message(self, message):
        """
        This method is used to apply a message that is received from Camelot to the current state.

        Parameters
        ----------
        message: str
            The message that will be applied.
        """
        changed_relations = self.current_state.apply_camelot_message(message)
        if len(changed_relations) > 0:
            self.queueIn_GUI.put(self.current_state.world_state)
        
    
            
from os import pathconf_names
import queue
from GUI import GUI
from pddl.action import Action
from camelot_action import CamelotAction
from camelot_world_state import CamelotWorldState
from pddl.PDDL import PDDL_Parser
import logging
from utilities import parse_json, replace_all
from camelot_input_multiplexer import CamelotInputMultiplexer
import shared_variables
import multiprocessing
import debugpy
import logging
from pathlib import Path
from datetime import datetime
import re

class GameController:

    def __init__(self):
        logname = "logPython"+datetime.now().strftime("%d%m%Y%H%M%S")+".log"
        Path("logs/python/").mkdir(parents=True, exist_ok=True)
        logging.basicConfig(filename='logs/python/'+logname, filemode='w', format='%(levelname)s:%(message)s', level=logging.DEBUG)
        self._domain_path, self._problem_path = shared_variables.get_domain_and_problem_path()
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
        
    
    def start_game(self, game_loop = True):
        """A method that is used to start the game loop
        
        Parameters
        ----------
        game_loop : default: True
            Variable used for debugging purposes.
        """
        initial_state = CamelotWorldState(self._domain, self._problem, wait_for_actions= game_loop)
        initial_state.create_camelot_env_from_problem()

        self._player = initial_state.find_player(self._problem)
        self._create_ingame_actions(game_loop)
        self._camelot_action.action("ShowMenu", wait=game_loop)
        self.current_state = initial_state
        self.GUI_process = multiprocessing.Process(target=GUI, args=(self.queueIn_GUI, self.queueOut_GUI))
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
        
        # for item in self._problem.objects:
        #     if "chest" in item.name.lower():
        #         self._camelot_action.action('EnableIcon', ['OpenFurniture', 'chest', item.name, 'Open ' + item.name, True], game_loop)
        #         self.input_dict["input OpenFurniture "+item.name] = ""
        #         self.input_dict["input OpenFurniture "+item.name] += "self._camelot_action.action('OpenFurniture', ['"+self._player.name+"', '"+ item.name +"'])\n"
        #         self.input_dict["input OpenFurniture "+item.name] += "self._camelot_action.action('DisableIcon', ['OpenFurniture', '"+self._player.name+"'], "+ str(game_loop) + "))\n"
        #         self.input_dict["input CloseFurniture "+item.name] = ""
        #         self.input_dict["input CloseFurniture "+item.name] += "self._camelot_action.action('CloseFurniture', ['"+self._player.name+"', '"+ item.name +"'])\n"


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
        
        # self.queue_GUI.close()
        # self.queue_GUI.join_thread()
        # self.GUI_process.join()


    def _success_message_handler(self):
        """A method that is used to handle the success message and update the world state
        """
        try:
            received = self._camelot_action.success_messages.get_nowait()
            logging.info("GameController: Success message received: " + received)
            self.current_state.apply_camelot_message(received)
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
                changed_relations = self.current_state.apply_camelot_message(received)
                if len(changed_relations) > 0:
                    self.queueIn_GUI.put(self.current_state.world_state)
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
            # action = Action.from_PDDL(message)
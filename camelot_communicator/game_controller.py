from pddl.action import Action
from camelot_action import CamelotAction
from camelot_world_state import CamelotWorldState
from pddl.PDDL import PDDL_Parser
import logging
from utilities import parse_json, replace_all
import random

class GameController:

    def __init__(self):
        self._domain_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\camelot_domain.pddl"
        self._problem_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\example_problem.pddl"
        self._parser = PDDL_Parser()
        self._domain = self._parser.parse_domain(self._domain_path)
        self._problem = self._parser.parse_problem(self._problem_path)
        self._camelot_action = CamelotAction()
        self._player = ''
        self.input_dict = {}
        
    
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
        self._location_management(game_loop)
        self._camelot_action.action("ShowMenu", wait=game_loop)
        for item in self._domain.actions:
            a = None
            while a == None:
                d = item.get_dict_parameters()
                # for i in d.keys():
                #     entity = self._problem.find_objects_with_type(self._domain.find_type(d[i].name))
                #     d[i] = random.choice(entity)
                d['?who'] = initial_state.world_state.find_entity_ignore_case("bob")
                d['?from'] = initial_state.world_state.find_entity_ignore_case("AlchemyShop")
                d['?to'] = initial_state.world_state.find_entity_ignore_case("Bridge")
                d['?entryfrom'] = initial_state.world_state.find_entity_ignore_case("AlchemyShop.Door")
                d['?entryto'] = initial_state.world_state.find_entity_ignore_case("Bridge.SouthEnd")
                try:
                    a = Action(item, d, initial_state.world_state.get_dict_predicates())
                    initial_state.world_state.apply_action(a)
                except ValueError:
                    continue
        while game_loop:
            received = input()

            if received == 'input Selected Start': 
                self._camelot_action.action("HideMenu")
                self._camelot_action.action('EnableInput')
                self._main_game_controller(game_loop)
    

    def _location_management(self, game_loop = True):
        """A method that is used to manage the places declared on the domain

        It declares the input function that is used from Camelot to enable an action to happen. In this case the action is the exit action. 
        It also creates the responce to the action, so when camelot triggers the input command the systems knows the responce.
        
        Parameters
        ----------
        game_loop : boolen, default - True
            boolean used for debugging porpuses.
        """
        json_p = parse_json("pddl_actions_to_camelot")
        for item in self._problem.initial_state:
            if item.predicate.name == self._domain.find_predicate('adjacent').name:
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
        while exit:

            received = input()
            
            if received in self.input_dict.keys():
                exec(self.input_dict[received])

from camelot_action import CamelotAction
from world_state import WorldState
from pddl.PDDL import PDDL_Parser

class GameController:

    def __init__(self):
        self._domain_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\camelot_domain.pddl"
        self._problem_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\example_problem.pddl"
        self._parser = PDDL_Parser()
        self._domain_parsed = self._parser.parse_domain(self._domain_path)
        self._problem_parsed = self._parser.parse_problem(self._problem_path)
        self._camelot_action = CamelotAction()
        self._player = ''
        
    
    def start_game(self, game_loop = True):
        initial_state = WorldState(self._domain_parsed, self._problem_parsed, wait_for_actions= game_loop)
        initial_state.create_camelot_env_from_problem()
        self._player = initial_state.find_player(self._problem_parsed)
        while game_loop:
            received = input()

            if received == 'input Selected Start': 
                self._camelot_action.action("HideMenu")
                self._camelot_action.action('EnableInput')
                self._main_game_controller(game_loop)
                

    def _main_game_controller(self, game_loop = True):
        exit = game_loop
        if self._player != '':
            self._camelot_action.action("SetCameraFocus",[self._player.name])
        while exit:

            received = input()

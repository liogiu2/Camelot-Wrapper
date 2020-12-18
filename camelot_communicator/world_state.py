from camelot_action import CamelotAction
from utilities import parse_json
from pddl.domain import Domain
import random



class WorldState:

    def __init__(self, domain, problem, wait_for_actions = False):
        self.__supported_types = ['location', 'character', 'item']
        self.__supported_predicates = ['at','stored']
        if type(domain) != Domain:
            raise Exception('Domain must be type Domain')
        self.domain = domain
        self._camelot_action = CamelotAction()
        self._wait_for_actions = wait_for_actions
        self.problem = problem

    def create_camelot_env_from_problem(self):
        #Create the locations listed in the problem
        self._create_locations_from_problem(self.problem)
        #Create the items listed in the problem
        self._create_items_from_problem(self.problem)
        #Create character listed in the problem
        self._create_characters_from_problem(self.problem)

        for item in self.problem.initial_state:
            # exclude at for forniture because camelot doesn't need to know where is a furniture
            if item.entities[0].type.name == 'furniture' and item.predicate.name == 'at':
                continue
            self._create_camelot_action_from_predicate(item)
        self._camelot_action.action("ShowMenu", wait=self._wait_for_actions)

    def _create_camelot_action_from_predicate(self, predicate):
        if predicate.predicate.name in self.__supported_predicates:
            action = self._find_in_json('Actionlist', predicate.predicate.name, 'PDDLProblem')
            if action is None:
                raise Exception('Action "%s" not found in camelot list of actions'%(predicate.predicate.name))
            list_entity = [i.name for i in predicate.entities]
            self._camelot_action.action(action['name'], list_entity, self._wait_for_actions)


    def _create_characters_from_problem(self, problem):
        type_char = self.domain.find_type(self.__supported_types[1])
        list_char = problem.find_objects_with_type(type_char)
        while list_char:
            char = list_char.pop(0)
            self._random_character(char.name)

    
    def _random_character(self, name):
        json_parsed = parse_json('characterlist')
        list_body = [d['name'] for d in json_parsed['body_type']]
        r_int = random.randint(0, len(list_body)-1)
        body = list_body[r_int]
        self._camelot_action.action('CreateCharacter', [name, body], self._wait_for_actions)
        outfit = ''
        while True:
            r_int_outfit = random.randint(0, len(json_parsed['outfit'])-1)
            outfit = json_parsed['outfit'][r_int_outfit]
            if outfit['Compatibility'] != 'all':
                if body in outfit['Compatibility']:
                    break
            else:break
        self._camelot_action.action('SetClothing', [name, outfit['name']], self._wait_for_actions)



    def _create_locations_from_problem(self, problem):
        type_location = self.domain.find_type(self.__supported_types[0])
        list_locations = problem.find_objects_with_type(type_location)
        while list_locations:
            location = list_locations.pop(0)
            loc = self._find_in_json('places', location.name, 'name')
            if loc is None:
                raise Exception('location not found in camelot')
            self._camelot_action.action('CreatePlace', [location.name, loc['name']], self._wait_for_actions)
    
    def _create_items_from_problem(self, problem):
        type_item = self.domain.find_type(self.__supported_types[2])
        list_item = problem.find_objects_with_type(type_item)
        while list_item:
            item = list_item.pop(0)
            json_parsed = parse_json('items')
            itm = ''
            for i in json_parsed['items']:
                if item.name.lower() == i.lower():
                    itm = i
                    break
            if itm == '':
                raise Exception('item not found in camelot')
            self._camelot_action.action('CreateItem', [item.name, itm], self._wait_for_actions)

    
    def _find_in_json(self, json, what, where):
        json_parsed = parse_json(json)
        for item in json_parsed:
            if '|' in item[where].lower():
                possible = item[where].lower().split('|')
                for i in possible:
                    if i == what.lower():
                        return item
            else:
                if item[where].lower() == what.lower():
                    return item
        return None


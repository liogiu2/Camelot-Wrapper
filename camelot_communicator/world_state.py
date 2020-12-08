from camelot_action import CamelotAction
from utilities import parse_json
from pddl.domain import Domain
import random



class WorldState:

    def __init__(self, domain):
        self.__supported_types = ['location', 'character', 'item']
        if type(domain) != Domain:
            raise Exception('Domain must be type Domain')
        self.domain = domain
        self._camelot_action = CamelotAction()
        self._wait_for_actions = False

    def create_wordstate_from_problem(self, problem):
        #Create the locations listed in the problem
        self._create_locations_from_problem(problem)
        #Create the items listed in the problem
        self._create_items_from_problem(problem)
        #Create character listed in the problem
        self._create_characters_from_problem(problem)

    def _create_characters_from_problem(self, problem):
        type_char = self.domain.find_type(self.__supported_types[1])
        list_char = problem.find_objects_with_type(type_char)
        while list_char:
            char = list_char.pop(0)
            self._random_character(char.name)

    
    def _random_character(self, name):
        json_parsed = parse_json('characterlist')
        list_body = [d['name'] for d in json_parsed['body_type']]
        r_int = random.randint(0, len(list_body))
        body = list_body[r_int]
        self._camelot_action.action('CreateCharacter', [name, body], self._wait_for_actions)
        outfit = ''
        while True:
            r_int_outfit = random.randint(0, len(json_parsed['outfit']))
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
            loc = self._find_in_json('places', location.name)
            if loc is None:
                raise Exception('location not found in camelot')
            self._camelot_action.action('CreatePlace', [loc['name'], loc['name']], self._wait_for_actions)
    
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
            self._camelot_action.action('CreateItem', [itm, itm], self._wait_for_actions)

    
    def _find_in_json(self, json, what):
        json_parsed = parse_json(json)
        for item in json_parsed:
            if item['name'].lower() == what.lower():
                return item
        return None


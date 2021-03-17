from pddl.problem import Problem
from pddl.relation_value import RelationValue
from pddl.relation import Relation
from pddl.entity import Entity
from camelot_action import CamelotAction
from utilities import parse_json
from pddl.domain import Domain
from pddl.world_state import WorldState
import random
import logging



class CamelotWorldState:
    """
    A Class used to represent a WordState
    
    Attributes
    ----------
    domain : Domain
        An object type Domain that is the Domain that will be used in this WordState

    problem : Problem
        An object type Problem that is the Problem that will be used in this WordState

    wait_for_actions : Boolean, optional
        A boolean flag that is set to False for Debugging porpuses. If True the actions will wait that Camelot responds before continuing the execution

    __supported_types : list, private
        All the domain types currently supported

    __supported_predicates: list, private
        All the domain predicates currently supported

    _camelot_action: CamelotAction
        Object used to send Actions to Camelot

    Methods
    ----------
    create_camelot_env_from_problem
        Created the Camelot environment from the problem object related to the WordState
    """

    def __init__(self, domain, problem, wait_for_actions = False):
        if type(domain) != Domain:
            raise Exception('Domain must be type Domain')
        self.domain = domain
        self.__supported_types = {
            'position': self.domain.find_type('position'), 
            'location': self.domain.find_type('location'),
            'entrypoint': self.domain.find_type('entrypoint'),
            'character': self.domain.find_type('character'), 
            'item': self.domain.find_type('item'), 
            'player': self.domain.find_type('player'), 
            'furniture': self.domain.find_type('furniture'),
        }
        self.__supported_predicates = {
            'at': self.domain.find_predicate('at'),
            'in': self.domain.find_predicate('in'),
            'stored': self.domain.find_predicate('stored'), 
            'can_open': self.domain.find_predicate('can_open'), 
            'is_open': self.domain.find_predicate('is_open'), 
            'has_surface': self.domain.find_predicate('has_surface'),
            'adjacent': self.domain.find_predicate('adjacent'),
        }
        self._camelot_action = CamelotAction()
        self._wait_for_actions = wait_for_actions
        self.problem = problem
        self.world_state = self._create_world_state()
        #logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
        
    def _create_world_state(self) -> WorldState:
        """A method that is used to create the WorldState from the initial state of the problem
        
        """
        world = WorldState(self.domain)
        for item in self.problem.objects:
            world.add_entity(item)
        for item in self.problem.initial_state:
            world.add_relation(item)
        return world


    def create_camelot_env_from_problem(self):
        """A method that is used to create the camelot environmen from the problem linked to the WorldState class
        
        Parameters
        ----------
        None
            
        """
        #Create the locations listed in the problem
        self._create_locations_from_problem(self.problem)
        #Create the items listed in the problem
        self._create_items_from_problem(self.problem)
        #Create character listed in the problem
        self._create_characters_from_problem(self.problem)
        #Integrate WordState with Camelot places infos
        self._integrate_wordstate_with_camelot_places(self.problem)

        for item in self.problem.initial_state:
            # exclude at for forniture because camelot doesn't need to know where is a furniture
            if item.entities[0].type.name == 'furniture' and item.predicate.name == 'at':
                continue
            self._create_camelot_action_from_relation(item)


    def _create_camelot_action_from_relation(self, relation):
        """A method that is used to create camelot actions from a relation.

        It searches in the Json file "Actionlist" within the key "PDDLProblem" the name of the predicate. 
        If it finds it, then it means that with that predicate we want to apply that camelot action. 
        
        Parameters
        ----------
        relation : Relation
            relation to convert to camelot action
        """
        if relation.predicate.name in self.__supported_predicates.keys():
            action = self._find_in_json('Actionlist', relation.predicate.name, 'PDDLProblem')
            if action is None:
                logging.info("%s skipped because it doesn't corrispond to a Camelot action"%str(relation))
            else:
                list_entity = [i.name for i in relation.entities]
                self._camelot_action.action(action['name'], list_entity, self._wait_for_actions)


    def _create_characters_from_problem(self, problem):
        list_char = problem.find_objects_with_type(self.__supported_types['character'])
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
        list_locations = problem.find_objects_with_type(self.__supported_types['location'])
        while list_locations:
            location = list_locations.pop(0)
            room = location.name
            loc = self._find_in_json('places', room, 'name')
            if loc is None:
                raise Exception('location not found in camelot')
            self._camelot_action.action('CreatePlace', [room, loc['name']], self._wait_for_actions)
    
    def _create_items_from_problem(self, problem):
        list_item = problem.find_objects_with_type(self.__supported_types['item'])
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
    
    def find_player(self, problem):
        list_char = problem.find_objects_with_type(self.__supported_types['player'])
        if len(list_char) > 1:
            raise Exception('More then one player defined in the problem.')
        return list_char[0]

    def _integrate_wordstate_with_camelot_places(self, problem: Problem):
        """A method that is used to integrate the wordstate with all components of Camelot places
        
        Parameters
        ----------
            none
            
        """
        list_loc = problem.find_objects_with_type(self.__supported_types['location'])
        for location in list_loc:
            item = self._find_in_json('places', location.name, 'name')
            if item is None:
                raise Exception('Cannot find location %s in places.json'%(location.name))
            for room_component in item['room_components']:
                #Create new Relation and new Objects taken from the json and add them to the problem
                obj = Entity(location.name +'.'+ room_component['name'], self.__supported_types['furniture'], problem)
                try:
                    problem.add_object(obj)
                    logging.debug("Object %s added to the problem"%str(obj))     
                except AttributeError:
                    logging.info("Object %s already exists, so we skip it."%str(obj))        
                #add relation with predicate at
                rel = Relation(self.__supported_predicates['at'], [obj, location], RelationValue.TRUE, self.domain, problem)
                try:
                    problem.add_relation_to_initial_state(rel)
                    logging.debug("Relation %s added to the problem"%str(rel))  
                except AttributeError:
                    logging.info("Relation %s already exists, so we skip it."%str(rel))
                #Parameter to set: ['Open', 'Close', 'Surface', 'Furniture', 'Seat', 'EntryPoint']
                for attribute in room_component['attribute']:
                    if attribute == '':
                        continue
                    elif attribute == 'Open':
                        rel = Relation(self.__supported_predicates['can_open'], [obj], RelationValue.TRUE, self.domain, problem)
                        try:
                            problem.add_relation_to_initial_state(rel)
                            logging.debug("Relation %s added to the problem"%str(rel))  
                        except AttributeError:
                            logging.info("Relation %s already exists, so we skip it."%str(rel))
                    elif attribute == 'Close':
                        rel = Relation(self.__supported_predicates['is_open'], [obj], RelationValue.FALSE, self.domain, problem)
                        try:
                            problem.add_relation_to_initial_state(rel)
                            logging.debug("Relation %s added to the problem"%str(rel)) 
                        except AttributeError:
                            logging.info("Relation %s already exists, so we skip it."%str(rel))
                    elif attribute == 'Surface':
                        rel = Relation(self.__supported_predicates['has_surface'], [obj], RelationValue.TRUE, self.domain, problem)
                        try:
                            problem.add_relation_to_initial_state(rel)
                            logging.debug("Relation %s added to the problem"%str(rel)) 
                        except AttributeError:
                            logging.info("Relation %s already exists, so we skip it."%str(rel))
                    elif attribute == 'Furniture':
                        pass
                    elif attribute == 'Seat':
                        pass
                    elif attribute == 'EntryPoint':
                        pass





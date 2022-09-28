from ev_pddl.action import Action
from ev_pddl.problem import Problem
from ev_pddl.predicate import Predicate
from ev_pddl.relation_value import RelationValue
from ev_pddl.relation import Relation
from ev_pddl.entity import Entity
try:
    from camelot_action import CamelotAction
    from utilities import parse_json
    import shared_variables
except (ModuleNotFoundError, ImportError):
    from .camelot_action import CamelotAction
    from .utilities import parse_json    
    from . import shared_variables
from ev_pddl.domain import Domain
from ev_pddl.world_state import WorldState
import random
import logging
import debugpy
import copy
import re
import random


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
    
    world_state : WorldState
        The PDDL representation of the world state

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

    def __init__(self, domain, problem, wait_for_actions=False):
        if type(domain) != Domain:
            raise Exception('Domain must be type Domain')
        self.domain = domain

        shared_variables.supported_types['position'] = self.domain.find_type('position')
        shared_variables.supported_types['location'] = self.domain.find_type('location')
        shared_variables.supported_types['entrypoint'] = self.domain.find_type('entrypoint')
        shared_variables.supported_types['character'] = self.domain.find_type('character')
        shared_variables.supported_types['item'] = self.domain.find_type('item')
        shared_variables.supported_types['player'] = self.domain.find_type('player')
        shared_variables.supported_types['furniture'] = self.domain.find_type('furniture')

        shared_variables.supported_predicates['at'] = self.domain.find_predicate('at')
        shared_variables.supported_predicates['in'] = self.domain.find_predicate('in')
        shared_variables.supported_predicates['stored'] = self.domain.find_predicate('stored')
        shared_variables.supported_predicates['can_open'] = self.domain.find_predicate('can_open')
        shared_variables.supported_predicates['can_close'] = self.domain.find_predicate('can_close')
        shared_variables.supported_predicates['is_open'] = self.domain.find_predicate('is_open')
        shared_variables.supported_predicates['has_surface'] = self.domain.find_predicate('has_surface')
        shared_variables.supported_predicates['adjacent'] = self.domain.find_predicate('adjacent')

        self._camelot_action = CamelotAction()
        self._wait_for_actions = wait_for_actions
        self.problem = problem
        self.current_room = ""
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
    
    def check_domain_actions_available_to_use(self):
        """A method that is used to check if all the actions available in the domain can be used.
        It checks the JSON file pddl_actions_to_camelot.json and if the action is not available it will be deactivated from the domain.

        Parameters
        ----------
        None

        """
        json_actions = parse_json('pddl_actions_to_camelot')
        for action in self.domain.actions:
            if action.name not in json_actions.keys() and not action.special_action:
                action.available = False

    def create_camelot_env_from_problem(self):
        """A method that is used to create the camelot environmen from the problem linked to the WorldState class

        Parameters
        ----------
        None

        """
        # Create the locations listed in the problem
        self._create_locations_from_problem(self.problem)
        # Create the items listed in the problem
        self._create_items_from_problem(self.problem)
        # Create character listed in the problem
        self._create_characters_from_problem(self.problem)
        # Integrate WordState with Camelot places infos
        self._integrate_wordstate_with_camelot_places(self.problem)

        for item in self.problem.initial_state:
            # exclude at for forniture because camelot doesn't need to know where is a furniture
            if item.entities[0].type.name == 'furniture' and item.predicate.name == 'at':
                continue
            self._create_camelot_action_from_relation(item)
        
        self.world_state = self._create_world_state()

    def _create_camelot_action_from_relation(self, relation):
        """A method that is used to create camelot actions from a relation.

        It searches in the Json file "Actionlist" within the key "PDDLProblem" the name of the predicate. 
        If it finds it, then it means that with that predicate we want to apply that camelot action. 

        Parameters
        ----------
        relation : Relation
            relation to convert to camelot action
        """
        if relation.predicate.name in shared_variables.supported_predicates.keys():
            action = self._find_in_json(
                'Actionlist', relation.predicate.name, 'PDDLProblem')
            if action is None:
                logging.info(
                    "%s skipped because it doesn't corrispond to a Camelot action" % str(relation))
            else:
                list_entity = [i.name for i in relation.entities]
                self._camelot_action.action(
                    action['name'], list_entity, self._wait_for_actions)

    def _create_characters_from_problem(self, problem):
        list_char = problem.find_objects_with_type(
            shared_variables.supported_types['character'])
        while list_char:
            char = list_char.pop(0)
            self._random_character(char.name)

    def _random_character(self, name):
        json_parsed = parse_json('characterlist')
        list_body = [d['name'] for d in json_parsed['body_type']]
        r_int = random.randint(0, len(list_body)-1)
        body = list_body[r_int]
        self._camelot_action.action(
            'CreateCharacter', [name, body], self._wait_for_actions)
        outfit = ''
        while True:
            r_int_outfit = random.randint(0, len(json_parsed['outfit'])-1)
            outfit = json_parsed['outfit'][r_int_outfit]
            if outfit['Compatibility'] != 'all':
                if body in outfit['Compatibility']:
                    break
            else:
                break
        self._camelot_action.action(
            'SetClothing', [name, outfit['name']], self._wait_for_actions)

    def _create_locations_from_problem(self, problem):
        list_locations = problem.find_objects_with_type(
            shared_variables.supported_types['location'])
        while list_locations:
            location = list_locations.pop(0)
            room = location.name
            loc = self._find_in_json('places', room, 'name')
            if loc is None:
                raise Exception('location not found in camelot')
            self._camelot_action.action(
                'CreatePlace', [room, loc['name']], self._wait_for_actions)

    def _create_items_from_problem(self, problem):
        list_item = problem.find_objects_with_type(
            shared_variables.supported_types['item'])
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
        list_char = problem.find_objects_with_type(
            shared_variables.supported_types['player'])
        if len(list_char) > 1:
            raise Exception('More then one player defined in the problem.')
        return list_char[0]

    def find_character_with_name(self, name) -> Entity:
        """
        Method that is used to find a character with a given name in the WordState entities.

        Parameters
        ----------
            name : str
        """
        for char in self.problem.find_objects_with_type(shared_variables.supported_types['character']):
            if char.name == name:
                return char
        return None

    def _integrate_wordstate_with_camelot_places(self, problem: Problem):
        """A method that is used to integrate the wordstate with all components of Camelot places

        Parameters
        ----------
            none

        """
        list_loc = problem.find_objects_with_type(shared_variables.supported_types['location'])
        for location in list_loc:
            item = self._find_in_json('places', location.name, 'name')
            if item is None:
                raise Exception(
                    'Cannot find location %s in places.json' % (location.name))
            for room_component in item['room_components']:
                # Create new Relation and new Objects taken from the json and add them to the problem
                obj = self._integrate_wordstate_with_camelot_rooms_components(room_component, location.name, problem)
                # add relation with predicate at
                rel = Relation(shared_variables.supported_predicates['at'], [obj, location], RelationValue.TRUE, self.domain, problem)
                try:
                    problem.add_relation_to_initial_state(rel)
                    logging.debug(
                        "Relation %s added to the problem" % str(rel))
                except AttributeError:
                    logging.info(
                        "Relation %s already exists, so we skip it." % str(rel))
                # Parameter to set: ['Open', 'Close', 'Surface', 'Furniture', 'Seat', 'EntryPoint']
                if  "door" not in room_component['name'].lower():
                    for attribute in room_component['attribute']:
                        if attribute == '':
                            continue
                        elif attribute == 'Open':
                            # debugpy.breakpoint()
                            rel = Relation(shared_variables.supported_predicates['can_open'], [
                                        obj], RelationValue.TRUE, self.domain, problem)
                            try:
                                problem.add_relation_to_initial_state(rel)
                                logging.debug(
                                    "Relation %s added to the problem" % str(rel))
                            except AttributeError:
                                logging.info(
                                    "Relation %s already exists, so we skip it." % str(rel))
                            rel = Relation(shared_variables.supported_predicates['is_open'], [
                                        obj], RelationValue.FALSE, self.domain, problem)
                            try:
                                problem.add_relation_to_initial_state(rel)
                                logging.debug(
                                    "Relation %s added to the problem" % str(rel))
                            except AttributeError:
                                logging.info(
                                    "Relation %s already exists, so we skip it." % str(rel))
                        elif attribute == 'Close':
                            rel = Relation(shared_variables.supported_predicates['can_close'], [
                                        obj], RelationValue.TRUE, self.domain, problem)
                            try:
                                problem.add_relation_to_initial_state(rel)
                                logging.debug(
                                    "Relation %s added to the problem" % str(rel))
                            except AttributeError:
                                logging.info(
                                    "Relation %s already exists, so we skip it." % str(rel))
                        elif attribute == 'Surface':
                            rel = Relation(shared_variables.supported_predicates['has_surface'], [
                                        obj], RelationValue.TRUE, self.domain, problem)
                            try:
                                problem.add_relation_to_initial_state(rel)
                                logging.debug(
                                    "Relation %s added to the problem" % str(rel))
                            except AttributeError:
                                logging.info(
                                    "Relation %s already exists, so we skip it." % str(rel))
                        elif attribute == 'Furniture':
                            pass
                        elif attribute == 'Seat':
                            pass
                        elif attribute == 'EntryPoint':
                            pass
    
    def _integrate_wordstate_with_camelot_rooms_components(self, room_component, location_name, problem: Problem) -> Entity:
        """
        A method that is used to integrate the wordstate with all components of Camelot rooms.
        It first creates the basic entity with the part of the room described (e.g.:"alchemyshop.Table"),
        and then adds all the other parts of the specific part of the room (e.g. "alchemyshop.Table.Left").

        Parameters
        ----------
        room_component : dict
            dictionary with the components of the specific part of the room
        location_name : str
            name of the room
        problem : Problem
            The problem that the entity will be connected to.
        
        Returns
        -------
        Entity
            The first entity that is created.

        """
        obj = Entity(location_name + '.' + room_component['name'], shared_variables.supported_types['furniture'], problem)
        try:
            problem.add_object(obj)
            logging.debug("Object %s added to the problem" % str(obj))
        except AttributeError:
            logging.info("Object %s already exists, so we skip it." % str(obj))
        if "position" in room_component:
            for item in room_component['position']:
                room_internal_position = Entity(location_name + '.'+ room_component['name'] + "." + item, shared_variables.supported_types['position'], problem)
                try:
                    problem.add_object(room_internal_position)
                    logging.debug("Object %s added to the problem" % str(obj))
                except AttributeError:
                    logging.info("Object %s already exists, so we skip it." % str(obj))
        return obj

    def apply_camelot_message(self, message: str, received_action_from_platform = None) -> list:
        """
        This method gets a success message from Camelot and creates a new world state with what happened applied.

        Parameters
        ----------
            message : str
        
        Returns
        -------
        list ( tuple )
            A list of tuple with first argument the string "new" or "changed_value" to represent what has been done to the relation
            and second argument relations that are added or changed in the world state.
        """
        
        changed_relations = []
        message_parts = message.split(' ')
        
        if message_parts[0] == 'input':
            # example of message to parse: "input arrived bob position alchemyshop.Door"
            # I exclude the messages with "at"
            if message_parts[1] == "arrived" and message_parts[3] == "position":
                new_world_state = copy.deepcopy( self.world_state )
                character = new_world_state.find_entity(name = message_parts[2])
                if character is None:
                    logging.error("Character %s not found in the world state" % message_parts[2])
                    raise Exception("Character %s not found in the problem" % message_parts[2])

                # Exclude messages like "input arrived bob position luca" where the position is a character
                location_entity = new_world_state.find_entity(name = message_parts[4])
                if location_entity is not None and location_entity.type.name == "character":
                    return changed_relations

                location_parts = message_parts[4].split('.')

                relations_at = new_world_state.get_entity_relations(character, 
                                                                    predicates= [shared_variables.supported_predicates['at']], 
                                                                    value_list= [RelationValue.PENDING_FALSE, RelationValue.PENDING_TRUE, RelationValue.TRUE])
                # The character is nowhere, so we add the relation with the new position
                if len(relations_at) == 0:
                    changed_relations.append(self._create_and_add_relation_for_location(new_world_state, character, message_parts[4], shared_variables.supported_predicates['at']))
                    # Check if the room is different from the current room, if true we change the relation IN
                    if location_parts[0] != self.current_room:
                        self._change_relation_in_location(new_world_state, character, changed_relations, location_parts[0])
                else:
                    for relation_at in relations_at:
                        entity = relation_at.find_entity_with_type(entity_type = shared_variables.supported_types['position'])
                        entity_parts = entity.name.split('.')
                        if self.current_room == "":
                            self.current_room = entity_parts[0]
                        # we change relations because actions can be used from the EM to sent what to do to the platform. 
                        # location_parts can be size 2 or 3 based on the position of the room. We summarize here the conditions where we have to apply the chages of the relations.
                        evaluate_location = False
                        if len(location_parts) == 2:
                            # Same room, different position within the room
                            if location_parts[0] == entity_parts[0] and location_parts[1] != entity_parts[1]:
                                evaluate_location = True
                        elif len(location_parts) == 3:
                            # If we don't have the last part of the specific position within the room, we have to add the relation
                            if len(entity_parts) == 2:
                                evaluate_location = True
                            # Same room, different position within the room or different specific position within the room e.g. "alchemyshop.Table.Right" != "alchemyshop.Table.Left"
                            elif location_parts[0] == entity_parts[0] and (location_parts[1] != entity_parts[1] or location_parts[2] != entity_parts[2]):
                                evaluate_location = True
                        
                        if evaluate_location:
                            # We add a new relation with the new position of the character
                            changed_relations.append(self._create_and_add_relation_for_location(new_world_state, character, message_parts[4], shared_variables.supported_predicates['at']))

                        # Different primary location (room)
                        elif entity_parts[0] != location_parts[0]:
                            relation_in = new_world_state.get_entity_relations(character, 
                                                                            predicates= [shared_variables.supported_predicates['in']], 
                                                                            value_list= [RelationValue.PENDING_FALSE, RelationValue.PENDING_TRUE, RelationValue.TRUE])

                            # Now we need to change the relation at in the old room to false since the character is in a different room
                            for relation_at in relations_at:
                                changed_relations.append(self._modify_relation_value(relation_at, RelationValue.FALSE))
                            
                            # Add new relation AT to change position in the new room
                            changed_relations.append(self._create_and_add_relation_for_location(new_world_state, character, message_parts[4], shared_variables.supported_predicates['at']))

                            self._change_relation_in_location(new_world_state, character, changed_relations, location_parts[0])
                            #Changed room, so we don't need to evaluate other at predicates
                            break
                self.world_state = copy.deepcopy(new_world_state)


            # example of message to parse: "input exited bob position alchemyshop.Door.In"
            elif message_parts[1] == "exited" and message_parts[3] == "position":
                new_world_state = copy.deepcopy( self.world_state )

                character = new_world_state.find_entity(name = message_parts[2])
                if character is None:
                    logging.error("Character %s not found in the world state" % message_parts[2])
                    raise Exception("Character %s not found in the problem" % message_parts[2])
                    
                location_entity = new_world_state.find_entity(name = message_parts[4])

                relation_at = new_world_state.find_relation(Relation(shared_variables.supported_predicates['at'], [character, location_entity], RelationValue.TRUE))
                if relation_at is not None:
                    changed_relations.append(self._modify_relation_value(relation_at, RelationValue.FALSE))

                self.world_state = copy.deepcopy(new_world_state)
        elif message_parts[0] == 'succeeded':
            remove_succedeed = len("succeeded ")
            message_parts = message[remove_succedeed:].replace("(", "|").replace(")", "").replace(",", "|").replace(" ", "").split("|")
            action_definition = self.domain.find_action_with_name(message_parts[0])
            if action_definition is not None:
                if received_action_from_platform is not None and action_definition.name == received_action_from_platform.name:
                    changed_relations.append( self.world_state.apply_action(received_action_from_platform, check_action_can_apply=False))
                else:
                    # Find the entities that are used in the action
                    list_parameters_entities = []
                    for i in range(1, len(message_parts)):
                        list_parameters_entities.append(self.world_state.find_entity(name = message_parts[i]))
                    # Build the paramenters that compose the action
                    parameters = {}
                    for parameter in action_definition.parameters:
                        for entity in list_parameters_entities:
                            if parameter.type.name in entity.type.get_list_extensions():
                                parameters[parameter.name] = entity
                                break
                        if parameter.name not in parameters.keys():
                            parameters[parameter.name] = self.world_state.find_entities_with_type(parameter.type)[0]
                    
                    action = Action(action_definition, parameters)
                    changed_relations.append(self.world_state.apply_action(action , check_action_can_apply=False))
        return changed_relations

    def _change_relation_in_location(self, new_world_state: WorldState, character: Entity, changed_relations: list, location: str):
        """
        Change the relation in the location of the character. This method is used to semplifiy the code.

        Parameters
        ----------
        new_world_state: WorldState
            The new world state
        character: Entity
            The character
        changed_relations: list
            The list of changed relations
        location: str
            The location
        """
        relation_in = new_world_state.get_entity_relations(character, 
                                                        predicates= [shared_variables.supported_predicates['in']], 
                                                        value_list= [RelationValue.PENDING_FALSE, RelationValue.PENDING_TRUE, RelationValue.TRUE])
        # Doesn't matter where the character was, since we are in a different room we can set the relation with IN to false
        changed_relations.append(self._modify_relation_value(relation_in[0], RelationValue.FALSE))
        # Add new relation IN to change position in the new room
        changed_relations.append(self._create_and_add_relation_for_location(new_world_state, character, location, shared_variables.supported_predicates['in']))
        self.current_room = location


    def _modify_relation_value(self, relation: Relation, value: RelationValue) -> tuple:
        """
        This method modifies the value of a relation.

        Parameters
        ----------
        relation : Relation
            The relation that will be modified
        value : RelationValue
            The new value of the relation
        
        Returns
        -------
        tuple
            A tuple with first argument the string "changed_value" to represent what has been done to the relation
            and second argument relations that are added or changed in the world state.
        """
        relation.modify_value(value)
        return ("changed_value", copy.deepcopy(relation))
    
    def _add_relation_to_world_state(self, relation: Relation, world_state: WorldState) -> tuple:
        """
        This method adds a relation to the world state.

        Parameters
        ----------
        relation : Relation
            The relation that will be added
        
        Returns
        -------
        tuple
            A tuple with first argument the string "new" to represent what has been done to the relation
            and second argument relations that are added or changed in the world state.
        """
        world_state.add_relation(relation)
        return ("new", copy.deepcopy(relation))
    
    def _create_and_add_relation_for_location(self, world_state: WorldState, character: Entity, location: str, predicate: Predicate, relation_value = RelationValue.TRUE) -> tuple:
        """
        This method creates a relation for the location of the character and adds it to the world state.
        If the relation already exists, it will be modified with the new relation_value.

        Parameters
        ----------
        world_state : WorldState
            The world state that will be modified
        character : Entity
            The character that will be added to the relation
        location : Entity
            The location that will be added to the relation
        
        Returns
        -------
        tuple
            A tuple with first argument the string "new" to represent what has been done to the relation
            and second argument relations that are added or changed in the world state.

        """
        old_relation_value = RelationValue.FALSE if relation_value == RelationValue.TRUE else RelationValue.TRUE
        location_entity = world_state.find_entity(name = location)
        if location_entity is None:
            location_entity = Entity(location, shared_variables.supported_types['position'], self.problem)
            self.problem.add_object(location_entity)
            world_state.add_entity(location_entity)
        #check if the relation already exists in the wordstate but with false value
        relation = world_state.find_relation(Relation(predicate, [character, location_entity], old_relation_value))
        if relation is None:
            new_relation = Relation(predicate, [character, location_entity], relation_value, self.domain, self.problem)
            return self._add_relation_to_world_state(new_relation, world_state)
        else:
            return self._modify_relation_value(relation, relation_value)
    
    def create_action_from_incoming_message(self, message):
        """This method is used to create an action from an incoming message representing the action that the external agent wants to perform.

        Parameters
        ----------
        message : str
            The message that will be used to create the action
        """
        # for debugging: openfurniture(bob, alchemyshop.Chest, alchemyshop.Chest)
        message_parts = re.split(r"\(|\)|,", message)
        action_name = message_parts[0]
        action_definition = self.domain.find_action_with_name(action_name)
        if action_definition is None:
            logging.error("GameController: PDDL action \"%s\" not found in domain" %( action_name ))
            return
        parameters = {}
        if action_name.startswith("instantiate_"):
            for i in range(len(action_definition.parameters)):
                if action_definition.parameters[i].type.name == "item":
                    item = Entity(name=message_parts[i+1] + str(random.randint(0,100)), type_e=action_definition.parameters[i].type)
                    self.world_state.add_entity(item)
                    parameters[action_definition.parameters[i].name] = item
                else:
                    parameters[action_definition.parameters[i].name] = self.world_state.find_entity(name = message_parts[i+1], type=action_definition.parameters[i].type)
        else:
            for i in range(len(action_definition.parameters)):
                parameters[action_definition.parameters[i].name] = self.world_state.find_entity(name = message_parts[i+1], type=action_definition.parameters[i].type)
        return Action(action_definition, parameters=parameters)

    def apply_action(self, action: Action):
        """This method is used to apply an action to Camelot and to the world state.

        Parameters
        ----------
        action : Action
            The action that will be applied
        
        Returns
        -------
        list
            A list of relations that are added or changed in the world state.
        """
        changed_relations = self.world_state.apply_action(action)
        if action.name.startswith("instantiate_"):
            changed_relations.insert(0, ('new_entity', action.parameters['?obj']))
        return changed_relations
    
    def check_action_can_apply(self, action: Action):
        """This method is used to check if an action can be applied.

        Parameters
        ----------
        action : Action
            The action that will be checked
        
        Returns
        -------
        bool
            True if the action can be applied, False otherwise
        """
        return self.world_state.check_action_can_apply(action)
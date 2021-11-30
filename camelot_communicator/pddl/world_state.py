from pddl.domain import Domain
from pddl.action_definition import ActionDefinition
from pddl.predicate import Predicate
from pddl.action_definition import ActionProposition
from pddl.action import Action
from pddl.relation import Relation
from pddl.relation_value import RelationValue
from pddl.entity import Entity
import logging


class WorldState:

    def __init__(self, domain: Domain):
        self.__domain = domain
        self.__relations = []
        self.__entities = []

    @property
    def entities(self):
        """Getter for entities

        """
        return self.__entities

    @entities.setter
    def entities(self, entities):
        """Setter for entities

        """
        self.__entities = entities

    @property
    def relations(self):
        """Getter for relations

        """
        return self.__relations

    @relations.setter
    def relations(self, relations):
        """Setter for relations

        """
        self.__relations = relations

    def add_relation(self, relation):
        """A method that is used to add a relation to the current worldstate

        Parameters
        ----------
        relation : type Relation
            relation that needs to be added
        """
        if type(relation) != Relation:
            raise TypeError("add_relation type must be Relation")
        if self.find_relation(relation) == None:
            self.__relations.append(relation)
        else:
            logging.info(
                "wolrdstate.add_relation(%s) -> The relation already exists. Skipping." % relation.predicate.name)

    def find_relation(self, relation: Relation, exclude_value=False) -> Relation:
        """A method that is used to find a relation in the current WorldState

        Returns the relation or None.

        Parameters
        ----------
        relation : type Relation
            relation that needs to be found
        exclude_value : bool, optional, default False
            if True, it will find the relation without evaluating the relation_value.
        """
        for item in self.__relations:
            if exclude_value:
                if item.equals_exclude_value(relation):
                    return item
            else:
                if item == relation:
                    return item
        return None

    def add_entity(self, entity):
        """A method that is used to add an entity to the list of entities

        Parameters
        ----------
        entity : type Entity
            entity that will be added to the list of entities
        """
        if type(entity) != Entity:
            raise TypeError("add_entity type must be Entity")
        if self.find_entity(entity) == None:
            self.__entities.append(entity)
        else:
            logging.info(
                "wolrdstate.add_entity(%s) -> The entity already exists. Skipping." % entity.name)

    def find_entity(self, entity) -> Entity:
        """A method that is used to find a Entity in the current WorldState

        Returns the Entity or None.

        Parameters
        ----------
        Entity : type Entity
            Entity that needs to be found
        """
        if type(entity) != Entity:
            raise TypeError("find_entity type must be Entity")
        for item in self.__entities:
            if item == entity:
                return item
        return None

    def find_entity_with_name(self, name: str) -> Entity:
        """A method that is used to find an entity with a specific name ignoring the case in the name

        Returns the Entity or None.

        Parameters
        ----------
        name : str
            name of the entity that needs to be found
        """
        for item in self.__entities:
            if item.name.lower() == name.lower():
                return item
        return None

    def get_dict_predicates(self) -> dict:
        """A method that is used to return a dict with all the predicates listed inside the domain

        Parameters
        ----------
            none
        """
        return_dict = {}
        for item in self.__domain.predicates:
            return_dict[item.name] = item
        return return_dict

    def find_entity_ignore_case(self, entity: Entity) -> Entity:
        """A method that is used to find a Entity in the current WorldState without checking for the case in the name

        Returns the Entity or None.

        Parameters
        ----------
        Entity : type Entity
            Entity that needs to be found
        """

        for item in self.__entities:
            if item.name.lower() == entity.lower():
                return item
        return None

    def can_action_be_applied(self, action: Action) -> bool:
        """A method that is used to check if an action can be applied to the current worldstate

        This method checks the precondition of the action in the current worldstate and returns True if the action can be applied, False otherwise.
        Parameters
        ----------
        action : type Action
            action to be checked if it can be applied
        """
        result = self._check_precondition_recursive(action.preconditions)

        return result

    def _check_precondition_recursive(self, action_proposition: ActionProposition):
        """A method that is used to check if the preconditions of the action can be applied to the worldstate. 
        Recursive method.

        Parameters
        ----------
        action_proposition : type ActionProposition
            ActionProposition that needs to be applied.
        """
        if action_proposition.name == 'and':
            for item in action_proposition.parameters:
                if type(item) == Relation:
                    if self.find_relation(item) is None:
                        return False
                elif type(item) == ActionProposition:
                    if self._check_precondition_recursive(item) == False:
                        return False
            return True
        elif action_proposition.name == 'or':
            for item in action_proposition.parameters:
                if type(item) == Relation:
                    if self.find_relation(item) is not None:
                        return True
                elif type(item) == ActionProposition:
                    if self._check_precondition_recursive(item) == True:
                        return True
            return False
        elif action_proposition.name == 'forall':
            # TODO: forall precondition check
            pass

    def apply_action(self, action: Action):
        """A method that is used to apply an action to the current worldstate. It returns the new worldstate.

        Parameters
        ----------
        action : Action
            action that we want to apply to the current worldstate.
        """
        if self.can_action_be_applied(action):
            self._apply_action_effect(action.effects)

    def _apply_action_effect(self, action_definition: ActionDefinition):
        """A method that is used to apply the effect of an action to the current worldstate.

        Parameters
        ----------
        action_definition : type ActionDefinition
            effect of the action that we want to apply to the worldstate
        """
        for relation in action_definition.parameters:
            worldstate_relation = self.find_relation(
                relation, exclude_value=True)

            if worldstate_relation is None:
                self.add_relation(relation)
            else:
                worldstate_relation.modify_value(relation.value)

    def get_entity_relations(self, entity: Entity, predicates=None, value_list = None) -> list:
        """A method that is used to get the relations of an entity. If predicate is not None, it will return only the relations that have the specified predicates.

        Parameters
        ----------
        entity : type Entity
            entity that we want to get the relations
        predicates : list, optional
            list of predicates that we want to get the relations of
        value_list : list, optional
            list of values that we want to get the relations of
        """
        if predicates is not None:
            if type(predicates) != list:
                raise TypeError("get_entity_relations: predicates type must be list")
        return_list = []
        for item in self.__relations:
            # Excluding values that are not listed in value list
            if value_list is not None:
                if item.value not in value_list:
                    continue
            if entity in item.entities:
                if predicates is None:
                    return_list.append(item)
                else:
                    if item.predicate in predicates:
                        return_list.append(item)
        return return_list

    def __str__(self) -> str:
        string = "entities: \n\t"
        for item in self.__entities:
            string += "%s, " % (str(item))
        string += "\nRelations: \n"
        for item in self.__relations:
            string += "\t%s\n " % (str(item))
        return string

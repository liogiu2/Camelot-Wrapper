from pddl.relation import Relation
from pddl.action_definition import ActionDefinition
from pddl.entity import Entity
import logging

class WorldState:

    def __init__(self, domain):
        self.__domain = domain
        self.__relations = []
        self.__entities = []

    @property
    def entities(self):
        """Getter for entities

        """
        return self.__relations
    
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
            logging.info("wolrdstate.add_relation(%s) -> The relation already exists. Skipping."%relation.predicate.name)


    def find_relation(self, relation) -> Relation:
        """A method that is used to find a relation in the current WorldState
        
        Returns the relation or None.

        Parameters
        ----------
        relation : type Relation
            relation that needs to be found
        """
        if type(relation) != Relation:
            raise TypeError("find_relation type must be Relation")
        for item in self.__relations:
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
            logging.info("wolrdstate.add_entity(%s) -> The entity already exists. Skipping."%entity.name)

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

    def can_action_be_applied(self, action) -> bool:
        """A method that is used to check if an action can be applied to the current worldstate
        
        This method checks the precondition of the action in the current worldstate and returns True if the action can be applied, False otherwise.
        Parameters
        ----------
        action : type Action
            action to be checked if it can be applied
        """
        result = False

        return result


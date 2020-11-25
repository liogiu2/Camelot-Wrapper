from pddl.predicate import Predicate
from pddl.action import Action
from pddl.types import Type

# self.domain_name = 'unknown'
# self.requirements = []
# self.actions = []
# self.types = []
# self.predicates = []

class Domain:

    def __init__(self, name = ''):
        self.__domain_name = name
        self.__types = []
        self.__predicates = []

    #-----------------------------------
    #       Name methods
    #-----------------------------------
    @property
    def domain_name(self):
        """
        Getter for the name of the domain
        """
        return self.__domain_name
    
    @domain_name.setter
    def domain_name(self, name):
        """
        Setter for the name of the domain
        """
        self.__domain_name = name
    
    #-----------------------------------
    #       Requirements methods
    #-----------------------------------
    
    @property
    def requirements(self):
        """
        Getter for the requirements of the domain
        """
        return self.__requirements

    @requirements.setter
    def requirements(self, requirements):
        """
        Setter for the requirements of the domain
        """
        self.__requirements = requirements
    
    #-----------------------------------
    #       Actions methods
    #-----------------------------------

    @property
    def actions(self):
        """
        Getter for the actions of the domain
        """
        return self.__actions

    @actions.setter
    def actions(self, actions):
        """
        Setter for the actions of the domain
        """
        self.__actions = actions
    
    #-----------------------------------
    #       Types methods
    #-----------------------------------

    @property
    def types(self):
        """
        Getter for the types of the domain
        """
        return self.__types

    @types.setter
    def types(self, types):
        """
        Setter for the types of the domain
        """
        if type(types) is not list:
            raise Exception("Types must be a list")

        self.__types = types

    def find_type(self, type_name):
        """
        Find type within the list of types
        """
        for type in self.types:
            if type.name == type_name:
                return type
        return None
    
    def add_type(self, type_d):
        """
        Add type to the list of Types
        """
        if type(type_d) is not Type:
            raise Exception('Expected type PDDL.Type when adding Type to the domain')

        t = self.find_type(type_d.name)
        if t is not None:
            raise Exception('Cannot add 2 Type to the domain with the same name: %s'%(type_d.name))
       
        self.__types.append(type_d)
        
    #-----------------------------------
    #       Predicates methods
    #-----------------------------------    

    @property
    def predicates(self):
        """
        Getter for the predicates of the domain
        """
        return self.__predicates

    @predicates.setter
    def predicates(self, predicates):
        """
        Setter for the predicates of the domain
        """
        self.__predicates = predicates
    
    def find_predicate(self, predicate_name):
        """
        Find predicate in the list of predicates based on the name and return the object type Predicate. If it's not found return None.
        """
        for item in self.predicates:
            if item.name == predicate_name:
                return item
        return None
    
    def add_predicate(self, predicate):
        """
        Add predicate to the list of predicates
        """
        if type(predicate) is not Predicate:
            raise Exception('predicate type must be Predicate')

        if self.find_predicate(predicate.name) is not None:
            raise Exception('Predicate with name %s already exists'%(predicate.name))

        self.__predicates.append(predicate)
    
    
    

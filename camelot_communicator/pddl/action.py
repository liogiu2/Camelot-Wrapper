#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from pddl.types import Type


class Action:

    def __init__(self, name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects):
        self.name = name
        self.parameters = parameters
        self.positive_preconditions = positive_preconditions
        self.negative_preconditions = negative_preconditions
        self.add_effects = add_effects
        self.del_effects = del_effects

    def __str__(self):
        return 'action: ' + self.name + \
        '\n  parameters: ' + str(self.parameters) + \
        '\n  positive_preconditions: ' + str(self.positive_preconditions) + \
        '\n  negative_preconditions: ' + str(self.negative_preconditions) + \
        '\n  add_effects: ' + str(self.add_effects) + \
        '\n  del_effects: ' + str(self.del_effects) + '\n'

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class ActionParameter:

    def __init__(self, name, type_p):
        self.name = name
        if type(type_p) is not Type:
            raise Exception('The type of the AcionParameter needs an object class Type but got %s'%(type(type_p)))
        self.type = type_p

class ActionProposition:

    def __init__(self, name, parameters):
        self.name = name
        if type(parameters) is not list:
            raise Exception ('Parameters must be a list')
        self.parameters = parameters
    
    def add_parameter(self, item):
        self.parameters.append(item)



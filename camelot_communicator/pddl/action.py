#!/usr/bin/env python
# Four spaces as indentation [no tabs]

from pddl.types import Type


class Action:

    def __init__(self, name, parameters, preconditions, effects):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effects = effects

    def __str__(self):
        string = 'action: ' + self.name 
        string +='\n\t  parameters: '
        for item in self.parameters:
            string += str(item)
        string +='\n\t  preconditions: ' + str(self.preconditions)
        string +='\n\t  effects: ' + str(self.effects) + '\n'
        return string

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

class ActionParameter:

    def __init__(self, name, type_p):
        self.name = name
        if type(type_p) is not Type:
            raise Exception('The type of the ActionParameter needs an object class Type but got %s'%(type(type_p)))
        self.type = type_p

    def __str__(self) -> str:
        return ' %s (%s) '%(self.name, str(self.type.name))
    

class ActionProposition:

    def __init__(self, name, parameters, argument = None):
        self.name = name
        if type(parameters) is not list:
            raise Exception ('Parameters must be a list')
        self.parameters = parameters
        if argument is None and name == 'forall':
            raise Exception('Forall needs an argument to check')
        if argument is not None:
            self.argument = argument

    
    def add_parameter(self, item):
        self.parameters.append(item)

    def __str__(self):
        string = ""
        if self.name == 'forall':
            string = self.name + '('
            string += self.argument.name + '): ('
        else:
            string = self.name + '('
        for item in self.parameters:
            string += str(item) + ', '
        string = string[:-2]
        string += ')'
        return string
    




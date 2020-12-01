from pddl.types import Type


class Entity:

    def __init__(self, name, type_e):
        self.name = name
        if type(type_e) is not Type:
            raise Exception('Expected Type got %s'%(type(type_e)))
        self.type = type_e


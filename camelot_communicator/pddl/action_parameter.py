from pddl.types import Type

class ActionParameter:

    def __init__(self, name, type_p):
        self.name = name
        if type(type_p) is not Type:
            raise Exception('The type of the ActionParameter needs an object class Type but got %s'%(type(type_p)))
        self.type = type_p

    def __str__(self) -> str:
        return ' %s (%s) '%(self.name, str(self.type.name))
    
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and 
            self.name == other.name and 
            self.type == other.type
        )
    
    def to_PDDL(self):
        """A method that is used to transform the action parameter to PDDL

        Returns
        -------
        String
            PDDL representation of the action parameter
        """
        return '%s'%(self.name)
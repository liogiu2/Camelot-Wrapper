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
    
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and 
            self.name == other.name and 
            self.argument == other.argument and 
            all(map(lambda x, y: x == y, self.parameters, other.parameters))
        )
    
    def to_PDDL(self):
        """A method that is used to transform the action proposition to PDDL

        Returns
        -------
        String
            PDDL representation of the action
        """
        return_string = ""
        if self.name == 'forall':
            return_string += "( forall ("
            return_string += self.argument.name+ " - " +self.argument.type.name +') : '
        else:
            return_string += "(" + self.name + " "
        for item in self.parameters:
            return_string += "("
            return_string += item.to_PDDL()
            return_string += ")"
        return_string += ")"
        return return_string
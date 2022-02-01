class ActionDefinition:

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
        return (
            self.__class__ == other.__class__ and 
            self.name == other.name and 
            all(map(lambda x, y: x == y, self.parameters, other.parameters)) and 
            self.preconditions == other.preconditions and 
            self.effects == other.effects
        )
    
    def get_dict_parameters(self):
        return_dict = {}
        for item in self.parameters:
            return_dict[item.name] = item.type
        return return_dict
    




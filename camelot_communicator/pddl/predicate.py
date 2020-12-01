class Predicate:
    
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments             

    def __str__(self):
        string = ' '+ self.name  +'('
        i = 1
        for item in self.arguments:
            string += item.name +','
            i += 1
        string = string[:-1]
        string += ')'
        return string


    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __repr__(self):
        string= "Predicate: %s " % (self.name)
        for item in self.arguments:
            string += '%s '%(item)
    
    def find_argument_with_type(self, type): #TODO: check all chain of extends, probably need to to it in the domain
        for item in self.arguments:
            if item.name == type:
                return item
        return None

class Predicate:
    
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments             

    def __str__(self):
        string = 'Predicate: '+ self.name + '\n'
        i = 1
        for item in self.arguments:
            string += 'Argument %s Type: %s'%(str(i), item)
            i += 1
        return string


    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __repr__(self):
        string= "Predicate: %s " % (self.name)
        for item in self.arguments:
            string += '%s '%(item)
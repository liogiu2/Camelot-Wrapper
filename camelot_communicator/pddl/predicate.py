class Predicate:
    
    def __init__(self, name, argument_1, argument_2 = None):
        self.name = name
        self.argument_1 = argument_1
        self.unary = True
        if argument_2 != None:
            self.argument_2 = argument_2
            self.unary = False   
             

    def __str__(self):
        return 'Predicate: '+ self.name + \
        '\n  argument_1: ' + str(self.argument_1) +\
        '%s' % str('\n  argument_2: ' + self.argument_2 if not self.unary else '') 

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "Predicate: %s %s %s" % (self.name, str(self.argument_1), str(self.argument_2) if not self.unary else '')
class Type:

    def __init__(self, name, extend):
        self.name = name
        self.extend = extend

    def __str__(self):
        return 'Type: ' + self.name + \
        '\n  extends: ' + str(self.extend)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "Type: %s" % (self.name)
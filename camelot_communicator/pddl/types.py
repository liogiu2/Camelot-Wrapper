class Type:

    def __init__(self, name, extend):
        self.name = name
        self.extend = extend

    def __str__(self):
        return 'Type: ' + self.name + \
        ' extends: ' + str(self.extend)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return "Type: %s" % (self.name)
    
    def get_list_extensions(self):
        extensions = []
        extensions.append(self.name)
        if self.name != 'object':
            list_ext = self.extend.get_list_extensions()
            for item in list_ext:
                extensions.append(item)
        return extensions

    
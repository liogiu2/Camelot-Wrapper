from pddl.domain import Domain


class Problem:
    """
    
    """
    
    def __init__(self, name, domain, objects = [], initial_state = []):
        self.problem_name = name
        if type(domain) is not Domain:
            raise Exception("Domain in problem was expecting type Domain got %s"%(type(domain)))
        self.domain = domain
        self.__objects = objects
        self.__initial_state = initial_state

    @property
    def objects(self):
        """
        Getter for objects
        """
        return self.__objects
    
    @objects.setter
    def objects(self, objects):
        """
        Setter for objects
        """
        self.__objects = objects
    
    def add_object(self, obj):
        if self.find_objects(obj.name) is not None:
            raise AttributeError('Object %s in the problem already exists'%(obj.name))
        self.__objects.append(obj)
    
    def find_objects(self, obj_name):
        # if '.' in obj_name:
        #     obj_name = '.'.join(map(lambda s: s.strip().capitalize(), obj_name.split('.')))
        #     obj_name = obj_name[0].lower() + obj_name[1:]
        for item in self.__objects:
            if item.name.lower() == obj_name.lower():
                return item
        return None
    
    @property
    def initial_state(self):
        """
        Getter for initial_state
        """
        return self.__initial_state
    
    @initial_state.setter
    def initial_state(self, initial_state):
        """
        Setter for initial_state
        """
        self.__initial_state = initial_state
    
    def add_relation_to_initial_state(self, relation):
        """A method that is used to add a relation to the initial state
        
        Parameters
        ----------
        relation : Relation
        """
        if relation in self.__initial_state:
            raise AttributeError('Relation already exists in current problem.')
        self.initial_state.append(relation)
    
    def __str__(self) -> str:
        string = "Problem name: %s "%(self.problem_name)
        string += "Associated Domain name: %s\n"%(self.domain.domain_name)
        string += "Objects: \n\t"
        for item in self.objects:
            string += "%s, "%(str(item))
        string += "\nInitial State: \n"
        for item in self.initial_state:
            string += "\t%s\n "%(str(item))
        return string
    
    def find_objects_with_type(self, type_e, exclude_types = []):
        return_list = []
        for item in self.objects:
            if type_e in item.type.get_list_extensions():
                if item.type not in exclude_types:
                    return_list.append(item)
        return return_list
    
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
            self.problem_name == other.problem_name and 
            all(map(lambda x, y: x == y, self.__objects, other.objects)) and 
            all(map(lambda x, y: x == y, self.__initial_state, other.initial_state)) and 
            self.domain == other.domain
            )

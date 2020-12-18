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
        self.__objects.append(obj)
    
    def find_objects(self, obj_name):
        if '.' in obj_name:
            obj_name = '.'.join(map(lambda s: s.strip().capitalize(), obj_name.split('.')))
            obj_name = obj_name[0].lower() + obj_name[1:]
        for item in self.__objects:
            if item.name == obj_name:
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
    
    def find_objects_with_type(self, type_e):
        return_list = []
        for item in self.objects:
            if item.type == type_e:
                return_list.append(item)
        return return_list

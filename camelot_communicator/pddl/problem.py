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
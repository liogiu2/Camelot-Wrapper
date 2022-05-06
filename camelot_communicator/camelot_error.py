try:
    from shared_variables import action_list
except (ModuleNotFoundError, ImportError):
    from .shared_variables import action_list

class CamelotError:
    """
    This class is used to store a camelot error.
    """
    # error SetPosition "Specified Place, position, or entity does not exist: alchemyshop.door"

    def __init__(self, error_message):
        self.error_message = error_message
        try:
            self._error_evaluation()
        except:
            pass
        self.handled = False

    def __str__(self):
        return self.error_message
    
    def _error_evaluation(self):
        """
        This method is used to evaluate the error.
        """
        error_split = self.error_message.replace('"', '').split()
        list_names = list(set(error_split) & set(action_list))
        if len(list_names) > 0:
            self.action_name = list_names[0]
        else:
            self.action_name = None
    
    def close_error(self):
        """
        This method is used to close the error.
        """
        self.handled = True
        

        
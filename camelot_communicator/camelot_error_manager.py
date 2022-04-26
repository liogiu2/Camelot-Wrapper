try:
    from platform_IO_communication import PlatformIOCommunication
    from camelot_error import CamelotError
except (ModuleNotFoundError, ImportError):
    from .platform_IO_communication import PlatformIOCommunication
    from .camelot_error import CamelotError
from singleton_decorator import singleton

@singleton
class CamelotErrorManager:
    """
    This class is used to manage camelot errors.
    """
    platform_IO_communication = PlatformIOCommunication()

    def __init__(self):
        self._errors = []
        self._solved_errors = []
    
    def add_error(self, error : CamelotError):
        """
        This method is used to add an error on the list of errors and send it to the platform.

        Parameters
        ----------
        error : CamelotError
            The error to add.
        """
        self._errors.append(error)
        self.platform_IO_communication.send_error_message(str(error))
    
    def check_errors_with_action(self, action_name, command):
        """
        This method is used to check if there is an error that has the same action name.

        Parameters
        ----------
        action_name : str
            The action name to check.
        command : str
            The command to check.
        """
        for error in self._errors:
            if error.action_name == action_name:
                # Find arguments of the command
                arguments = command[command.find("(")+1:command.find(")")].split(',')
                # Check if the arguments of the command are in (any part of) the error message
                common_elements = set(error.error_message.split()) & set(arguments)
                if len(common_elements) > 0:
                    # If there is a common element, the error is solved
                    self.solve_error(error)
                    return error
        return None
    
    def solve_error(self, error: CamelotError):
        """
        This function is used to solve an error.

        Parameters
        ----------
        error : CamelotError
            The error to solve.
        """
        error.close_error()
        self._solved_errors.append(error)
        self._errors.remove(error)



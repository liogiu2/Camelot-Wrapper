from platform_IO_communication import PlatformIOCommunication
from camelot_error import CamelotError
from utilities import singleton

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
        """
        self._errors.append(error)
        self.platform_IO_communication.send_error_message(str(error))
    
    def check_errors_with_action(self, action_name, command):
        """
        This method is used to check if there is an error that has the same action name.
        """
        for error in self._errors:
            if error.action_name == action_name:
                # Find arguments of the command
                arguments = command[command.find("(")+1:command.find(")")].split(',')
                # Check if the arguments of the command are in (any part of) the error message
                common_elements = set(error.error_message.split()) & set(arguments)
                if len(common_elements) > 0:
                    return error
        return None
    



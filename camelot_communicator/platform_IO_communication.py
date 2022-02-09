from utilities import singleton

@singleton
class PlatformIOCommunication:
    """
    This class is used to send and receive messages to the platform.
    """
    # External Communication: https://zeromq.org/
    # APIs: https://anderfernandez.com/en/blog/how-to-create-api-python/
    

    def __init__(self):
        pass

    def send_message(self, message):
        """
        This method is used to send a message to the platform.

        Parameters 
        ----------
        message : str
            The message to be sent.
        """
        pass

    def receive_message(self) -> str:
        """
        This method is used to receive a message from the platform.

        Returns
        -------
        str
            The message received from the platform.
        """
        return ""
    
    def send_error_message(self, message):
        """
        This method is used to send an error message to the platform.

        Parameters
        ----------
        message : str
            The error message to be sent.
        """
        pass


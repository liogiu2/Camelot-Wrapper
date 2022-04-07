from utilities import singleton
import requests
import json
import time
import threading
import queue
import debugpy


@singleton
class PlatformIOCommunication:
    """
    This class is used to send and receive messages to the platform.
    """    

    def __init__(self):
        self.base_link  = "http://127.0.0.1:8080"
        self.__online = self._is_platform_online()
        self.__message_queue = queue.Queue()
        self.__input_thread = threading.Thread(target=self.__receive_message_thread, args=(self.__message_queue), daemon=True)
        self.initial_message_link = ""
        self.receive_message_link = ""
        self.send_message_link = ""

    def __receive_message_thread(self, message_queue: queue.Queue):
        """
        This method is used to create a thread that continuosly makes request to the platform to receive a new message when available.
        """
        while self.__online:
            message = self._receive_message()
            if message != "":
                message_queue.put(message)
            time.sleep(0.2)

    def send_message(self, message):
        """
        This method is used to send a message to the platform.

        Parameters 
        ----------
        message : str
            The message to be sent.
        """
        if self.__online:
            response = requests.post(self.base_link + self.send_message_link, data = json.dumps({'text':message}))
            pass
    
    def get_received_message(self):
        """
        This method is used to get the received message from the platform.

        Returns
        -------
        str
            The received message. "" if no message is available.
        """
        try:
            return self.__message_queue.get_nowait()
        except queue.Empty:
            return ""

    def _receive_message(self) -> str:
        """
        This method is used to receive a message from the platform.

        Returns
        -------
        str
            The message received from the platform.
        """
        if self.__online:
            response = requests.get(self.base_link + self.receive_message_link)
            return response.json()['text']
        return ""
    
    def send_error_message(self, message):
        """
        This method is used to send an error message to the platform.

        Parameters
        ----------
        message : str
            The error message to be sent.
        """
        if self.__online:
            response = requests.post(self.base_link + "/add_error_message", data = json.dumps({'text':message, "error_type": ""}))
            pass

    def _is_platform_online(self) -> bool:
        """
        This method is used to check if the API of the evaluation platform is online.

        Returns
        -------
        bool
            True if the API is online, False otherwise.
        """
        t = threading.Timer(10.0, self._is_platform_online)
        t.start()
        try:
            response = requests.head(self.base_link + "/")
            if response.status_code == 200:
                return True
            else:
                t.cancel()
                return False
        except:
            t.cancel()
            return False


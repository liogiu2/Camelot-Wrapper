import debugpy
from camelot_error_manager import CamelotErrorManager
from camelot_IO_communication import CamelotIOCommunication
from utilities import singleton
import threading
from queue import Queue, Empty
import logging
import shared_variables

@singleton
class CamelotInputMultiplexer:

    __messages_management = None
    __input_queue = None
    __location_queue = None
    __success_queue = None
    __other_queue = None
    __thread_running = True
    __started = False

    def start(self):
        if not self.__started:
            self.camelot_IO_communication = CamelotIOCommunication()
            self.camelot_IO_communication.start()
            self.__input_queue = Queue()
            self.__location_queue = Queue()
            self.__success_queue = Queue()
            self.__error_queue = Queue()
            self.__other_queue = Queue()
            self.__messages_management = threading.Thread(target=self._input_messages_management , args =(), daemon=True)
            self.__messages_management.start()
            self.__started = True
            self._camelot_error_manager = CamelotErrorManager()

    def _input_messages_management(self):
        """
        This thread is used to manage the input messages received from the camelot_IO_communication.
        It gets the messages from the camelot_IO_communication and put them in the right queue that is used from the main thread.
        """

        while self.__thread_running:
            message = self.camelot_IO_communication.get_message()
            logging.debug("CamelotInputMultiplexer: Got message from main queue: %s" % message)

            if message == "input Quit":
                self.__thread_running = False
                self.stop()
                break

            if message.startswith("succeeded"):
                self.__success_queue.put(message)
                logging.debug("CamelotInputMultiplexer: Added to success queue")
            elif message.startswith("input"):
                if message.startswith(shared_variables.location_message_prefix):
                    self.__location_queue.put(message)
                    logging.debug("CamelotInputMultiplexer: Added to location queue")
                else:
                    self.__input_queue.put(message)
                    logging.debug("CamelotInputMultiplexer: Added to input queue")
            elif message.startswith("started"):
                logging.debug("CamelotInputMultiplexer: Received started so I pass next print to realease the event")
                self.camelot_IO_communication.print_action("%PASS%")
            elif message.startswith("error") or message.startswith("failed") or message.lower().startswith("exception"):
                self.__error_queue.put(message)
                logging.debug("CamelotInputMultiplexer: Added to error queue")
            else:
                self.__other_queue.put(message)
                logging.debug("CamelotInputMultiplexer: Added to other queue")
    
    def get_success_message(self, command, action_name):
        """
        This method is used from the main thread to get the success messages that come from Camelot.
        """
        message = ""
        try:
            message = self.__success_queue.get_nowait()
        except Empty:
            message = None
            error = self._camelot_error_manager.check_errors_with_action(action_name, command)
            if error != None:
                return False
        
        if message != None:
            logging.debug("CamelotInputMultiplexer: Got success message: %s"%(message))
            if message == "kill":
                raise Exception("Kill called - End program")
        return message
    
    def get_error_message(self):
        """
        This method is used to get the error messages that come from Camelot. If message_part is not None, it will return the error message that contains the message_part.

        Parameters
        ----------
        message_part : str
            The part of the error message that is searched for.
        """
        try:
            message = self.__error_queue.get_nowait()
            logging.debug("CamelotInputMultiplexer(get_success_message): Got error message: %s"%(message))
        except Empty:
            message = None

        return message
    
    def get_input_message(self, no_wait = False):
        """
        This method is used from the main thread to get the input messages that come from Camelot.
        """
        if no_wait:
            message = self.__input_queue.get_nowait()
        else:
            message =  self.__input_queue.get()
        logging.debug("CamelotInputMultiplexer: Got input message: %s"%(message))
        if message == "kill":
            raise Exception("Kill called - End program")
        return message
    
    def get_location_message(self, no_wait = False):
        """
        This method is used from the main thread to get the location messages that come from Camelot.
        """
        if no_wait:
            message = self.__location_queue.get_nowait()
        else:
            message =  self.__location_queue.get()
        logging.debug("CamelotInputMultiplexer: Got location message: %s"%(message))
        if message == "kill":
            raise Exception("Kill called - End program")
        return message
    
    def stop(self):
        """
        This method is used to stop the thread.
        """
        logging.debug("CamelotInputMultiplexer: Stopping camelot input multiplexer...")
        self.__thread_running = False
        self.__messages_management.join()
        self.camelot_IO_communication.stop()
        self.__input_queue.put("kill")
        self.__location_queue.put("kill")
        self.__success_queue.put("kill")
        self.__other_queue.put("kill")

            



            


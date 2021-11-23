from camelot_IO_communication import CamelotIOCommunication, singleton
import threading
from queue import Queue
import logging

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
            self.__location_message_prefix = ("input started walking", "input stopped walking", "input arrived", "input exited")
            self.__success_queue = Queue()
            self.__other_queue = Queue()
            self.__messages_management = threading.Thread(target=self._input_messages_management , args =(), daemon=True)
            self.__messages_management.start()
            self.__started = True

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
                if message.startswith(self.__location_message_prefix):
                    self.__location_queue.put(message)
                    logging.debug("CamelotInputMultiplexer: Added to location queue")
                else:
                    self.__input_queue.put(message)
                    logging.debug("CamelotInputMultiplexer: Added to input queue")
            elif message.startswith("started"):
                logging.debug("CamelotInputMultiplexer: Received started so I pass next print to realease the event")
                self.camelot_IO_communication.print_action("%PASS%")
            else:
                self.__other_queue.put(message)
                logging.debug("CamelotInputMultiplexer: Added to other queue")
    
    def get_success_message(self, text = ""):
        """
        This method is used from the main thread to get the success messages that come from Camelot.
        """
        message = self.__success_queue.get()
        logging.debug("CamelotInputMultiplexer: Got success message: %s"%(message))
        if message == "kill":
            raise Exception("Kill called - End program")
        return message
    
    def get_input_message(self, text = ""):
        """
        This method is used from the main thread to get the input messages that come from Camelot.
        """
        message =  self.__input_queue.get()
        logging.debug("CamelotInputMultiplexer: Got input message: %s"%(message))
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

            



            


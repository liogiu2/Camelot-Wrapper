from camelot_IO_communication import CamelotIOCommunication, singleton
import threading
from queue import Queue
import logging

@singleton
class CamelotInputMultiplexer:

    #https://stackoverflow.com/questions/4103773/efficient-way-of-having-a-function-only-execute-once-in-a-loop
    #https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    #https://stackoverflow.com/questions/42237752/single-instance-of-class-in-python


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

        while self.__thread_running:
            message = self.camelot_IO_communication.get_message()
            logging.debug("Got message from main queue: %s" % message)

            if message == "timeout" or message == "kill" or message == "input Quit":
                self.stop()
                break

            if message.startswith("succeeded"):
                logging.debug("Adding to success queue...")
                self.__success_queue.put(message)
                logging.debug("Added to success queue")
            elif message.startswith("input"):
                if message.startswith(self.__location_message_prefix):
                    logging.debug("Adding to location queue...")
                    self.__location_queue.put(message)
                    logging.debug("Added to location queue")
                else:
                    logging.debug("Adding to input queue...")
                    self.__input_queue.put(message)
                    logging.debug("Added to input queue")
            else:
                logging.debug("Adding to other queue...")
                self.__other_queue.put(message)
                logging.debug("Added to other queue")
    
    def get_success_message(self, text = ""):
        logging.debug("Getting success message...")
        message = self.__success_queue.get()
        logging.debug("Got success message: %s"%(message))
        if message == "kill":
            raise Exception("Kill called - End program")
        return message
    
    def get_input_message(self, text = ""):
        message =  self.__input_queue.get()
        if message == "kill":
            raise Exception("Kill called - End program")
        return message
    
    def stop(self):
        logging.debug("Stopping camelot input multiplexer...")
        self.__thread_running = False
        self.__messages_management.join()
        self.camelot_IO_communication.stop()
        self.__input_queue.put("kill")
        self.__location_queue.put("kill")
        self.__success_queue.put("kill")
        self.__other_queue.put("kill")

            



            


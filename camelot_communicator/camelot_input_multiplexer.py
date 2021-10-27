from camelot_IO_communication import CamelotIOCommunication
import threading
from queue import Queue
import logging

class CamelotInputMultiplexer:

    #https://stackoverflow.com/questions/4103773/efficient-way-of-having-a-function-only-execute-once-in-a-loop
    #https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
    #

    __messages_management = None
    __input_queue = None
    __location_queue = None
    __success_queue = None
    __other_queue = None
    __thread_running = True

    @classmethod
    def start(cls):
        CamelotIOCommunication.start()
        cls.__input_queue = Queue()
        cls.__location_queue = Queue()
        cls.__location_message_prefix = ("input started walking", "input stopped walking", "input arrived", "input exited")
        cls.__success_queue = Queue()
        cls.__other_queue = Queue()
        cls.__messages_management = threading.Thread(target=cls._input_messages_management , args =(), daemon=True)
        cls.__messages_management.start()

    @classmethod
    def _input_messages_management(cls):

        while cls.__thread_running:
            message = CamelotIOCommunication.get_message()
            logging.debug("Got message from main queue: %s" % message)

            if message == "timeout":
                cls.stop()
                break

            if message.startswith("succeeded"):
                logging.debug("Adding to success queue...")
                cls.__success_queue.put(message)
                logging.debug("Added to success queue")
            elif message.startswith("input"):
                if message.startswith(cls.__location_message_prefix):
                    logging.debug("Adding to location queue...")
                    cls.__location_queue.put(message)
                    logging.debug("Added to location queue")
                else:
                    logging.debug("Adding to input queue...")
                    cls.__input_queue.put(message)
                    logging.debug("Added to input queue")
            else:
                logging.debug("Adding to other queue...")
                cls.__other_queue.put(message)
                logging.debug("Added to other queue")
    
    @classmethod
    def get_success_message(cls, text = ""):
        logging.debug("Getting success message...")
        message = cls.__success_queue.get()
        logging.debug("Got success message: %s"%(message))
        if message == "kill":
            raise Exception("Kill called - End program")
        return message
    
    @classmethod
    def get_input_message(cls, text = ""):
        message =  cls.__input_queue.get()
        if message == "kill":
            raise Exception("Kill called - End program")
        return message
    
    @classmethod
    def stop(cls):
        cls.__thread_running = False
        cls.__messages_management.join()
        CamelotIOCommunication.stop()
        cls.__input_queue.put("kill")
        cls.__location_queue.put("kill")
        cls.__success_queue.put("kill")
        cls.__other_queue.put("kill")

            



            


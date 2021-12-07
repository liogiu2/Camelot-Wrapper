import threading
import queue
import logging
import sys
from pathlib import Path
from datetime import datetime
import time


def singleton(self, *args, **kw):
    """
    The decorator is used to make sure that only one instance of the class is created in the program.
    """
    instances = {}

    def _singleton(*args, **kw):
        if self not in instances:
            instances[self] = self(*args, **kw)
        return instances[self]
    return _singleton


@singleton
class CamelotIOCommunication:

    __queue_input = None
    __queue_output = None
    __running = True
    __input_thread = None
    __output_thread = None
    __started = False

    def start(self):
        if not self.__started:
            # logname = "logPython"+datetime.now().strftime("%d%m%Y%H%M%S")+".log"
            # Path("logs/python/").mkdir(parents=True, exist_ok=True)
            # logging.basicConfig(filename='logs/python/'+logname, filemode='w',
            #                     format='%(levelname)s:%(message)s', level=logging.DEBUG)
            self.__queue_input = queue.Queue()
            self.__queue_output = queue.Queue()
            self.__running = True
            lock = threading.Lock()
            event_obj = threading.Event()
            self.__input_thread = threading.Thread(target=self.__camelot_sender_thread, args=(
                self.__queue_output, self.__running, lock, event_obj), daemon=True)
            self.__input_thread.start()
            self.__output_thread = threading.Thread(target=self.__camelot_receiver_thread, args=(
                self.__queue_input, self.__running, lock, event_obj), daemon=True)
            self.__output_thread.start()
            self.__started = True

    def __camelot_sender_thread(self, queue: queue.Queue, is_running: bool, lock: threading.Lock, event_obj: threading.Event):
        """
        Thread method that controls the sending of messages to the standard input where Camelot is listening for inputs.
        It uses locks to ensure that the standard input / output is not used by two threads at the same time.
        It uses an event to notify the thread that a message has been received from the standard input so the operation on the standard output can be performed.

        Parameters
        ----------
        queue : queue.Queue; the queue used to get the messages to sent over the standard input
        is_running : bool; the flag used to stop the thread
        lock : threading.Lock; the lock used to ensure that the standard input / output is not used by two threads at the same time
        event_obj : threading.Event; the event used to notify the thread that a message has been received from the standard input so the operation on the standard output can be performed.
        """
        logging.debug("__camelot_sender_thread: Starting")
        while(is_running):
            event_obj.clear()

            logging.debug("__camelot_sender_thread: Trying to get message from queue")
            message = queue.get()
            logging.debug("__camelot_sender_thread: Received from queue: %s" % (message))
            if message == "kill":
                is_running = False
                break
            if message != "%PASS%":
                self.__standard_IO_operations(message, 0, lock)
                logging.debug("__camelot_sender_thread: sent to standard output")

            event_obj.set()

    def __camelot_receiver_thread(self, queue: queue.Queue, is_running: bool, lock: threading.Lock, event_obj: threading.Event):
        """
        Thread method that controls the receiving of messages from the standard output where Camelot is sending messages.
        It uses locks to ensure that the standard input / output is not used by two threads at the same time.
        It uses an event to notify the thread that a message has been sent to the standard output so the operation on the standard input can be performed.
        The event is used to ensure that the thread is not blocking the standard output when waiting for a message from Camelot. It has a timeout of 0.1 seconds.

        Parameters
        ----------
        queue : queue.Queue; the queue used to put the messages received from the standard output
        is_running : bool; the flag used to stop the thread
        lock : threading.Lock; the lock used to ensure that the standard input / output is not used by two threads at the same time
        event_obj : threading.Event; the event used to notify the thread that a message has been sent to the standard output so the operation on the standard input can be performed.
        """
        logging.debug("__camelot_receiver_thread: Starting")
        while(is_running):
            event_obj.wait(timeout=0.1)
            logging.debug("__camelot_receiver_thread: Trying to get message from standard input")
            message = self.__standard_IO_operations(None, 1, lock)
            if message == None:
                logging.debug("__camelot_receiver_thread: No message received")
                time.sleep(0.1)
                continue
            logging.debug("__camelot_receiver_thread: Received from standard input: %s" % (message))
            queue.put(message)
            logging.debug("__camelot_receiver_thread: added to the queue")
            if message == "input Quit":
                is_running = False

    def __standard_IO_operations(self, message: str, mode: int, lock: threading.Lock) -> str:
        """
        Method used to send and receive messages to the standard input or output. 
        It uses locks to ensure that the standard input or output is not used by two threads at the same time.
        mode = 0 -> input;
        mode = 1 -> output;
        return: the message received from the standard input or output or None if the mode is not valid or OK 
        if the message was sent to the standard output correctly.
        """
        lock.acquire()
        logging.debug("__standard_IO_operations: Lock acquired by %s" % ("Input" if mode == 0 else "Output"))
        return_message = None
        if mode == 0:
            if message == None:
                return None
            print(message)
            logging.debug("__standard_IO_operations: Printing message: " + message)
            return_message = "OK"
        elif mode == 1:
            return_message = input()
            return_message = return_message.strip()
            logging.debug("__standard_IO_operations: Received message: " + return_message)
        lock.release()
        logging.debug("__standard_IO_operations: Lock released")
        return return_message

    def print_action(self, text):
        """
        This method is called to add a new message to the queue to be printed over the standard output.

        Parameters
        ----------
        text : str; the message to be printed.
        """
        self.__queue_output.put(text)

    def get_message(self) -> str:
        """
        This method is called to get a message from the input queue.
        """
        message = ""
        while message == "":
            try:
                message = self.__queue_input.get()
                logging.debug("Giving message to main thread: " + message)
            except queue.Empty:
                logging.debug("Timeout, try sending message")
                self.__queue_output.put("timeout")
            if message == "kill" or message == "input Quit":
                logging.debug(
                    "Initiating closing procedures.")
                self.stop()

        return message

    def stop(self):
        """
        This method is called to stop the threads.
        """
        logging.debug("Stop Called")
        self.__running = False
        self.__input_thread.join()
        self.__output_thread.join()
        sys.exit()

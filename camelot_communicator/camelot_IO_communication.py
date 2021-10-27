import threading
import queue
import logging
import socket
import sys

def singleton(self, *args, **kw):
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
            logging.basicConfig(filename='app.log', filemode='w', format='%(levelname)s:%(message)s', level=logging.DEBUG)
            self.__queue_input = queue.Queue()
            self.__queue_output = queue.Queue()
            self.__running = True
            self.__input_thread = threading.Thread(target=self.__socket_reading , args =(self.__queue_input, self.__running, ), daemon=True)
            self.__input_thread.start()
            self.__output_thread = threading.Thread(target=self.__socket_writing , args =(self.__queue_output, self.__running, ), daemon=True)
            self.__output_thread.start()
            self.__started = True


    def __socket_reading(self, queue_input : queue.Queue, is_running : bool):
        HOST = "localhost"
        PORT = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((HOST, PORT))
        except socket.error as err:
            pass
        s.listen(10)
        conn, addr = s.accept()
        while is_running:
            data = conn.recv(1024)
            logging.debug("Received: %s"%(data))
            queue_input.put(data.decode("utf-8"))
            logging.debug("added to the queue")
        s.close()
    
    def __socket_writing(self, queue_output : queue.Queue, is_running : bool):
        HOST = "localhost"
        PORT = 9998
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((HOST, PORT))
        except socket.error as err:
            pass
        s.listen(10)
        conn, addr = s.accept()
        while is_running:
            data = queue_output.get()
            if data == "kill":
                break
            logging.debug("sending: %s"%(data))
            conn.send(bytes(data+"\r\n",'UTF-8'))
            logging.debug("Data Sent")
        s.close()

            
    def print_action(self, text):
        self.__queue_output.put(text)


    def get_message(self) -> str:
        message = ""
        while message == "":
            try:
                logging.debug("Trying getting message from main input queue")
                message = self.__queue_input.get(timeout=10)
                logging.debug("Giving message to main thread: "+ message)
            except queue.Empty:
                if self.__input_thread.is_alive():
                    logging.debug("Input thread alive")
                else:
                    logging.debug("Input thread not alive")
                    self.__queue_output.put("kill")
                    logging.debug("Adding kill to output queue")
                if self.__output_thread.is_alive():
                    logging.debug("Output thread alive")
                else:
                    logging.debug("Output thread not alive")
                message = "timeout"
                

        return message

    def stop(self):
        logging.debug("Stop Called")
        self.__running = False
        self.__input_thread.join()
        self.__output_thread.join()
    




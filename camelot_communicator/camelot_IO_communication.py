import threading
import queue
import logging
import socket
import sys
from pathlib import Path
from datetime import datetime
from multiprocessing.connection import Listener

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
            logname = "logPython"+datetime.now().strftime("%d%m%Y%H%M%S")+".log"
            Path("logs/python/").mkdir(parents=True, exist_ok=True)
            logging.basicConfig(filename='logs/python/'+logname, filemode='w', format='%(levelname)s:%(message)s', level=logging.DEBUG)
            self.__queue_input = queue.Queue()
            self.__queue_output = queue.Queue()
            self.__running = True
            self.__input_thread = threading.Thread(target=self.__socket_reading_multi , args =(self.__queue_input, self.__running, ), daemon=True)
            self.__input_thread.start()
            self.__output_thread = threading.Thread(target=self.__socket_writing_no_server , args =(self.__queue_output, self.__running, ), daemon=True)
            self.__output_thread.start()
            self.__started = True


    def __socket_reading(self, queue_input : queue.Queue, is_running : bool):
        HOST = "localhost"
        PORT = 9999
        logging.debug("socket_reading: started")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("socket_reading: socket created")

        try:
            s.bind((HOST, PORT))
            logging.debug("socket_reading: socket bind succeded")
        except socket.error as err:
            logging.debug("socket_reading: Error in reading socket connection: %s"%(err))
        try:
            s.listen(10)
            logging.debug("socket_reading: listen")

            conn, addr = s.accept()
            logging.debug("socket_reading: accept")

        except socket.error as err:
            logging.debug("socket_reading: error %s"%(err))
        logging.debug("socket_reading: Starting receiving socket messages.")

        while is_running:
            data = conn.recv(1024)
            logging.debug("socket_reading: received data: %s"%(data))
            message = data.decode('UTF-8').strip()[2:]
            logging.debug("socket_reading: Received: %s"%(message))
            queue_input.put(message)
            logging.debug("socket_reading: added to the queue")
            if message == "kill":
                logging.debug("Received kill message from Java. Initiating closing procedures.")
                is_running = False
                self.stop()
        s.close()

    def __socket_reading_no_server(self, queue_input : queue.Queue, is_running : bool):
        HOST = "localhost"
        PORT = 9999
        logging.debug("socket_reading: started")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("socket_reading: socket created")
        s.connect((HOST, PORT))

        while is_running:
            data = s.recv(16)
            logging.debug("socket_reading: received data: %s"%(data.decode()))
            message_size = int(data.decode())
            logging.debug("socket_reading: message size: %i"%(message_size))
            data = s.recv(min((message_size if message_size % 2 == 0 else message_size+1), 1024))
            # logging.debug("socket_reading: received data: %s"%(data))
            message = data.decode('UTF-8').strip()#[2:]
            logging.debug("socket_reading: Received: %s"%(message))
            queue_input.put(message)
            logging.debug("socket_reading: added to the queue")
            if message == "kill":
                logging.debug("Received kill message from Java. Initiating closing procedures.")
                is_running = False
                self.stop()
        s.close()
    
    def __socket_reading_multi(self, queue_input : queue.Queue, is_running : bool):
        PORT = 9999
        listener = Listener(address=('0.0.0.0', PORT), family='AF_INET', authkey=None)
        with listener.accept() as conn:
            while is_running:
                data = conn.recv_bytes().decode().strip()
                logging.debug("socket_reading: Received: %s"%(data))
                queue_input.put(data)
                logging.debug("socket_reading: added to the queue")
                if data == "kill":
                    logging.debug("Received kill message from Java. Initiating closing procedures.")
                    is_running = False
                    self.stop()
    
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
            try:
                conn.sendall(bytes(data+"\r\n",'UTF-8'))
            except:
                logging.debug("Socket closed by Java. Initializing closing utils")
                is_running = False
                self.stop()
            logging.debug("Data Sent")
        s.close()

    def __socket_writing_no_server(self, queue_output : queue.Queue, is_running : bool):
        HOST = "localhost"
        PORT = 9998
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        while is_running:
            data = queue_output.get()
            if data == "kill":
                break
            logging.debug("sending: %s"%(data))
            try:
                s.sendall(bytes(data+"\r\n",'UTF-8'))
            except:
                logging.debug("Socket closed by Java. Initializing closing utils")
                is_running = False
                self.stop()
            logging.debug("Data Sent")
        s.close()

            
    def print_action(self, text):
        self.__queue_output.put(text)


    def get_message(self) -> str:
        message = ""
        while message == "":
            try:
                logging.debug("Trying getting message from main input queue")
                message = self.__queue_input.get()
                logging.debug("Giving message to main thread: "+ message)
            except queue.Empty:
                """ if self.__input_thread.is_alive():
                    logging.debug("Input thread alive")
                else:
                    logging.debug("Input thread not alive")
                    self.__queue_output.put("kill")
                    logging.debug("Adding kill to output queue")
                    self.stop()
                if self.__output_thread.is_alive():
                    logging.debug("Output thread alive")
                else:
                    self.__queue_output.put("kill")
                    logging.debug("Output thread not alive")
                    self.stop()
                message = "timeout" """
                logging.debug("Timeout, try sending message")
                self.__queue_output.put("timeout")
            if message == "kill" or message == "input Quit":
                logging.debug("Received kill message from Java. Initiating closing procedures.")
                self.stop()
                

        return message

    def stop(self):
        logging.debug("Stop Called")
        self.__running = False
        self.__input_thread.join()
        self.__output_thread.join()
        sys.exit()
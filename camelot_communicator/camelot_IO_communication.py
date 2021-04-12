import threading
import queue
import logging
import socket

class CamelotIOCommunication:

    __queue_input = None
    __queue_output = None
    __running = True
    __input_thread = None
    __output_thread = None

    @classmethod
    def start(cls):
        if cls.__input_thread is None:
            logging.basicConfig(filename='app.log', filemode='w', format='%(levelname)s:%(message)s', level=logging.DEBUG)
            cls.__queue_input = queue.Queue()
            cls.__queue_output = queue.Queue()
            cls.__running = True
            cls.__input_thread = threading.Thread(target=cls.__socket_reading , args =(cls.__queue_input, cls.__running, ), daemon=True)
            cls.__input_thread.start()
            cls.__output_thread = threading.Thread(target=cls.__socket_writing , args =(cls.__queue_output, cls.__running, ), daemon=True)
            cls.__output_thread.start()


    @classmethod
    def __socket_reading(cls, queue_input : queue.Queue, is_running : bool):
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
    
    @classmethod
    def __socket_writing(cls, queue_output : queue.Queue, is_running : bool):
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
            logging.debug("sending: %s"%(data))
            conn.send(bytes(data+"\r\n",'UTF-8'))
            logging.debug("Data Sent")

            
               
    
    @classmethod
    def print_action(cls, text):
        cls.__queue_output.put(text)


    @classmethod
    def get_message(cls) -> str:
        message = ""
        while message == "":
            try:
                logging.debug("Trying getting message from queue")
                message =  cls.__queue_input.get(timeout= 1)
                logging.debug("Giving message to main thread: "+ message)
            except queue.Empty:
                logging.debug("Timeout")
            logging.debug("Restarting")

        return message

    @classmethod
    def stop(cls):
        logging.debug("Stop Called")
        cls.__running = False
        cls.__input_thread.join()
    




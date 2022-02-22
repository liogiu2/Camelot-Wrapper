import os
import sys

if os.name == 'nt':
    pddl_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\EV_PDDL"
else:
    pddl_path = "/Users/giuliomori/Documents/GitHub/EV_PDDL/"

sys.path.insert(0, pddl_path)
from game_controller import GameController
import logging
import getopt
from pathlib import Path
from datetime import datetime
# from pyswip import Prolog

# prolog = Prolog()
# prolog.assertz("")
#CamelotInputManager.start()
# import debugpy

# debugpy.listen(5678)
# debugpy.wait_for_client()
#debugpy.breakpoint()
#import logging

def main(argv):
    GUI = False
    try:
        opts, args = getopt.getopt(argv,"hdGl")
    except getopt.GetoptError:
        print('Parameter not recognized')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("usage: python camelot_communicator.py <optional> -d")
            sys.exit()
        elif opt == '-d':
            import debugpy
            debugpy.listen(5678)
            debugpy.wait_for_client()
        elif opt == '-l':
            logname = "logPython"+datetime.now().strftime("%d%m%Y%H%M%S")+".log"
            Path("logs/python/").mkdir(parents=True, exist_ok=True)
            logging.basicConfig(filename='logs/python/'+logname, filemode='w', format='%(levelname)s:%(message)s', level=logging.DEBUG)
        elif opt == '-G':
            GUI = True

    gc = GameController(GUI=GUI)
    try:
        gc.start_game(True)
    except Exception as e:
        logging.exception("Main: Exception : %s" %( e ))

if __name__ == '__main__':
    main(sys.argv[1:])
    


# from camelot_input_manager import CamelotInputManager

# import time


# CamelotInputManager.start()
# time.sleep(10)

# print(CamelotInputManager.get_message())
# time.sleep(1)
# print(CamelotInputManager.get_messdsfage())
# time.sleep(1)
# print(CamelotInputManager.get_message())

# CamelotInputManager.stop()
# import socket

# HOST = "localhost"
# PORT = 9999
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     s.bind((HOST, PORT))
# except socket.error as err:
#     pass
# s.listen(10)
# conn, addr = s.accept()
# while(True):
#     conn.send(bytes("start CreatePlace(alchemyshop, AlchemyShop)"+"\r\n",'UTF-8'))
#     data = conn.recv(1024)
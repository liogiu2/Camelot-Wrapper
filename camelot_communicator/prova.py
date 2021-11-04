from game_controller import GameController
# from pyswip import Prolog

# prolog = Prolog()
# prolog.assertz("")
#CamelotInputManager.start()
# import debugpy

# debugpy.listen(5678)
# debugpy.wait_for_client()
# debugpy.breakpoint()
#import logging

gc = GameController()

gc.start_game(False)


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
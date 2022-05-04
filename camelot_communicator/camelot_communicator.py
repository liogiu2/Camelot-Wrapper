import os
import sys

if os.name == 'nt':
    pddl_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\EV_PDDL"
else:
    pddl_path = "/Users/giuliomori/Documents/GitHub/EV_PDDL/"

sys.path.insert(0, pddl_path)
import game_controller
import logging
import getopt
from pathlib import Path
from datetime import datetime

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
            logging.info("Logging started")
        elif opt == '-G':
            GUI = True

    logging.debug("Starting Camelot Communicator")
    gc = game_controller.GameController(GUI=GUI)
    logging.debug("Camelot Communicator started")
    try:
        gc.start_platform_communication()
        gc.start_game(True)
    except Exception as e:
        logging.exception("Main: Exception : %s" %( e ))

if __name__ == '__main__':
    main(sys.argv[1:])
import sys
from pathlib import Path
import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..\\..', 'EV_PDDL'))
sys.path.append("/Users/giuliomori/Documents/GitHub/EV_PDDL/")
import game_controller
import logging
import getopt
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
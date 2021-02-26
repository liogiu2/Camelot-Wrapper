from game_controller import GameController
# from pyswip import Prolog

# prolog = Prolog()
# prolog.assertz("")

# import debugpy

# debugpy.listen(5678)
# print("Waiting for debugger attach")
# debugpy.wait_for_client()
# debugpy.breakpoint()

gc = GameController()

gc.start_game(False)

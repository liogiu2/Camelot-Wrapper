from camelot_communicator import camelot_action

def test_action(capsys):
    a = camelot_action()
    a.Die("Bob")
    captured = capsys.readouterr()
    assert captured.out == "start Die(Bob)\n"

# def test_action_wait(capsys):
#     a = camelot_action()
#     r = a.Die("Bob")
#     captured = capsys.readouterr()
#     assert captured.out == "start Die(Bob)\n"
#     print("succeeded Die(Bob)")
from camelot_communicator.camelot_action import CamelotAction

def test_action(capsys):
    a = CamelotAction()
    a.action("Die", ['Bob'], False)
    captured = capsys.readouterr()
    assert captured.out == "start Die(Bob)\n"

def test_action_with_more_paramenters(capsys):
    a = CamelotAction()
    a.action("CreateItem", ['item', 'item_type'], False)
    captured = capsys.readouterr()
    assert captured.out == "start CreateItem(item, item_type)\n"

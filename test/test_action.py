from camelot_communicator.camelot_action import CamelotAction

def test_action(capsys):
    a = CamelotAction()
    a.action("Die", ['Bob'], False)
    captured = capsys.readouterr()
    assert captured.out == "start Die(Bob)\n"

def test_action_no_param(capsys):
    a = CamelotAction()
    a.action("ShowMenu", False)
    captured = capsys.readouterr()
    assert captured.out == "start ShowMenu()\n"

def test_action_with_more_paramenters(capsys):
    a = CamelotAction()
    a.action("CreateItem", ['item', 'item_type'], False)
    captured = capsys.readouterr()
    assert captured.out == "start CreateItem(item, item_type)\n"

def test_action_with_boolean(capsys):
    a = CamelotAction()
    a.action("EnableIcon", ['SwordAttack', 'Sword', 'Tom', 'Attack Tom!', True], False)
    captured = capsys.readouterr()
    assert captured.out == "start EnableIcon(\"SwordAttack\", Sword, Tom, \"Attack Tom!\", true)\n"

def test_action_optional_parameter(capsys):
    a = CamelotAction()
    a.action("EnableIcon", ['SwordAttack', 'Sword', 'Tom', True], False)
    captured = capsys.readouterr()
    assert captured.out == "start EnableIcon(\"SwordAttack\", Sword, Tom, true)\n"


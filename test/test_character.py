from camelot_communicator.character import Character

def test_character(capsys):
    test_c = Character("Bob", 'B')
    captured = capsys.readouterr()
    assert captured.out == "start CreateCharacter(Bob, B)\n" or captured.out == 'start CreateCharacter("Bob", B)\n'
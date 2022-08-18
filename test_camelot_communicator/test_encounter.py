import unittest

from camelot_wrapper.encounter import Encounter

class TestEncounter(unittest.TestCase):

    def setUp(self) -> None:
        self.json_data = {
            "name": "Prova",
            "description": "Prova",
            "metadata": {
                "type": "prova"
            },
            "preconditions": "(and (in luca City) (in bob City) (alive bob) (alive luca))",
            "instructions": [
                {
                    "type" : "PDDL",
                    "commands": [
                        "move-within-location(luca, bob)",
                        "move-within-location(luca, City.Bench)"
                    ]
                },
                {
                    "type" : "Camelot",
                    "commands": [
                        "Wave(bob)"
                    ]
                }
            ]
        }

    def test_encounter(self):
        enc = Encounter(self.json_data)
        self.assertEqual(enc.name, "Prova")
        self.assertEqual(enc.description, "Prova")
        self.assertEqual(enc.metadata["type"], "prova")
        self.assertEqual(enc.preconditions, "(and (in luca City) (in bob City) (alive bob) (alive luca))")
        i = 0
        for item in enc.get_instruction():
            if i == 0:
                self.assertEqual(item, ("PDDL", "move-within-location(luca, bob)"))
                i += 1
            elif i == 1:
                self.assertEqual(item, ("PDDL", "move-within-location(luca, City.Bench)"))
                i += 1
            else:
                self.assertEqual(item, ("Camelot", "Wave(bob)"))
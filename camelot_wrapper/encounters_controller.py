from functools import cached_property
import jsonpickle
from encounter import Encounter
from utilities import parse_json
import glob
import os

class EncountersController:

    def __init__(self):
        initial_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        if os.name == 'nt':
            filenames = [path.removeprefix("encounters\\").removesuffix(".json") for path in glob.glob('encounters/*.json')]
        else:
            filenames = [path.removeprefix("encounters/").removesuffix(".json") for path in glob.glob('encounters/*.json')]
        self.encounters = [Encounter(parse_json(filename, encounter=True)) for filename in filenames]
        os.chdir(initial_path)
    
    def find_encounter(self, encounter_name) -> Encounter:
        """
        Method used to find an encounter by name.

        Parameters:
        ----------
        encounter_name : str
            The name of the encounter to find.
        """
        for encounter in self.encounters:
            if encounter.name == encounter_name:
                return encounter
        return None
    
    @cached_property
    def get_encounters_name(self) -> list:
        """
        Method used to get the names of all the encounters.

        Returns:
        ----------
        encounters_name : list
            The names of all the encounters.
        """
        return [encounter.name for encounter in self.encounters]
    
    def get_encounters_message(self) -> str:
        """
        Method used to create the message to send to the EM with all the possible encounters.

        Returns:
        ----------
        message : str
            The message to send to the EM.
        """
        message = {
            "encounters": [encounter.get_EM_message() for encounter in self.encounters]
        }
        return jsonpickle.encode(message)
    
    def start_encounter(self, encounter_name : str):
        """
        Method used to start an encounter.

        Parameters:
        ----------
        encounter_name : str
            The name of the encounter to start.
        """
        encounter = self.find_encounter(encounter_name)
        if encounter:
            pass
        else:
            raise ValueError("Encounter not found.")
    
    
    
    
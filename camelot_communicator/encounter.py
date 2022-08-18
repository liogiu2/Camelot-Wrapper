class Encounter:
    """
    Class used to represent an encounter. 

    Attributes:
    ----------
    name : str
        The name of the encounter.
    description : str
        The description of the encounter.
    metadata : dict
        The metadata of the encounter.
    """

    def __init__(self, json_data) -> None:
        self.json_data = json_data
        self.name = json_data['name']
        self.description = json_data['description']
        self.metadata = json_data['metadata']
        self.preconditions = json_data['preconditions']
        self._instructions = json_data['instructions']
        self._instructions_sent = []
    
    
    def get_instruction(self):
        """
        Method used to get the instructions of the encounter. 
        This function is a generator that returns the instructions one by one as a tuple (instruction_type, instruction_command).

        Returns:
        ----------
        instruction : tuple
            The instruction as a tuple (instruction_type, instruction_command).
        """
        for instruction in self._instructions:
            for command in instruction["commands"]:
                return_instruction = (instruction["type"], command)
                self._instructions_sent.append(return_instruction)
                yield return_instruction
    
    def get_EM_message(self) -> str:
        """
        Method used to create a message from this encounter to be sent to the EM during the initial phase.
        """
        message = {
            "name": self.name,
            "description": self.description,
            "metadata": self.metadata,
            "preconditions": self.preconditions
        }
        return message

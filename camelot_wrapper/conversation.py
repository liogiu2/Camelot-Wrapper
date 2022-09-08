import subprocess
from yarnrunner_python import YarnRunner
import shlex
import os

class Conversation:

    def __init__(self, name : str, filename : str) -> None:
        self.name = name
        command = "ysc compile "+filename+" -o output -n "+ filename.replace(".yarn", ".yarnc") +" -t " + filename.replace(".yarn", ".csv")
        subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
        self._running = False
        self._prepared = False
        self.runner = None
        self.player_name = None
        self.npc_name = None
    
    def prepare(self, player_name : str, npc_name : str):
        """
        This method is used to prepare the conversation for execution.

        Parameters
        ----------
        player_name : str
            The name of the player.
        npc_name : str
            The name of the npc.
        """
        with open(os.path.join(os.path.dirname(__file__),'narrative/output/'+self.name+'.yarnc'), 'rb') as story_f:
            with open(os.path.join(os.path.dirname(__file__),'narrative/output/'+self.name+'.csv'), 'r') as strings_f:
                self.runner = YarnRunner(story_f, strings_f, autostart=False)

        def update_player_model(fighter, method_actor, storyteller, tactician, power_gamer):
            print(fighter, method_actor, storyteller, tactician, power_gamer)
        
        self.runner.add_command_handler("update_player_model", update_player_model)

        self.player_name = player_name
        self.npc_name = npc_name
        self._prepared = True
    
    def is_running(self) -> bool:
        """
        This method is used to check if the conversation is running.
        It will return True if the conversation is running and False otherwise.
        """
        return self._running
    
    def run_one_line_conversation(self) -> str:
        """
        This method is used to run a conversation. It will run the conversation and return the lines printed from the story.
        After this method is called either the conversation encountered a choice point or it finished.
        Check if the conversation is finished by calling the is_finished method.
        Check if the conversation has available choices by calling the get_choices method.
        """
        if not self._prepared:
            raise Exception("Conversation is not prepared.")
        self.runner.resume()
        if self.runner.has_line():
            return self.runner.get_line()
        else:
            return None
    
    def has_line(self):
        """
        This method is used to check if the conversation has a line to print.
        It will return True if the conversation has a line to print and False otherwise.
        """
        if not self._prepared:
            raise Exception("Conversation is not prepared.")
        return self.runner.has_line()
    
    def run_conversation(self) -> list:
        """
        This method is used to run a conversation.
        It will run the conversation and return the lines printed from the story.
        After this method is called either the conversation encountered a choice point or it finished.
        Check if the conversation is finished by calling the is_finished method.
        Check if the conversation has available choices by calling the get_choices method.
        """
        if not self._prepared:
            raise Exception("Conversation is not prepared.")

        self.runner.resume()
        return self.runner.get_lines()
    
    def is_finished(self):
        """
        This method is used to check if the conversation is finished.
        It will return True if the conversation is finished and False otherwise.
        """
        if not self._prepared:
            raise Exception("Conversation is not prepared.")
        if self.runner.finished:
            self._running = False
            self._prepared = False
        return self.runner.finished
    
    def get_choices(self):
        """
        This method is used to get the available choices of the conversation.
        It will return a list of choices.
        Each Choice object has an index and a text.
        The index is the index of the choice in the list of choices.
        The text is the text of the choice.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to get the choices from.
        """
        if not self._prepared:
            raise Exception("Conversation is not prepared.")
        return self.runner.get_choices()
    
    def choose(self, choice_index : int):
        """
        This method is used to make a choice in the conversation.
        It will make the choice with the index specified in the choice_index parameter.
        After this method is called you can continue the conversation using the run_conversation method.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to make the choice in.
        choice_index : int
            The index of the choice to make.
        """
        if not self._prepared:
            raise Exception("Conversation is not prepared.")
        self.runner.choose(choice_index)
    
    def get_camelot_setdialog_string(self) -> list:
        """
        This method is used to get the string that can be used to set the dialog of the conversation.
        It will return the string that can be used to set the dialog of the conversation.
        """
        if not self._prepared:
            raise Exception("Conversation is not prepared.")
        
        if not self._running:
            self._running = True
        return_list = []
        line_of_dialog = self.run_one_line_conversation()
        return_list.append(self._prepare_line(line_of_dialog))
        if self.has_line():
            return return_list
        else:
            for choice in self.get_choices():
                choice_string = " "
                text = self._prepare_line(choice['text'])
                choice_string += "[{}|{}] ".format(choice['index'], text)
                return_list.append(choice_string)
            return return_list


    def _prepare_line(self, line : str) -> str:
        """
        This method is used to prepare a line of dialog.
        It will replace the player name and the companion name with the names specified in the prepare method.
        It will also add the Camelot SetDialog command to the beginning of the line.

        Parameters
        ----------
        line : str
            The line to prepare.
        """
        return line.replace("Player", self.player_name).replace("Companion", self.npc_name).replace("<FirstName>", self.player_name)


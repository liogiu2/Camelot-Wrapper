from cProfile import run
from yarnrunner_python import YarnRunner
import glob
import subprocess
import os
import shlex
from camelot_action import CamelotAction

class ConversationController:

    def __init__(self):
        self.narrative_filenames = [path.removeprefix("narrative/") for path in glob.glob('narrative/*.yarn')]
        os.chdir("narrative")
        for filename in self.narrative_filenames:
            command = "ysc compile "+filename+" -o output -n "+ filename.replace(".yarn", ".yarnc") +" -t " + filename.replace(".yarn", ".csv")
            subprocess.run(shlex.split(command), stdout=subprocess.PIPE)
        
        self.runners = {}
        self._camelot_action = CamelotAction()

    def prepare_conversation(self, conversation_name : str) -> list:
        """
        This method is used to prepare a conversation to be run. It inizialize the Yarn runner and will populate the runners dictionary.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to be run.
        """
        with open('output/'+conversation_name+'.yarnc', 'rb') as story_f:
            with open('output/'+conversation_name+'.csv', 'r') as strings_f:
                runner = YarnRunner(story_f, strings_f, autostart=False)

        def update_player_model(fighter, method_actor, storyteller, tactician, power_gamer):
            print(fighter, method_actor, storyteller, tactician, power_gamer)
        
        runner.add_command_handler("update_player_model", update_player_model)

        self.runners[conversation_name] = runner
    
    def run_one_line_conversation(self, conversation_name : str) -> str:
        """
        This method is used to run a conversation. It will run the conversation and return the lines printed from the story.
        After this method is called either the conversation encountered a choice point or it finished.
        Check if the conversation is finished by calling the is_finished method.
        Check if the conversation has available choices by calling the get_choices method.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to be run.
        """
        if conversation_name not in self.runners:
            raise Exception("Conversation not prepared")
        runner = self.runners[conversation_name]
        runner.resume()
        if runner.has_line():
            return runner.get_line()
        else:
            return None
    
    def run_conversation(self, conversation_name : str):
        """
        This method is used to run a conversation.
        It will run the conversation and return the lines printed from the story.
        After this method is called either the conversation encountered a choice point or it finished.
        Check if the conversation is finished by calling the is_finished method.
        Check if the conversation has available choices by calling the get_choices method.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to be run.
        """
        if conversation_name not in self.runners:
            raise Exception("Conversation not prepared")
        runner = self.runners[conversation_name]
        runner.resume()
        return runner.get_lines()
    
    def is_finished(self, conversation_name : str):
        """
        This method is used to check if the conversation is finished.
        It will return True if the conversation is finished and False otherwise.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to check if ended.
        """
        if conversation_name not in self.runners:
            raise Exception("Conversation not prepared")
        return self.runners[conversation_name].finished
    
    def get_choices(self, conversation_name : str):
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
        if conversation_name not in self.runners:
            raise Exception("Conversation not prepared")
        return self.runners[conversation_name].get_choices()
    
    def choose(self, conversation_name : str, choice_index : int):
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
        if conversation_name not in self.runners:
            raise Exception("Conversation not prepared")
        self.runners[conversation_name].choose(choice_index)

    def start_camelot_conversation(self, conversation_name : str, player_name: str, npc_name : str):
        """
        This method is used to prepare Camelot for a conversation.
        It will create and send all the camelot commands to prepare the execution of the conversation.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to prepare Camelot for.
        """
        if conversation_name not in self.runners:
            raise Exception("Conversation not prepared")
        
        self._camelot_action.action("SetLeft", [player_name], False)
        self._camelot_action.action("SetRight", [npc_name], False)
        self._prepare_and_send_camelot_setdialog_command(conversation_name, npc_name)
        self._camelot_action.action("ShowDialog", [], False)

        
    def _prepare_and_send_camelot_setdialog_command(self, conversation_name : str, npc_name : str):
        runner = self.runners[conversation_name]
        line_of_dialog = self.run_one_line_conversation(conversation_name).replace("Companion", npc_name)
        if runner.has_line():
            self._camelot_action.action("SetDialog", [line_of_dialog], False)
        else:
            choice_string = " "
            for choice in self.get_choices(conversation_name):
                text = str(choice['text']).replace("Player", "Me")
                choice_string += "[{}|{}] ".format(choice['index'], text)
            self._camelot_action.action("SetDialog", [line_of_dialog], False)
        
        

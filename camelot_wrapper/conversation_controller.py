from yarnrunner_python import YarnRunner
import glob
import subprocess
import os
import shlex
try:
    from camelot_action import CamelotAction
    from conversation import Conversation
except (ModuleNotFoundError, ImportError):
    from .camelot_action import CamelotAction
    from .conversation import Conversation
import debugpy


class ConversationController:

    def __init__(self):
        initial_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))
        self.narrative_filenames = [path.removeprefix("narrative/") for path in glob.glob('narrative/*.yarn')]
        self.narrative_names = [filename.replace(".yarn", "") for filename in self.narrative_filenames]
        os.chdir("narrative")
        self.conversations = {}
        for name in self.narrative_names:
            self.conversations[name] = Conversation(name, name + ".yarn")
        os.chdir(initial_path)
        
        self.runners = {}
        self._camelot_action = CamelotAction()
    
    def get_running_conversation(self) -> Conversation:
        """
        This method is used to get the conversation that is currently running.
        """
        for key in self.conversations.keys():
            if self.conversations[key].is_running():
                return self.conversations[key]
    
    def check_conversation_exists(self, conversation_name : str):
        """
        This method is used to check if a conversation exists.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to check if exists.
        """
        return conversation_name in self.narrative_names

    def start_camelot_conversation(self, conversation_name : str, player_name: str, npc_name : str):
        """
        This method is used to prepare Camelot for a conversation.
        It will create and send all the camelot commands to prepare the execution of the conversation.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to prepare Camelot for.
        """
        self.conversations[conversation_name].prepare(player_name, npc_name)
        
        self._camelot_action.action("SetLeft", [player_name], True)
        self._camelot_action.action("SetRight", [npc_name], True)
        self._prepare_and_send_camelot_setdialog_command(conversation_name)
        self._camelot_action.action("ShowDialog", [], True)
    
    def continue_conversation_with_choice(self, choice : int):
        """
        This method is used to continue a conversation with a choice.
        It will create and send all the camelot commands to continue the execution of the conversation.

        Parameters
        ----------
        choice : int
            The choice to continue the conversation with.
        """
        self._camelot_action.action("ClearDialog", [], False)
        running_conversation = self.get_running_conversation()
        running_conversation.choose(choice)
        self._prepare_and_send_camelot_setdialog_command(running_conversation.name)

        
    def _prepare_and_send_camelot_setdialog_command(self, conversation_name : str):
        """
        This method is used to prepare and send the camelot setdialog command.
        It will prepare the camelot setdialog command and send it to Camelot.

        Parameters
        ----------
        conversation_name : str
            The name of the conversation to prepare the camelot setdialog command for.
        """
        # debugpy.listen(5678)
        # debugpy.wait_for_client()
        # debugpy.breakpoint()
        lines_of_dialog = self.conversations[conversation_name].get_camelot_setdialog_string()
        for line_of_dialog in lines_of_dialog:
            self._camelot_action.action("SetDialog", [line_of_dialog], False)
        
        

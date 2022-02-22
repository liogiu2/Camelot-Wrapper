import debugpy
import logging
import queue
from camelot_IO_communication import CamelotIOCommunication
from utilities import singleton, parse_json, replace_all, str2bool
from camelot_input_multiplexer import CamelotInputMultiplexer
from ev_pddl.action import Action
#TODO: check if parameters in action are what camelot expects

@singleton
class CamelotAction:
    """
    This class is used to prepare the messages to be sent to Camelot.
    """

    def __init__(self):
        self.camelot_input_multiplex = CamelotInputMultiplexer()
        self.camelot_input_multiplex.start()
        self.camelot_IO_communication = CamelotIOCommunication()
        self.success_messages = queue.Queue()
        self.debug = False
        self.json_actionlist = parse_json("Actionlist")
        self.json_actions_to_camelot = parse_json("pddl_actions_to_camelot")

    def check_for_success(self, command, action_name):
        """
        Waits for success or fail response from Camelot.

        Parameters
        ----------
        command : str
            The command that was sent to Camelot.
        action_name : str
            The name of the action.
        """

        # Keep getting responses until the success of fail the given command is received
        while True:

            # Get response from Camelot
            received = self.camelot_input_multiplex.get_success_message(command, action_name)
            
            # Return True if success response, else false for fail response
            if received != None:
                logging.debug("Camelot output: %s" % received)
                if received == 'succeeded ' + command:
                    self.success_messages.put(received)
                    logging.debug("Camelot_Action: Success message added to queue")
                    return True
                elif received.startswith('failed ' + command) or received.startswith('error ' + command):
                    return False
                elif received == False:
                    # Found error from Camelot that belongs to this action
                    return False


    def action(self, action_name, parameters = [] , wait=True):
        """
        Format an action for interpretation by Camelot and sends it to Camelot.

        Parameters
        ----------
        action_name : str
            The name of the action.
        parameters : list
            The parameters of the action.
        wait : bool
            If true, wait for success or fail response from Camelot. If False, do not wait.
        
        Returns
        -------
        bool
            True if success, else False.
        """
        if(not any(d['name'] == action_name for d in self.json_actionlist)):
            raise KeyError("Action name {:} does not exist. The parameter Action Name is case sensitive.".format(action_name))
        if(type(parameters) == bool):
            wait = parameters
            parameters = []

        action_data = [d for d in self.json_actionlist if d['name'] == action_name][0]
        
        if(len(parameters) > 0):
            self._check_action_parameters(action_data, parameters)

        # Format commands
        # This method assumes that the parameters are checked and ok to be printed
        command = self._generate_camelot_string(action_name, parameters, action_data)
        
        self.send_camelot_instruction('start ' + command)

        if wait==True:
            # Call function to check for its success
            return self.check_for_success(command, action_name)
        else:
            return True
    
    def send_camelot_instruction(self, instruction):
        """
        This method is used to send a command to Camelot without performing any checks.

        Parameters
        ----------
        instruction : str
            The instruction to send to Camelot.
        """
        if instruction.startswith('start '):
            self.camelot_IO_communication.print_action(instruction)
        else:
            self.camelot_IO_communication.print_action('start ' + instruction)

    
    def _generate_camelot_string(self, action_name, parameters, action_data):
        """
        This method is used to generate the string to be sent to Camelot.

        Parameters
        ----------
        action_name : str
            The name of the action.
        parameters : list
            The parameters of the action.
        action_data : dict
            The data of the action.
        """
        command = action_name + "("
        index = 0
        for item in parameters:
            if(type(item) == str and action_data['param'][index]['type'] == "String"):
                command += '"' + item + '"'
            elif(type(item) == bool):
                command += str(item).lower()
            else:
                command += item
            command += ', '
            index += 1
        if(index > 0):
            command = command[:-2]
        command += ")"
        return command
    
    def _check_action_parameters(self, action_data, parameters):
        nparam = 0
        for item in action_data['param']:
            if(item['default'] == 'REQUIRED'):
                nparam += 1
        
        if(len(parameters) < nparam):
            raise KeyError("Number of parameters less then REQUIRED ones.")
    
    def generate_camelot_action_parameters_from_action(self, action: Action):
        """
        This method is used to generate the commands to be sent to Camelot from a PDDL action.

        Parameters
        ----------
        action : Action
            The action used to generate the camelot commands.
        
        Returns
        -------
        list
            A list of dictionaries that are the parameters that can be used to generate Camelot Actions.
        """
        # openfurniture(bob, alchemyshop.Chest, alchemyshop.Chest)
        camelot_commands = []
        if action.name not in self.json_actions_to_camelot.keys():
            return None
        command_data = self.json_actions_to_camelot.get(action.name).get("commands")
        parameters = {k : v.name for (k,v) in action.parameters.items()}
        for command in command_data:
            command_dict = {
                "action_name": command["action_name"],
                "action_args": [],
                "wait": str2bool(command["wait"])
            }
            for item in command["action_args"]:
                command_dict["action_args"].append(replace_all(item, parameters))
            camelot_commands.append(command_dict)
        return camelot_commands
    
    def actions(self, action_parameters):
        """
        This method is used to create and send actions to camelot starting from a list of dictionaries representing the parameters of the action.

        Parameters
        ----------
        action_parameters : list
            The list of dictionaries that represent the parameters of the action.
        
        Returns
        -------
        bool
            True if all the actions succedeed, else False.
        """
        result = True
        for action_parameter in action_parameters:
            action_name = action_parameter["action_name"]
            action_args = action_parameter["action_args"]
            wait = action_parameter["wait"]
            result = result and self.action(action_name, action_args, wait)
        return result

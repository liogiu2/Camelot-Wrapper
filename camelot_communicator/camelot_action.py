import json
import pandas as pd
import importlib.resources as pkg_resources
from . import json_data
"""
Inputs: Json file with the description of each action
Outputs: 
"""
class CamelotAction:

    def __init__(self):
        with pkg_resources.open_text(json_data, 'Actionlist.json') as json_file:
            self.json_data_r = json.load(json_file)
            self.df = pd.DataFrame(data=self.json_data_r)

    
    '''
    Purpose: Waits for success or fail response from Camelot
    Inputs: command that was sent to Camelot
    Outputs: True for success, False for failure
    '''

    def check_for_success(self,command):

        # Keep getting responses until the success of fail the given command is received
        while True:

            # Get response from Camelot
            received = input()

            # Return True if success response, else false for fail response
            if received == 'succeeded ' + command:
                return True
            elif received.startswith('failed ' + command):
                return False
            elif received.startswith('error ' + command):
                return False

    '''
    Purpose: Format an action for interpretation by Camelot
    Inputs: Action to be sent to Camelot
    Outputs: True for success, False for failure
    '''
    def action(self, action_name, parameters = [] , wait=True):
        if(action_name not in self.df.name.values):
            raise KeyError("Action name {:} does not exist. The parameter Action Name is case sensitive.".format(action_name))

        row = self.df.loc[self.df['name'] == action_name]

        nparam = 0
        for item in row['param'].iloc[0]:
            if(item['default'] == 'REQUIRED'):
                nparam += 1
        
        
        if(len(parameters) < nparam):
            raise KeyError("Number of parameters less then REQUIRED ones.")

        # Format commands
        command = action_name + "("
        for item in parameters:
            command += item
            command += ', '
        command = command[:-2]
        command += ")"

        print('start ' + command)
        if wait==True:
            # Call function to check for its success
            return self.check_for_success(command)
        else:
            return True;

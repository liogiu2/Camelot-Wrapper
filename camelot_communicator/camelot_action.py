import json
import pandas as pd
"""
Purpose: Dynamic class that creates methods for each action avalailable in camelot
Inputs: Json file with the description of each action
Outputs: A method for each action
"""
class camelot_action:

    json_data = []
    df = pd.DataFrame()

    def __init__(self):
        with open('camelot_communicator/json/Actionlist.json') as json_file:
            self.json_data = json.load(json_file)
            self.df = pd.DataFrame(data=self.json_data)

    def _create_doc_text(self, attrname):
        row_doc = self.df.loc[self.df['name'] == attrname]
        doc_text = """
            Method Name: 
                {:}
            Description:
                {:}

            Args:
                """.format(attrname,row_doc['desc'].iloc[0])
        for item in row_doc['param'].iloc[0]:
            doc_text += """{:} ({:}): {:} (default = {:})
                """.format(item['name'],item['type'], item['desc'], item['default'])
        return doc_text

    def _create_text_action(self, attrname, args):
        text = attrname + "(" 
        for value in args:
            text += value + ","
        text = text[:-1]
        text += ")"
        return text

    """
    Purpose: Create a method for each action in the Json file
    Operation: I use a workaround of the python programming. 
    __getattr__ is a method called by python when the class doesn't recognize a method called.
    So, every time the programmer calls the class with a method that is not recognized, we create a function that uses the name of the
    method that is not recognized and it searches it n the json file with all the camelot actions. If an action with the same name
    exists, then we create the method with some general checks on the action.
    Outputs: The input for camelot
    """

    def __getattr__(self,attrname):

        def _camelot_action_method(*args, wait = False):
            row = self.df.loc[self.df['name'] == attrname]
            nparam = 0
            for item in row['param'].iloc[0]:
                if(item['default'] == 'REQUIRED'):
                    nparam += 1

            if(len(args) < nparam):
                raise KeyError("Number of parameter less then REQUIRED ones.")
            
            text = self._create_text_action(attrname, args)
            result = self.action(text, False)
            return result

        if attrname in self.df['name'].tolist():
            _camelot_action_method.__doc__ = self._create_doc_text(attrname = attrname)
            return _camelot_action_method
        else:
            raise NameError("The generator didn't recognize the method name {:}.".format(attrname))
    
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
    def action(self,command, wait=True):
        # Format commands
        print('start ' + command)
        if wait==True:
            # Call function to check for its success
            return self.check_for_success(command)
        else:
            return True;

#import pandas as pd
import json
import importlib.resources as pkg_resources
from camelot_action import CamelotAction
from camelot_world_state import CamelotWorldState
import json_data

class Character:

    def __init__(self, name, body_type = 'A'):
        with pkg_resources.open_text(json_data, 'characterlist.json') as json_file:
            self.json_data_r = json.load(json_file)
            #self.df = pd.DataFrame(data=self.json_data_r)

        self.c_action = CamelotAction()
        self.name = name

        #Check if body type does not exist
        if(not any(d['name'] == body_type for d in self.json_data_r['body_type'])):
            raise KeyError("Body type not recognized.")

        self.body_type = body_type

        if(self.c_action.action("CreateCharacter", [name, body_type], False)):
            CamelotWorldState.character_list.append(self)
        
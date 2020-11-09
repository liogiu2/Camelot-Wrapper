import json
import pandas as pd
with open('json_data/Actionlist.json') as json_file:
    json_data_r = json.load(json_file)
action_name = 'AddToList'
row = [d for d in json_data_r if d['name'] == action_name][0]

nparam = 0
for item in row['param']:
    if(item['default'] == 'REQUIRED'):
        nparam += 1

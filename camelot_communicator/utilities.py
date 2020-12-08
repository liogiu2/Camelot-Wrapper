import json
import importlib.resources as pkg_resources
import json_data

def parse_json(jsonfile):
    with pkg_resources.open_text(json_data, jsonfile+'.json') as json_file:
        json_data_parsed = json.load(json_file)
    return json_data_parsed
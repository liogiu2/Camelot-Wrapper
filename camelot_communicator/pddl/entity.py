from pddl.types import Type
from utilities import parse_json


class Entity:

    def __init__(self, name, type_e, problem = None):
        name, type_e = self._entity_check(name, type_e, problem)
        self.name = name
        if type(type_e) is not Type:
            raise Exception('Expected Type got %s'%(type(type_e)))
        self.type = type_e

    def __str__(self) -> str:
        return "%s (%s)"%(self.name, self.type.name)

    def _entity_check(self, name, type_e, problem):
        l_extention = type_e.get_list_extensions()
        if 'position' in l_extention:
            n = name.split('.')
            if len(n) == 2:
                json_parsed = parse_json('places')
                for item in json_parsed:
                    if item['name'].lower() == n[0].lower():
                        for comp in item['room_components']:
                            if comp['name'].lower() == n[1].lower():
                                n[1] = comp['name']
                                break
                        break
                name = n[0] + '.' + n[1]
                
                
        return (name, type_e)

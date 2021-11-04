from pddl.problem import Problem
from pddl.domain import Domain
from pddl.predicate import Predicate
from pddl.relation_value import RelationValue

class Relation:

    def __init__(self, predicate, entities, value, domain = None, problem = None):
        if type(value) is not RelationValue:
            raise Exception('Value must be enum RelationValue')
        if type(predicate) is not Predicate:
            raise Exception('predicate must be class Predicate')
        if domain is not None and problem is not None:
            if type(domain) is not Domain:
                raise Exception('Domain must be class Domain')
            if type(problem) is not Problem:
                raise Exception('Problem must be class Problem')
            if not self.is_valid_relation(predicate, entities, domain, problem):
                raise Exception('Relation is not valid')
            self.domain = domain
            self.problem = problem
        self.predicate = predicate
        self.entities = entities
        self.value = value
        

    def is_valid_relation(self, predicate, entities, domain, problem):
        #check if entities exist
        for item in entities:
            if problem.find_objects(item.name) is None:
                raise Exception('Object %s not found in the list of Objects in the Problem'%(item.name))
        #check if predicate exist
        if domain.find_predicate(predicate.name) is None:
            raise Exception('Cannot find predicate %s in domain %s'%(predicate.name, domain.domain_name))
        #check that type of entities and predicate fit
        check_entity = entities.copy()
        for item in predicate.arguments:
            entity_found = self._find_entity_with_type(check_entity, item.name)
            if entity_found is None:
                raise Exception('Entity %s in relation not found'%(item.name))
            check_entity.remove(entity_found)
        if len(check_entity) > 0:
            raise Exception('More objects written with relation %s'%(predicate.name))
        return True

    
    def _find_entity_with_type(self, entities, type):
        for item in entities:
            extension = item.type.get_list_extensions()
            if type in extension:
                return item
        return None

    def modify_value(self, value: RelationValue):
        if self.value != value: 
            self.value = value
    
    def __str__(self) -> str:
        string = self.predicate.name + '('
        for item in self.entities:
            string += item.name + ', '
        string = string[:-2] +')'
        return string
    
    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and 
            self.value == other.value and 
            self.predicate == other.predicate and 
            all(map(lambda x, y: x == y, self.entities, other.entities))
        )

    def equals_exclude_value(self, other):
        return (
            self.__class__ == other.__class__ and 
            self.predicate == other.predicate and 
            all(map(lambda x, y: x == y, self.entities, other.entities))
        )



from pddl.action_definition import ActionDefinition, ActionProposition
from pddl.predicate import Predicate
from pddl.relation import Relation, RelationValue

class Action:

    def __init__(self, action_definition, parameters):
        self._action_definition = action_definition
        self._parameters = {}
        self._preconditions = None
        self._effects = None
        self.create_action(self._action_definition, parameters)
    
    def create_action(self, action_definition: ActionDefinition, parameters):
        """A method that is used to create an action from an action definition
        
        Parameters
        ----------
        action_definition : ActionDefinition
            the model of the action
        parameters : list
            the parameters that need to be sobstituted from the action_definition
        """
        #Cheking action_definition parameters with dict of parameters passed in the method to be sobstitute in the action
        for param in action_definition.parameters:
            if param.name in parameters.keys():
                if parameters[param.name] in self._parameters.values():
                    raise ValueError("%s already esists in the list of parameters"%(parameters[param.name]))
                self._parameters[param.name] = parameters[param.name]
            else:
                raise KeyError("Parameter %s in action %s not found"%(param.name, action_definition.name))
        #Transforming preconditions from predicate to relations
        self._preconditions = self._transform_action_proposition_recursive(action_definition.preconditions)
        #Transforming effects from predicate to relations
        self._effects = self._transform_action_proposition_recursive(action_definition.effects)
        
    def _transform_action_proposition_recursive(self, action_prop: ActionProposition):
        """A method that is used to recursively navigate an actionProposition and transform the predicates to relations
        
        Parameters
        ----------
        action_prop : ActionProposition
            actionProposition to navigate and transform to relations
        """
        if action_prop.name in ['and', "or", "not"]:
            if action_prop.name == 'not' and len(action_prop.parameters) == 1:
                relation = self._from_predicate_to_relation(action_prop.parameters[0], True)
                return relation
            return_action_prop = ActionProposition(action_prop.name, [])
            for item in action_prop.parameters:
                if type(item) == Predicate:
                    relation = self._from_predicate_to_relation(item)
                    return_action_prop.add_parameter(relation)
                elif type(item) == ActionProposition:
                    return_action_prop.add_parameter(self._transform_action_proposition_recursive(item))
            return return_action_prop
        elif action_prop.name == 'forall':
            #TODO: transformation for forall
            pass   

    def _from_predicate_to_relation(self, predicate, not_value = False) -> Relation:
        list_entity = []
        for arg in predicate.arguments:
            if arg.name not in self._parameters.keys():
                raise ValueError("%s not found in list of parameters"%(arg.name))
            list_entity.append(self._parameters[arg.name])
        if not_value:
            return Relation(predicate, list_entity, RelationValue.FALSE)
        else:
            return Relation(predicate, list_entity, RelationValue.TRUE)
            
        
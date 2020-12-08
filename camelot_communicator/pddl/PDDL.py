#!/usr/bin/env python
# Four spaces as indentation [no tabs]
from pddl.relation_value import RelationValue
from pddl.relation import Relation
from pddl.entity import Entity
from pddl.predicate import Predicate
import re
from pddl.action import Action, ActionParameter, ActionProposition
from pddl.types import Type
from pddl.domain import Domain
from pddl.problem import Problem

class PDDL_Parser:

    def __init__(self):
        self.domain = Domain()
        self.supported_keywords = ['and', 'or', 'not', 'forall']
    # ------------------------------------------
    # Tokens
    # ------------------------------------------

    def scan_tokens(self, filename):
        with open(filename,'r') as f:
            # Remove single line comments
            str = re.sub(r';.*$', '', f.read(), flags=re.MULTILINE).lower()
        # Tokenize
        stack = []
        list = []
        current = ''
        for t in re.findall(r'[()]|[^ \t()]+', str):
            if t == '(':
                stack.append(list)
                list = []
            elif t == ')':
                if stack:
                    l = list
                    list = stack.pop()
                    list.append(l)
                    current = ''
                else:
                    raise Exception('Missing open parentheses')
            elif t != '\n':
                if ':' in t:
                    current = t.replace('\n', '')
                words = t.split('\n')
                if not all(p == '' for p in words):
                    tmod = t.replace('\n', '')
                    list.append(tmod)
                    if ((current == ':types' and tmod != ":types") or (current == ':objects' and tmod != ":objects")) and '\n' in t:
                        list.append('\n')


        if stack:
            raise Exception('Missing close parentheses')
        if len(list) != 1:
            raise Exception('Malformed expression')
        return list[0]

    #-----------------------------------------------
    # Parse domain
    #-----------------------------------------------

    def parse_domain(self, domain_filename):
        tokens = self.scan_tokens(domain_filename)
        if type(tokens) is list and tokens.pop(0) == 'define':
            self.actions = []
            self.types = []
            self.predicates = []
            while tokens:
                group = tokens.pop(0)
                t = group.pop(0)
                if   t == 'domain':
                    self.domain.domain_name = group[0]
                elif t == ':requirements':
                    self.domain.requirements = group[0]
                    # TODO raise exception for unknown requirements
                elif t == ':predicates':
                    self.parse_predicates(group)
                elif t == ':types':
                    self.parse_types_and_objects(group, 'types')
                elif t == ':action':
                    self.parse_action(group)
                    self.domain.actions = self.actions
                else: print(str(t) + ' is not recognized in domain')
        else:
            raise 'File ' + domain_filename + ' does not match domain pattern'
        return self.domain
    #-----------------------------------------------
    # Parse types
    #-----------------------------------------------
    def parse_types_and_objects(self, group, target):
        """
        Method to parse the Types and objects and adding them to the domain/problem. 
        """
        if not type(group) is list:
            raise Exception('No types defined')

        extend = Type("object", None)
        list_extend = []

        while(group):
            item = group.pop(0)
            if item != '\n':
                if item == '-':
                    name = group.pop(0)
                    if name != 'object':
                        extend = self.domain.find_type(name)
                        if extend is None:
                            raise Exception('Type not found in %s'%(target))
                elif '-' in item:
                    raise Exception ('Found "-" attached to a name of a type, please put spaces between types. Error: %s'%(str(item)))
                else:
                    if item in list_extend:
                        raise Exception ('Cannot create %s twice'%(target))
                    list_extend.append(item)
            else:
                for i in list_extend:
                    if target == 'types':
                        self.domain.add_type(Type(i, extend))
                    else:
                        self.objects.append(Entity(i, extend))
                list_extend = []

    #-----------------------------------------------
    # Parse predicates
    #-----------------------------------------------
    def parse_predicates(self, group):
        if not type(group) is list:
            raise Exception('No predicates defined')

        for predicate in group:
            if type(predicate) is not list:
                raise Exception ('Invalid predicate parsing. Expecting list got %s' % str(type(predicate)))
            predicate1 = self._parse_predicate(predicate)
            if self.domain.find_predicate(predicate1.name) is not None:
                raise Exception('Two predicates with the same name (%s) are declared'%(predicate1.name))
            self.domain.add_predicate(predicate1)

    def _parse_predicate(self, predicate):
        work_list = predicate.copy()
        first = True
        n_arg = 0
        args = []
        predicate_obj = Predicate('', [])
        while work_list:
            item = work_list.pop(0)
            if first:
                if '?' in item:
                    raise Exception('? cannot be in the name of the predicate')
                predicate_obj.name = item
                first = False
                continue
            #Checking cases where the - is attached to the word
            elif '-' in item:
                if '?' not in item:
                    possible_type = item.replace('-', '')
                    if possible_type != '':
                        item = possible_type
            if '?' not in item and item != '-':
                t = self.domain.find_type(item)
                if t is None:
                    raise Exception('Type "%s" used in predicate %s not found' % (item,predicate_obj.name))
                for a in args:
                    predicate_obj.arguments.append(t)
                    n_arg += 1
                    if n_arg > 2:
                        raise Exception('A predicate cannot have more then 2 arguments')
                args = []
            #Base case of a variable
            elif '?' in item:
                args.append(item)
        return predicate_obj

    #-----------------------------------------------
    # Parse action
    #-----------------------------------------------

    def parse_action(self, group): #TODO: check predicates
        name = group.pop(0)
        if not type(name) is str:
            raise Exception('Action without name definition')
        for act in self.actions:
            if act.name == name:
                raise Exception('Action ' + name + ' redefined')
        action_parameters = []
        preconditions = []
        effects = []
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if not type(group) is list:
                    raise Exception('Error with ' + name + ' parameters')
                action_parameters = self.parse_variable(group.pop(0))
            elif t == ':precondition':
                preconditions = self.split_propositions(group.pop(0), name, ':preconditions', action_parameters)
            elif t == ':effect':
                effects = self.split_propositions(group.pop(0),  name, ':effects', action_parameters)
            else: print(str(t) + ' is not recognized in action')
        self.actions.append(Action(name, action_parameters, preconditions, effects))

    #-----------------------------------------------
    # Parse problem
    #-----------------------------------------------

    def parse_problem(self, problem_filename):
        tokens = self.scan_tokens(problem_filename)
        if type(tokens) is list and tokens.pop(0) == 'define':
            self.problem_name = 'unknown'
            self.objects = []
            self.starting_state = []
            while tokens:
                group = tokens.pop(0)
                t = group[0]
                if   t == 'problem':
                    self.problem_name = group[-1]
                elif t == ':domain':
                    if self.domain.domain_name != group[-1]:
                        raise Exception('Different domain specified in problem file')
                    self.problem = Problem(self.problem_name, self.domain)
                elif t == ':requirements':
                    pass # Ignore requirements in problem, parse them in the domain
                elif t == ':objects':
                    group.pop(0)
                    self.parse_types_and_objects(group, 'objects')
                    self.problem.objects = self.objects
                elif t == ':init':
                    group.pop(0)
                    self.parse_relations(group)
                    self.problem.initial_state = self.starting_state
                elif t == ':goal':
                    #We don't need the goal yet
                    pass
                else: print(str(t) + ' is not recognized in problem')
            return self.problem

    def parse_relations(self, group):
        while group:
            item = group.pop(0)
            pred = self.domain.find_predicate(item.pop(0))
            entities = []
            while item:
                i = item.pop(0)
                ent = self.problem.find_objects(i)
                if ent is None:
                    raise Exception('Couldn\'t find object %s'%(i))
                entities.append(ent)
            self.starting_state.append(Relation(pred, entities, RelationValue.TRUE, self.domain, self.problem))
    #-----------------------------------------------
    # Split propositions
    #-----------------------------------------------
    def split_propositions(self, group, name, part, action_parameters):
        if not type(group) is list:
            raise Exception('Error with ' + name + part)
        return self._split_proposition(group, action_parameters)

    
    def _split_proposition(self, group, action_parameters):      
        prop = group.pop(0)
        if prop == 'and':
            action_prop = ActionProposition('and', [])
            for item in group:
                self._evaluate_proposition(item, action_parameters, action_prop)
            return action_prop
        elif prop == 'not':
            action_prop = ActionProposition('not', [])
            if len(group) > 1:
                raise Exception("Proposition not can have only one predicate")
            self._evaluate_proposition(group[0], action_parameters, action_prop)
            return action_prop
        elif prop == 'or':
            action_prop = ActionProposition('or', [])
            for item in group:
                self._evaluate_proposition(item, action_parameters, action_prop)
            return action_prop
        elif prop == 'forall': #TODO: double check parameters forall
            param = self.parse_variable(group[0])[0]
            forall_action_paramenters = action_parameters.copy()
            forall_action_paramenters.append(param)
            action_prop = ActionProposition('forall', [], argument=param)
            self._evaluate_proposition(group[1], forall_action_paramenters, action_prop)
            return action_prop
        else:
            raise Exception('Proposition not supported.')

    def parse_variable(self, parameters):
        name_p = []
        action_parameters = []
        while parameters:
            item = parameters.pop(0)
            if '?' in item:
                if '-' in item:
                    raise Exception('Character "-" attached to the name of the variable')
                name_p.append(item)
            elif '-' in item:    
                type_p = ''
                if item == '-':
                    type_p = parameters.pop(0)
                else:
                    type_p = item.replace('-', '')
                if len(name_p) == 0:
                    raise Exception('Error while parsing action parameters')

                type_obj = self.domain.find_type(type_p)
                if type_obj is None:
                    raise Exception ('Name of type "%s" in action parameter does not exist'%(type_p))
                for i in name_p:
                    action_parameters.append(ActionParameter(i, type_obj))
                name_p = []
        return action_parameters
    
    def _find_actionparameter(self, name, action_parameters):
        for item in action_parameters:
            if item.name == name:
                return item
        return None
    
    def _evaluate_proposition(self, item, action_parameters, action_prop):
        if item[0] in self.supported_keywords:
            action_prop.add_parameter(self._split_proposition(item, action_parameters))
        else:
            pred = self.domain.find_predicate(item[0])
            if pred is None:
                raise Exception('Predicate is not recognized')
            if len(item)-1 != len(pred.arguments):
                raise Exception('Number of elements in proposition different to number or predicate variables')
            i = 1
            for arg in pred.arguments:
                ap1 = self._find_actionparameter(item[i], action_parameters)
                if ap1 is None:
                    raise Exception('Action Parameter is not recognized')
                i += 1
                #TODO: check if predicates arguments are fulfilled
            action_prop.add_parameter(pred)



# ==========================================
# Main
# ==========================================
#if __name__ == '__main__':
    # import sys
    # import pprint
    # domain = sys.argv[1]
    # problem = sys.argv[2]
    # parser = PDDL_Parser()
    # print('----------------------------')
    # pprint.pprint(parser.scan_tokens(domain))
    # print('----------------------------')
    # pprint.pprint(parser.scan_tokens(problem))
    # print('----------------------------')
    # parser.parse_domain(domain)
    # parser.parse_problem(problem)
    # print('Domain name:' + parser.domain_name)
    # for act in parser.actions:
    #     print(act)
    # print('----------------------------')
    # print('Problem name: ' + parser.problem_name)
    # print('Objects: ' + str(parser.objects))
    # print('State: ' + str(parser.state))
    # print('Positive goals: ' + str(parser.positive_goals))
    # print('Negative goals: ' + str(parser.negative_goals))
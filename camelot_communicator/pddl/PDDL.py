#!/usr/bin/env python
# Four spaces as indentation [no tabs]
from pddl.predicate import Predicate
import re
from pddl.action import Action
from pddl.types import Type
from pddl.domain import Domain

class PDDL_Parser:

    def __init__(self):
        self.domain = Domain()
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
                    if current == ':types' and tmod != ":types" and '\n' in t:
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
                    self.parse_types(group)
                elif t == ':action':
                    self.parse_action(group)
                    self.domain.actions = self.actions
                else: print(str(t) + ' is not recognized in domain')
        else:
            raise 'File ' + domain_filename + ' does not match domain pattern'
    #-----------------------------------------------
    # Parse types
    #-----------------------------------------------
    def parse_types(self, group):
        """
        Method to parse the Types and adding them to the domain. 
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
                elif '-' in item:
                    raise Exception ('Found "-" attached to a name of a type, please put spaces between types. Error: %s'%(str(item)))
                else:
                    if item in list_extend:
                        raise Exception ('Cannot create Type twice')
                    list_extend.append(item)
            else:
                for i in list_extend:
                    self.domain.add_type(Type(i, extend))
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
            work_list = predicate.copy()
            first = True
            arg1 = False
            arg2 = False
            predicate1 = Predicate('', '')
            while work_list:
                item = work_list.pop(0)
                if first:
                    if '?' in item:
                        raise Exception('? cannot be in the name of the predicate')
                    predicate1.name = item
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
                    if t is not None:
                        if not arg1:
                            predicate1.argument_1 = t
                            arg1 = True
                        elif not arg2:
                            predicate1.argument_2 = t
                            predicate1.unary = False
                            arg2 = True
                        else:
                            raise Exception('A predicate cannot have more then 2 arguments')
            self.domain.add_predicate(predicate1)


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
        parameters = []
        positive_preconditions = []
        negative_preconditions = []
        add_effects = []
        del_effects = []
        while group:
            t = group.pop(0)
            if t == ':parameters':
                if not type(group) is list:
                    raise Exception('Error with ' + name + ' parameters')
                parameters = group.pop(0)
            elif t == ':precondition':
                self.split_propositions(group.pop(0), positive_preconditions, negative_preconditions, name, ' preconditions')
            elif t == ':effect':
                self.split_propositions(group.pop(0), add_effects, del_effects, name, ' effects')
            else: print(str(t) + ' is not recognized in action')
        self.actions.append(Action(name, parameters, positive_preconditions, negative_preconditions, add_effects, del_effects))

    #-----------------------------------------------
    # Parse problem
    #-----------------------------------------------

    def parse_problem(self, problem_filename):
        tokens = self.scan_tokens(problem_filename)
        if type(tokens) is list and tokens.pop(0) == 'define':
            self.problem_name = 'unknown'
            self.objects = []
            self.state = []
            self.positive_goals = []
            self.negative_goals = []
            while tokens:
                group = tokens.pop(0)
                t = group[0]
                if   t == 'problem':
                    self.problem_name = group[-1]
                elif t == ':domain':
                    if self.domain_name != group[-1]:
                        raise Exception('Different domain specified in problem file')
                elif t == ':requirements':
                    pass # Ignore requirements in problem, parse them in the domain
                elif t == ':objects':
                    group.pop(0)
                    self.objects = group
                elif t == ':init':
                    group.pop(0)
                    self.state = group
                elif t == ':goal':
                    self.split_propositions(group[1], self.positive_goals, self.negative_goals, '', 'goals')
                else: print(str(t) + ' is not recognized in problem')

    #-----------------------------------------------
    # Split propositions
    #-----------------------------------------------
    #TODO: check on predicates
    def split_propositions(self, group, pos, neg, name, part):
        if not type(group) is list:
            raise Exception('Error with ' + name + part)
        if group[0] == 'and':
            group.pop(0)
        else:
            group = [group]
        for proposition in group:
            if proposition[0] == 'not':
                if len(proposition) != 2:
                    raise Exception('Unexpected not in ' + name + part)
                neg.append(proposition[-1])
            else:
                pos.append(proposition)
    #-----------------------------------------------
    # Split objects
    #-----------------------------------------------

    def split_objects(self, group):
        if not type(group) is list:
            raise Exception('Error with objects parsing')
        for item in group:
            #TODO: parse objects in problem
            pass

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

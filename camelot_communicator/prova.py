import sys
from  pddlpy import DomainProblem


domainfile = ".\\pddl\\example_domain.pddl"
problemfile = ".\\pddl\\example_problem.pddl"
domprob = DomainProblem(domainfile, problemfile)
print()
print("DOMAIN PROBLEM")
print("objects")
print("\t", domprob.worldobjects())
print("operators")
print("\t", list( domprob.operators() ))
print("init",)
print("\t", domprob.initialstate())
print("goal",)
print("\t", domprob.goals())
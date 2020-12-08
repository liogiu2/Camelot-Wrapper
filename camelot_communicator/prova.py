from world_state import WorldState
from pddl.PDDL import PDDL_Parser

parser = PDDL_Parser()

domain = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\camelot_domain.pddl"
problem = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\example_problem.pddl"

domain_parsed = parser.parse_domain(domain)
problem_parsed = parser.parse_problem(problem)

#print(domain_parsed)
#print(problem_parsed)

initial_state = WorldState(domain_parsed).create_wordstate_from_problem(problem_parsed)



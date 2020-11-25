from pddl.PDDL import PDDL_Parser

parser = PDDL_Parser()

domain = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\camelot_domain.pddl"
problem = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\example_problem.pddl"

domain_parsed = parser.parse_domain(domain)
problem_parsed = parser.parse_problem(problem)

parser.objects


import os

location_message_prefix = ("input started walking", "input stopped walking", "input arrived", "input exited")

supported_types = {}
supported_predicates = {}

def get_domain_and_problem_path():
    domain_path = ""
    problem_path = ""
    if os.name == 'nt':
        domain_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\camelot_domain.pddl"
        problem_path = "C:\\Users\\giulio17\\Documents\\Camelot_work\\camelot_communicator\\camelot_communicator\\pddl\\data\\example_problem.pddl"
    else:
        domain_path = "/Users/giuliomori/Documents/GitHub/camelot_communicator/camelot_communicator/pddl/data/camelot_domain.pddl"
        problem_path = "/Users/giuliomori/Documents/GitHub/camelot_communicator/camelot_communicator/pddl/data/example_problem.pddl"
    return domain_path, problem_path
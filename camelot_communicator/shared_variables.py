import os
from pathlib import Path

location_message_prefix = ("input started walking", "input stopped walking", "input arrived", "input exited")

supported_types = {}
supported_predicates = {}

action_list = []

def get_domain_and_problem_path():
    domain_path = ""
    problem_path = ""
    p = Path(__file__).parent
    domain_path  = (p / "pddl_data/camelot_domain.pddl").resolve()
    problem_path = (p / "pddl_data/example_problem.pddl").resolve()
    # if os.name == 'nt':
    #     domain_path = "pddl_data\\camelot_domain.pddl"
    #     problem_path = "pddl_data\\example_problem.pddl"
    # else:
    #     domain_path = "/Users/giuliomori/Documents/GitHub/camelot_communicator/camelot_communicator/pddl_data/camelot_domain.pddl"
    #     problem_path = "/Users/giuliomori/Documents/GitHub/camelot_communicator/camelot_communicator/pddl_data/example_problem.pddl"
    return str(domain_path), str(problem_path)

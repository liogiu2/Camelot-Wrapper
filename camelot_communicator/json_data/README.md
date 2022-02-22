# Instructions on how to structure pddl_actions_to_camelot.json
It's important to structure the pddl_actions_to_camelot.json in a way that the program can correctly interpret.

For each action that we want to write the commands that we want to execute in Camelot, the key has to be the name of the action as in the "camelot_domain.pddl".
As before, as argument of this key, we need a dictionary with the key "commands".
This key has as argument a list of dictionaries, where each disctionary is constructed of 3 keys. "action_name" that represents the name of the Camelot action we want to execute, "action_args" that is a list of parameters that will be part of the action, and "wait" that needs to be True or False based on if we want the platform to wait for a reply from Camelot.
The parameter that needs to be substituted in "action_args" must be with the same name as in the PDDL declaration under "camelot_domain.pddl". 
If the parameter needs to be a String, then it needs to have '' in the declaration.
For example the action "give" has three parameters that are of interest of the camelot command: "?giver ?receiver ?item".
To make the substitution happen, the program will replace these three strings with the corresponding entity.
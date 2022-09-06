from yarnrunner_python import YarnRunner

# Open the compiled story and strings CSV.
with open('narrative/output/initial_narrative.yarnc', 'rb') as story_f:
    with open('narrative/output/initial_narrative.csv', 'r') as strings_f:
        # Create the runner
        runner = YarnRunner(story_f, strings_f, autostart=False)

# Register any command handlers
# (see https://yarnspinner.dev/docs/writing/nodes-and-content/#commands)
def update_player_model(arg1, arg2, arg3, arg4, arg5):
    print(arg1, arg2, arg3, arg4, arg5)

runner.add_command_handler("update_player_model", update_player_model)

# Start the runner and run until you hit a choice point
runner.resume()

# Access the lines printed from the story
print('\n'.join(runner.get_lines()))

# Access the choices
for choice in runner.get_choices():
    print(f"[{choice.index}] ${choice.text}")

# Make a choice and run until the next choice point or the end
runner.choose(1)

# Access the new lines printed from the last run
print('\n'.join(runner.get_lines()))

# Are we done?
if runner.finished:
    print("Woohoo! Our story is over!")
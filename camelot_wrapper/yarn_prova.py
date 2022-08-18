from yarnrunner_python import YarnRunner

# Open the compiled story and strings CSV.
story_f = open('narrative/Output.yarnc', 'rb')
strings_f = open('narrative/Output.csv', 'r')

# Create the runner
runner = YarnRunner(story_f, strings_f, autostart=False)

# Register any command handlers
# (see https://yarnspinner.dev/docs/writing/nodes-and-content/#commands)
def custom_command(arg1, arg2):
    pass

runner.add_command_handler("customCommand", custom_command)

# Start the runner and run until you hit a choice point
runner.resume()

# Access the lines printed from the story
print('\n'.join(runner.get_lines()))

# Access the choices
for choice in runner.get_choices():
    print(f"[{choice.index}] ${choice.text}")

# Make a choice and run until the next choice point or the end
runner.choose(0)

# Access the new lines printed from the last run
print('\n'.join(runner.get_lines()))

# Are we done?
if runner.finished:
    print("Woohoo! Our story is over!")
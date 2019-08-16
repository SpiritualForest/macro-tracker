from ui.cli import commands
import config

# Experimental.
# Examples:
# Update the database macros:
# add, -f food, -w weight, -d date (optional)
# if -d is omitted, defaults to today's date
# add -f potato -w 500g -d 10/8/2019
# add -f apple -w 100g
# -f and -w accept comma separated lists too:
# add -f potato,apple -w 500g,100g

# Show logged macros:
# -d/--date, if omitted defaults to day
# --fromdate/-fd from date, --todate/-td to date, show all logs from date <date> to <date>
# -st/--showtargets, show how the macros compare against the targets set by the user 
# viewmacros -d 10/8/2019 (D/M/Y)
# viewmacros -fd 25/4/2019 -td 30/5/2019 to show all logs from 25 April 2019 to 30 May 2019

def ParseParameters(command, text):
    # Parse the text into parameters
    words = text.split()
    # Now we go through the words and look for -param value pairs,
    # and construct a dictionary based on those pairs
    # Start at the first word, skipping every other word.
    # The skipped word is the value
    callbackParameters = {}
    seen = []
    for i in range(0, len(words), 2):
        try:
            param = words[i]
            value = words[i+1]
            if param in commands.GetCommandParameters(command):
                # parameter is supported, get the callback argument name for it
                # for example: param is "-f", arg name is "food"
                arg = commands.GetArgumentName(command, param)
                callbackParameters[arg] = value
                seen.append(param)
            else:
                # Error?
                print('Invalid parameter for {}: "{}"'.format(command, param))
                return
        except IndexError:
            # If this index error occurred,
            # it means there was error with the command
            print("Error parsing parameters for command {}".format(command))
            return
    # Check that all the required parameters were seen:
    for rp in commands.GetRequiredParameters(command):
        if rp not in seen:
            print('Error: required argument for {} missing: "{}"'.format(command, rp))
            return None

    return callbackParameters

# Parse the user input. Get the command.
# If the command exists, parse the rest of the text as parameters.
# Validate that the command supports the parameters.
# Create a dictionary of the parameters with their respective values.
# call ExecuteCallback(commandName, parametersDict)

def run():
    print("Macrotracker {}".format(config.version))
    print("Available commands: {}".format(", ".join(commands.commands.keys())))
    print('Type "exit" to quit.')
    while True:
        line = input("> ")
        if line.lower() == "exit":
            # exit is special - terminate the program
            return
        else:
            if not line:
                # empty line
                continue
            command, parameters = line.split(" ", 1)
            if command not in commands.commands:
                print("Unknown command: {}".format(command))
                continue
            # Command known
            parameters = ParseParameters(command, parameters)
            if parameters:
                # The parameters are valid, we can execute the callback
                commands.ExecuteCallback(command, parameters)

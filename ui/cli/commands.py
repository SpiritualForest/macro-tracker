# This file defines the various commands,
# their supported parameters, help messages,
# and callback functions.
#from database import api
from collections import namedtuple

CommandParameters = namedtuple("CommandParameters", "Required Optional")

commands = {}

def RegisterCommand(command, parameters, callback):
    # command: string
    # parameters: a tuple of the parameters the command accepts
    # callback: callback function
    if not command:
        print("No command name passed to RegisterCommand().")
        return
    if not parameters:
        print('No passed to RegisterCommand() with "{}"'.format(command))
        return
    if not callback:
        print('No callback function passed to RegisterCommand() with "{}"'.format(command))
        return
    # Now we can add the command to our commands dictionary
    commands[command] = {}
    commands[command]["callback"] = callback
    commands[command]["parameters"] = {}
    commands[command]["required parameters"] = []
    for p in parameters:
        param, callbackArg, required = p.split("=")
        commands[command]["parameters"][param] = callbackArg
        if required:
            # required parameter
            commands[command]["required parameters"].append(param)

def GetCommandParameters(command):
    return commands[command]["parameters"]

def GetCallbackFunction(command):
    return commands[command]["callback"]

def GetArgumentName(command, parameter):
    return commands[command]["parameters"][parameter]

def IsRequiredParameter(command, parameter):
    return parameter in commands[command]["required parameters"]

def GetRequiredParameters(command):
    return commands[command]["required parameters"]

def ExecuteCallback(command, parameters):
    # command: string, the command whose callback we execute
    # parameters: dict of "param": "value", which we pass to the callback
    callback = GetCallbackFunction(command)
    callback(**parameters)

def addCmd_callback(food, weight, date=None):
    print("addCmd_callback called with arguments: food={}, weight={}, date={}".format(food, weight, date))

# NOTE: testing! Remove this!
RegisterCommand("add", ("-f=food=required", "-w=weight=required", "-d=date="), addCmd_callback)

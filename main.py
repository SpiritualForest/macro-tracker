# Macro tracker main file
import sys
from macrotracker import database

# Each input mode has its own function that handles its subsequent commands

def insert_mode():
    commands = ("exit", "exitall",)
    print("Entering insert mode.")
    print("Available commands: {}".format(", ".join(commands)))
    while True:
        cmd = input("insert > ").lower()
        if cmd == "exit":
            print("Leaving insert mode.")
            return
        if cmd == "exitall":
            return "EXITALL"

def CommandLineInterface():
    # If this function is called, it means
    # that the file was executed with no parameters,
    # and has thus lead to the default user interface,
    # which is a simple command-line interface.
    commands = sorted(["exit", "makedb", "add", "view"])
    print("Welcome to the macro tracker program.")
    print("Available commands: {}".format(", ".join(commands)))
    while True:
        cmd = input("> ").lower()
        if cmd and cmd not in commands:
            # Non-empty string that doesn't exist in the commands tuple
            print("Error. Unknown command: {}".format(cmd))
            continue
        if cmd == "exit":
            return
        if cmd == "makedb":
            database.MakeDatabase()
        if cmd == "insert":
            result = insert_mode()
            if result == "EXITALL":
                return


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Get into the default command line interface
        CommandLineInterface()
    else:
        # TODO: Accept parameters for single-instruction commands
        # and also to launch a GUI.
        # Will be implemented much later.
        pass

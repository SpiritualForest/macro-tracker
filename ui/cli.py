import cmd
import re
from database import api
from database.macros import foodIds # Just for names
import config

dateMatch = re.compile("(\d+)/(\d+)/?(\d+)") # d/m/y

class MacrotrackerShell(cmd.Cmd):
    intro = "Macrotracker {} - type ? to list all the commands.\n".format(config.version)
    prompt = "macrotracker> "

    def do_add(self, arg):
        "Update macros. ADD <id> <weight in grams> [d/m/y]: ADD 1 500 10/8/2019"
        params = arg.split()
        date = None
        if len(params) < 2:
            print("Not enough parameters. Syntax: ADD <id> <weight in grams> [/d/m/y]")
            return
        if len(params) > 3:
            print("Too many parameters. Syntax: ADD <id> <weight in grams> [d/m/y]")
            return
        # At least two parameters supplied
        date = None
        if len(params) == 3:
            # get the date, must be the last parameter
            found = dateMatch.findall(params.pop())
            if not found:
                print("Error in date parameter. Must be D/M/Y - 10/8/2019 for 10 August 2019.")
                return
            # If we reached here, there was a match
            date = tuple(map(int, found.pop(0)))
        try:
            params = [float(p) for p in params]
        except ValueError:
            # Cannot proceed, not a floating point number
            print("Error in parameters. ID and weight must be numbers.")
            return
        foodId, weight = params
        # Finally, call the API function
        success = api.AddFood(foodId, weight, date)
        if success:
            foodName = foodIds[foodId]
            print("Macros updated. Added {}g of {}".format(weight, foodName))

    def do_listfoods(self, arg):
        "List the available foods and their IDs"
        foods = api.ListFoods()
        for food in foods:
            print("{} (id {})".format(foods[food], food))

    def do_exit(self, arg):
        'Exit the application'
        return True

    def precmd(self, line):
        # Make it lower
        return line.lower()

def run():
    MacrotrackerShell().cmdloop()

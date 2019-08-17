import cmd
import re
from database import api
from database.macros import foodIds, Macros # Just for names
import config

dateMatch = re.compile("(\d+)/(\d+)/?(\d+)") # d/m/y

class MacrotrackerShell(cmd.Cmd):
    intro = "Macrotracker {} - type ? to list all the commands.\n".format(config.version)
    prompt = "macrotracker> "

    def do_addfood(self, arg):
        # TODO: Accept weight units (g, kg)
        "Update macros for the given date.\nIf the date is omitted, defaults to today.\nSyntax: ADD <id> <weight in grams> [d/m/y]: ADD 1 500 10/8/2019"
        params = arg.split()
        date = None
        if len(params) < 2:
            print("Not enough parameters. Syntax: ADDFOOD <id> <weight in grams> [/d/m/y]")
            return
        if len(params) > 3:
            print("Too many parameters. Syntax: ADDFOOD <id> <weight in grams> [d/m/y]")
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
    
    def help_addfood(self):
        print("---")
        print("Update macros for the given date.")
        print("Syntax: ADDFOOD <food id> <weight in grams> [d/m/y]")
        print("The date parameter is a string, day/month/year - 10/8/2019 for 10 August 2019.")
        print("The date parameter is optional, and if omitted, will default to today's date.")
        print("Example: ADDFOOD 0 500 30/7/2019 to add the macro values for 500 grams of food ID 0 for 30 July 2019.")
        print("Dateless: ADDFOOD 0 500 to add the macro values for 500 grams of food ID 0 for today's date.")
        print('Type "listfoods" to view a list of foods and their respective ID.')
        print("---")

    def do_settargets(self, arg):
        if not arg:
            print("Not enough parameters.")
            print("Syntax: SETTARGETS macroname=value [macroname=value macroname=value]")
        words = arg.split()
        params = {}
        for word in words:
            try:
                macro, value = word.split("=")
                macro = macro.capitalize()
                if macro not in Macros._fields:
                    # No such parameter, let's skip it
                    print("Non-existent parameter encountered: {} - ignoring.".format(macro))
                    continue
                if not value:
                    # Empty value, skip
                    print("Empty value for parameter: {} - skipping.".format(macro))
                    continue
                # If we reached here, the parameter and value are valid
                params[macro] = float(value)

            except ValueError:
                print("Error parsing parameter. Parameter syntax is name=value")
                return
        # End of loop.
        # If we reached here, we can call the API function - only if the params dict isn't empty.
        # Pass it a Macros namedtuple.
        if params:
            success = api.SetMacros(Macros(**params))
            if success:
                print("Macro targets updated.")

    def help_settargets(self):
        print("---")
        print("Sets the target amount for the given macros.")
        print("Syntax: SETTARGETS macroname=N [macroname=N macroname=N]")
        print("Example: SETTARGETS calories=1600 fat=10 protein=80 carbs=300")
        print("You don't have to set all macros each time. Macros that were omitted from the command will not be updated.")
        print('Type "listmacros" to view all available macros.')
        print("---")
    
    def do_showtargets(self, arg):
        'Show the target values for all the macros and the date they were last updated.'
        if arg:
            print("This command doesn't accept any parameters.")
            return
        values, date = api.ShowTargets()
        print("---")
        if date is None:
            print("Targets were never set.")
            return
        # Targets have been previously updated, we can show them
        print("Targets updated on {}".format(date))
        for field in values._fields:
            value = getattr(values, field)
            print("{}: {}".format(field, value))
        print("---")

    def do_listfoods(self, arg):
        "List the available foods and their IDs"
        foods = api.ListFoods()
        for food in foods:
            print("{} (id {})".format(foods[food], food))
    
    def do_listmacros(self, arg):
        'List the available macros for which a target amount can be set.'
        print("Available macros:")
        print(", ".join(api.ListMacros()))

    def do_exit(self, arg):
        'Exit the application'
        return True

    def precmd(self, line):
        # Make it lower
        return line.lower()

    def emptyline(self):
        # Do nothing
        pass

def run():
    MacrotrackerShell().cmdloop()

import cmd
import re
from database import api
from database.datehandler import GetDateString, GetYear, GetDaysAgo
from database.macros import foodIds, Macros, units # Just for names
import config

dateMatch = re.compile("^(\d+)[/\.](\d+)[/\.]?(\d+)?") # Matches both d/m/y and d.m.y with year parameter optional
unitMatch = re.compile("(\d+)(g$|kg$|mg$)")
timeStringMatch = re.compile("^(\d+)(d|w|m|y)$") # 2d, 10m, 5w, 3y

def MatchDateString(dateString):
    # match the date string
    # and return a tuple of (d, m, y)
    # or None if not found
    try:
        day, month, year = dateMatch.findall(dateString).pop()
        if not year:
            # No year supplied,
            # Default to the current year.
            year = GetYear()
        # Form the date tuple
        date = (int(day), int(month), int(year))
        return date

    except IndexError:
        # Pop from an empty list, means there was no re match.
        return None    

class MacrotrackerShell(cmd.Cmd):
    intro = 'Macrotracker {} - use "help" to list all the commands.\n'.format(config.version)
    prompt = "macrotracker> "

    def do_addfood(self, arg):
        params = arg.split()
        date = None
        if len(params) < 2:
            print("Not enough parameters. Syntax: ADDFOOD <id> <weight in grams> [/d/m[/y]]")
            return
        if len(params) > 3:
            print("Too many parameters. Syntax: ADDFOOD <id> <weight in grams> [d/m[/y]]")
            return
        # At least two parameters supplied
        if len(params) == 3:
            # get the date, must be the last parameter
            found = dateMatch.findall(params.pop())
            if not found:
                print("Error in date parameter. Must be D/M/Y - 10/8/2019 for 10 August 2019.")
                return
            # If we reached here, there was a match
            date = tuple(map(int, found.pop(0)))
        try:
            # Parse the weight and ID and make them into int/float
            foodId, weight = params
            foodId = int(foodId)
            foundWeight = unitMatch.findall(weight)
            if not foundWeight:
                print("Error in parsing weight parameter. Must be Nmg, Ng or Nkg: 720mg, 120g, or 1.2kg depending on unit.")
                return
            # Get the weight and the unit
            weight, unit = foundWeight.pop()
            # Testing
            oldweight = float(weight)
            weight = float(weight)
            # Now we convert the weight to grams
            if unit == "kg":
                # Multiply by 1000
                weight *= 1000
            elif unit == "mg":
                # divide by 1000
                weight = weight / 1000
        except ValueError:
            # Cannot proceed, ID or weight is not a digit
            print("Error in parameters. ID and weight must be numbers.")
            return
        # Finally, call the API function
        success = api.AddFood(foodId, weight, date)
        if success:
            foodName = foodIds[foodId]
            print("---")
            print("Macros updated. Added {}g of {}".format(weight, foodName))
            print("---")
    
    def help_addfood(self):
        print("---")
        print("Update macros for the given date.")
        print("Syntax: ADDFOOD <food id> <weight><unit> [d/m/y]")
        print("The date parameter is a string, day/month/year - 10/8/2019 for 10 August 2019.")
        print("The date parameter is optional, and if omitted, will default to today's date.")
        print("Example: ADDFOOD 0 500g 30/7/2019 to add the macro values for 500 grams of food ID 0 for 30 July 2019.")
        print("Dateless: ADDFOOD 0 1.3kg to add the macro values for 1.3 kilograms (1300 grams) of food ID 0 for today's date.")
        print('Type "listfoods" to view a list of foods and their respective ID.')
        print("---")

    def do_settarget(self, arg):
        if not arg:
            print("Not enough parameters.")
            print("Syntax: SETTARGET macroname=value [macroname=value macroname=value]")
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

    def help_settarget(self):
        print("---")
        print("Sets the target amount for the given macros.")
        print("Syntax: SETTARGET macroname=N [macroname=N macroname=N]")
        print("Example: SETTARGET calories=1600 fat=10 protein=80 carbs=300")
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
            print("{}: {}{}".format(field, value, units[field]))
        print("---")

    def do_getmacros(self, arg):
        # Get the macros tracked in the specified period of time
        args = arg.split()
        startDate, endDate = None, None
        results = {}
        if args:
            modeArg = args.pop(0)
            # mode can be --date/-d <date>, --daterange/-dr <start> <end>, --fromlast/-fl <N><d(ay)|w(eek)|m(onth)|y(ear)>
            if modeArg in ("--date", "-d"):
                # Single day's macros
                if not args:
                    # No date supplied
                    print("Error. No date supplied.")
                    return
                elif len(args) > 1:
                    # Too many parameters given
                    print("Error. Too many parameters supplied for date argument.")
                    return
                # Match the date
                argString = args.pop()
                startDate = MatchDateString(argString)
                if not startDate:
                    # No match
                    print("Error parsing parameter for date argument. Use D.M[.Y] or D/M[/Y]. Year is optional.")
                    return
                endDate = startDate # Same date on this occasion

            # Now date ranges
            elif modeArg in ("--daterange", "-dr"):
                if len(args) < 2:
                    # Not enough parameters
                    print("Error. Not enough parameters.")
                    return
                # Match the dates
                startDate, endDate = MatchDateString(args[0]), MatchDateString(args[1])
                if not startDate or not endDate:
                    # One of the strings didn't match
                    print("Error parsing parameter for date argument. Use D.M[.Y] or D/M[/Y]. Year is optional.")                    
                    return
            # Now --fromlast
            elif modeArg in ("--fromlast", "-fl"):
                # Get all macros that were tracked from the last N day/week/month/year ago until today
                if not args:
                    print("Error. Not enough parameters.")
                    return
                try:
                    time, timeString = timeStringMatch.findall(args.pop()).pop()
                    time = int(time)
                    if timeString == "w":
                        # week
                        time *= 7
                    elif timeString == "m":
                        # month
                        time *= 30
                    elif timeString == "y":
                        # year
                        time *= 365
                    dateDaysAgo = GetDaysAgo(time) # datetime object representing the date from <time> days ago
                    startDate = (dateDaysAgo.day, dateDaysAgo.month, dateDaysAgo.year)
                except IndexError:
                    # pop from empty list again, no match
                    print("Error parsing time string parameter.")
                    return
            else:
                print('Unknown parameter. See "help getmacros"')
                return

        # Call the API function  with the dates
        # If the dates are both None, will default to today's date (see api.py)
        results = api.GetMacros(startDate, endDate)
        if not results:
            print("No macros tracked for the specified period of time.")
            return
        print("---")
        for date in results:
            print("Macros for {}:".format(GetDateString(date)))
            m = results[date]
            for field in m._fields:
                print("{}: {}{}".format(field, round(getattr(m, field), 3), units[field]))
            print("---")
    
    def help_getmacros(self):
        print("---")
        print("Get the macros that were tracked at the time periods specified.")
        print("If no parameters are given, gets the macros from today.")
        print("Multiple parameters accepted:")
        print("GETMACROS --date/-d <d.m[.y> to get the macros from the given date. If the year parameter is omitted, defaults to the current year.")
        print("Example: GETMACROS --date 17.8 for 17 August of this year.")
        print("---")
        print("GETMACROS --daterange/-dr <start date> <end date>")
        print("Example: GETMACROS --daterange 4.8.2019 10.8.2019 to get the macros from 4-10 August 2019. Year is optional.")
        print("---")
        print("GETMACROS --fromlast/-fl <N><d|w|m|y>")
        print("Example: GETMACROS --fromlast 35d to get all the macros that were tracked in the last 35 days.")
        print('Time units accepted: "d" for day, "w" for week, "m" for month, "y" for year.')
        print("Example: GETMACROS -fl 2w to get the macros that were tracked in the last 2 weeks, up to today.")
        print("---")

    def do_getfoods(self, arg):
        # Show the foods that were logged on a given date
        date = None
        if arg:
            # parse the date
            date = MatchDateString(arg)
            if not date:
                print("Error parsing date parameter. Use D.M[.Y] or D/M[/Y]. Year is optional.")
                return
        foods, dateString = api.GetFoods(date)
        print("---")
        if not foods:
            print("Nothing logged on {}".format(dateString))
        else:
            print("Logged on {}:\n".format(dateString))
            for food in foods:
                print("{}: {}g".format(food, foods[food]))
        print("---")

    def help_getfoods(self):
        print("---")
        print("Show the foods that were logged on the given date.")
        print("Syntax: GETFOODS [D/M/Y]")
        print("The date parameter is optional, and if omitted, defaults to today's date.")
        print("---")
        
    def do_listfoods(self, arg):
        "List the available foods and their IDs"
        print("---")
        foods = api.ListFoods()
        for food in foods:
            print("{} (id {})".format(foods[food], food))
        print("---")
    
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

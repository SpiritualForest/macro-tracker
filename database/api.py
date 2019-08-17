# This file implements the database API
# I chose to do this so that the user interface modules
# will interact with an abstraction layer for the database,
# rather than directly with the database module.

from database import database
from database import macros
from database import datehandler

def ListFoods():
    # Just list all the foods found in the macros.data dictionary
    # and their respective id that's used to perform operations on them
    # such as adding their macros to the database.
    return macros.foodIds

def AddFood(foodId, weight, date=None):
    if foodId not in macros.foodIds:
        print("ID doesn't exist: {}".format(foodId))
        return False
    if weight < 0:
        print("Error: sub-zero weight.")
        return False
    if date:
        # Date parameter supplied,
        # now we convert it to a unix epoch timestamp value.
        day, month, year = date
        # Get a unix timestamp and add the food to the database
        timestamp = datehandler.GetTimestampFromDate(datehandler.GetDatetimeObject(day, month, year))
        date = timestamp
    # Now call the database function
    foodName = macros.foodIds[foodId]
    success = database.AddFood(foodName, weight, date)
    return success

def ListMacros():
    # return a list of all available macros
    # for which a target amount can be set
    return macros.Macros._fields

def SetMacros(macroValues):
    # Update the user's settings.
    # A None value indicates the parameter should not be changed
    success = database.UpdateUserSettings(macroValues)
    return success

def ShowTargets():
    # return the user settings for the macros
    values, date = database.GetUserSettings()
    if date is not None:
        # Get a string like "12 May 2016" from the unix timestamp
        date = datehandler.GetDateString(date)
    return (values, date)

def GetTodayMacros():
    # FIXME: remove this temporary function, this is just for testing
    return database.GetTodayMacros()

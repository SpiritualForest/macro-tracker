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

def GetFoods(date=None):
    # Get the foods that were logged on <date>
    # If date is None, default to today
    if date:
        timestamp = datehandler.GetTimestampFromDate(datehandler.GetDatetimeObject(*date))
        date = timestamp
    else:
        date = datehandler.GetToday()
    foods = database.GetFoods(date)
    # Stringify the date
    dateString = datehandler.GetDateString(date)
    return (foods, dateString)

def GetMacros(start=None, end=None):
    # Get the macros that were tracked on the days between <start> and <end>, inclusive
    # start and end are tuples of (day, month, year) values
    # if start and end are None, will default to today's date in the database function (GetMacros() database.by)
    startTimestamp = datehandler.GetToday()
    if start:
        startTimestamp = datehandler.GetTimestampFromDate(datehandler.GetDatetimeObject(*start))
    if end:
        end = datehandler.GetTimestampFromDate(datehandler.GetDatetimeObject(*end))
    results = database.GetMacros(startTimestamp, end)
    return results

def RemoveFood(foodId, weight, date=None):
    # Remove tracked <weight> of <foodId> from the database
    if foodId not in macros.foodIds:
        print("ID doesn't exist: {}".format(foodId))
        return
    if weight < 0:
        # Must be positive
        print("Sub-zero weight provided: {}".format(weight))
        return
    if date:
        # date is a tuple of (day, month, year)
        timestamp = datehandler.GetTimestampFromDate(datehandler.GetDatetimeObject(*date))
        date = timestamp
    name = macros.foodIds[foodId]
    success = database.RemoveFood(name, weight, date)
    return success

def CalcFood(foodId, weight):
    # Calculate the macros for the given food based on the weight
    # and return the results
    if foodId not in macros.foodIds:
        print("ID doesn't exist: {}".format(foodId))
        return
    if weight < 0:
        print("Error: sub-zero weight.")
        return
    food = macros.foodIds[foodId]
    macroValues = macros.CalculateMacros(food, weight)
    return macroValues

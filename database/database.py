# Handle the database stuff for logging user data
# FIXME: there should be one sqlite3 connection object that's active
# from the moment the application starts until it exits.
# Do not create another connection object for every single command.
import sqlite3
import os # for os.remove()
# Now our own project's code
from database import macros
from database import datehandler
import config

DATABASE = config.database # Our database file
# Database table names
TABLE_MACROS = "Macros"
TABLE_SETTINGS = "Settings"
TABLE_FOODS = "Foods"

def MakeDatabase():
    # Create the database
    macroColumns = ", ".join(["{} real".format(macro) for macro in macros.Macros._fields])
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # First, create the Macros table
        cursor.execute("CREATE TABLE {} (ID integer primary key autoincrement, {}, Date real);".format(TABLE_MACROS, macroColumns))
        
        # Settings table
        cursor.execute("CREATE TABLE {} (ID integer primary key autoincrement, {}, Date real);".format(TABLE_SETTINGS, macroColumns))
        # Initialize all settings to NULL, to indicate that the settings were never updated
        macroNames = ", ".join([macro for macro in macros.Macros._fields])
        nulls = ", ".join(["NULL" for x in macros.Macros._fields])
        cursor.execute("INSERT INTO {} ({}, Date) VALUES ({}, NULL)".format(TABLE_SETTINGS, macroNames, nulls))
         
        # Food weight log table
        cursor.execute("CREATE TABLE {} (ID integer primary key autoincrement, Name text, Weight real, Date real);".format(TABLE_FOODS))
        
        # Save change and close the connection
        conn.commit()
        conn.close()
        return True # success

    except sqlite3.OperationalError as exception:
        print("Database creation failed: {}".format(exception))
        return False # failure

def UpdateMacros(macroValues, date):
    # Update the day's macros in the database.
    # If this is the first insertion of the day, insert a new row.
    # Otherwise, update the existing row's values.
    # macroValues should be a Macros() tuple, date should be a unix epoch float
    if macroValues._fields != macros.Macros._fields:
        # Wrong data structure supplied?
        return False

    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Select only the macro values from the database, based on today's date (string we made up)
    cursor.execute("SELECT {} FROM {} WHERE Date=?".format(", ".join(macroValues._fields), TABLE_MACROS), (date,))
    row = cursor.fetchone()
        # Now let's start preparing our INSERT or UPDATE statement
    if not row:
        # Empty row indicates that nothing from today was found.
        # This means it's the first insertion attempt for today,
        # therefore we use INSERT INTO.
        # Now we generate the parameter-holding question marks,
        # depending on how many macro values we have.
        # Results in a string of "?, ?, ?, [...]" of however many values exist.
        questionMarks = ", ".join(["?" for x in macroValues._fields])
        sqlStatement = "INSERT INTO {} ({}, Date) VALUES ({}, ?)".format(TABLE_MACROS, ", ".join(macroValues._fields), questionMarks)
        cursor.execute(sqlStatement, (*macroValues, date))
    else:
        # A previous insertion has already occurred today.
        # This time we update the values by adding the new values to the old ones.
        updatedValues = [getattr(macroValues, key) + row[key] for key in row.keys()]
        # This time we need question marks that are like "?=?, ?=?, ?=?" for our parameters.
        questionMarks = ", ".join(["{}=?".format(key) for key in row.keys()])
        sqlStatement = "UPDATE {} SET {} WHERE Date=?".format(TABLE_MACROS, questionMarks)
        cursor.execute(sqlStatement, (*updatedValues, date))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    # return True to indicate success
    return True

def AddMacros(food, weight, date):
    macroValues = macros.CalculateMacros(food, weight)
    success = UpdateMacros(macroValues, date)
    return success

def AddFood(food, weight, date=None):
    # TODO: allow specification of weight unit (g, kg)
    # API function.
    if food not in macros.data or weight < 0:
        # Food doesn't exist or weight is less than 0.
        return False

    # Now try to add the macros
    if not date:
        # No date supplied, we default to today's date
        date = datehandler.GetToday()
    success = AddMacros(food, weight, date)
    if not success:
        # Database update failed
        return
    # Database update succeeded
    # Now add the individual food stuff too.
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Now insert the food and weight into the foods table
    # This one is always INSERT INTO
    sqlStatement = "INSERT INTO {} (Name, Weight, Date) VALUES (?, ?, ?)".format(TABLE_FOODS)
    cursor.execute(sqlStatement, (food, weight, date,))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return True # success

def UpdateUserSettings(macroValues):
    # Update the user's macro target settings
    # input: a Macros namedtuple
    # First, let's build the query
    if macroValues._fields != macros.Macros._fields:
        # Incorrect data?
        print("Incorrect data supplied to UpdateUserSettings(): {}".format(macroValues))
        return
    updateKeys, updateValues = [], []
    for field in macroValues._fields:
        value = getattr(macroValues, field)
        if value is None:
            # It's None, skip it
            continue
        # If we reached here, it's a value that needs to be updated
        updateKeys.append(field)
        updateValues.append(value)
    
    if not updateKeys:
        # All values were None. Nothing to update.
        return

    questionMarks = ", ".join(["{}=?".format(field) for field in updateKeys])
    date = datehandler.GetToday()
    # No WHERE because there's only one row at all times in this table, which is initialized to 0.
    sqlStatement = "UPDATE {} SET {}, Date=?".format(TABLE_SETTINGS, questionMarks)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sqlStatement, (*updateValues, date,))
    conn.commit()
    conn.close()
    # Return True to indicate success
    return True

def GetTodayMacros():
    # Show macro data that were logged on the given date (day/month/year)
    query = "SELECT {} FROM {} WHERE Date=?".format(", ".join(macros.Macros._fields), TABLE_MACROS)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (datehandler.GetToday(),))
    # Since we always update the values for the same date, there will only ever be one row for each date
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    else:
        # Return a tuple of the result
        result = {}
        for key in row.keys():
            result[key] = row[key]
        return macros.Macros(**result)

def GetMacros(start, end=None):
    # Get the macros for all the dates from <start> to <end> (inclusive)
    # start and end are datetime.datetime() objects containing only the date.
    # returns a tuple of tuples, containing the results
    startTimestamp = datehandler.GetTimestampFromDate(start)
    endTimestamp = datehandler.GetTimestampFromDate(end)
    query = "SELECT {}, Date FROM {} WHERE Date >= ? AND Date <= ?;".format(", ".join(macros.Macros._fields), TABLE_MACROS)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, (startTimestamp, endTimestamp))
    rows = tuple(cursor.fetchall())
    conn.close()
    return rows

def GetUserSettings():
    # Get the user's target settings
    # and the date they were set on
    # returns a tuple of (Macros, unix epoch)
    query = "SELECT {}, Date FROM {}".format(", ".join(macros.Macros._fields), TABLE_SETTINGS)
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()
    if not row:
        # Something went wrong
        return None
    else:
        result = {}
        # Iterate until the second to last element,
        # these ones go into our result dict.
        # The date is the last element and will be pulled separately.
        for key in row.keys()[:-1]:
            result[key] = row[key]
        date = row["Date"]
        return (macros.Macros(**result), date)

def ExportDatabase():
    # Export the database into HTML, SQL, whatever.
    pass

def MergeDatabase():
    # Merge the data from an existing database into a new one.
    # This is useful in case we added more macros after creating
    # a database, but don't want to lose the previous logs.
    pass

def RemoveDatabase():
    # Delete the database file.
    try:
        os.remove(DATABASE)
    except (FileNotFoundError, PermissionError) as exception:
        print("Could not remove database: {}".format(exception))

# SQLite update statement:
# UPDATE table 
# SETcolumn1 = value1, column2 = value2
# WHERE condition

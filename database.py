# Handle the database stuff for logging user data
# TODO: 
# There should be a command line parameter to indicate verbosity.
# If the user wants extra verbosity, then print() all the output, otherwise don't.
import sqlite3
import datetime
import macros
import os

# Paths and filenames
# TODO: this should be configurable, not hard coded.
LOCALPATH = os.path.dirname(os.path.realpath(__file__)) + "/"
DATABASE = LOCALPATH + "dietlog.db"

def GetTodayString():
    # Return a string of today's date
    # D/M/Y - 10/8/2019 for 10 August 2019
    date = datetime.date.today()
    return "{}/{}/{}".format(date.day, date.month, date.year)

TODAY = GetTodayString()

def MakeDatabase():
    # Create the database
    macroColumns = ", ".join(["{} real".format(macro) for macro in macros.Macros._fields])
    foodLogColumns = "Name text, Weight real, Date text"
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        # First, create the Macros table
        cursor.execute("""CREATE TABLE Macros ( 
            ID integer primary key autoincrement, 
            {},
            Date text
            );""".format(macroColumns))
        # Settings table
        cursor.execute("""CREATE TABLE Settings (
            ID integer primary key autoincrement,
            {}
            );""".format(macroColumns))
        # Initialize all settings to 0
        macroNames = ", ".join([macro for macro in macros.Macros._fields])
        zeroes = ", ".join(["0" for x in macros.Macros._fields])
        cursor.execute("INSERT INTO Settings ({}) VALUES ({})".format(macroNames, zeroes))
        # Food weight log table
        cursor.execute("""CREATE TABLE Foods (
            ID integer primary key autoincrement,
            {});""".format(foodLogColumns))
        # Save change and close the connection
        conn.commit()
        conn.close()
        return True # success

    except sqlite3.OperationalError as exception:
        print("Database creation failed: {}".format(exception))
        return False # failure

def UpdateMacros(food, weight):
    # Update the day's macros in the database.
    # If this is the first insertion of the day, insert a new row.
    # Otherwise, update the existing row's values.
    if food not in macros.data:
        # No such food
        print("Error. Food item not found: {}".format(food))
        return
    if weight < 0:
        print("Error. Sub-zero weight provided.")
        return
    # Checks pass
    macroValues = macros.CalculateMacros(food, weight)
    if not macroValues:
        # Something still went wrong?
        return

    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Select only the macro values from the database, based on today's date (string we made up)
    cursor.execute("SELECT {} FROM Macros WHERE Date=?".format(", ".join(macroValues._fields)), (TODAY,))
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
        sqlStatement = "INSERT INTO Macros ({}, Date) VALUES ({}, ?)".format(", ".join(macroValues._fields), questionMarks)
        cursor.execute(sqlStatement, (*macroValues, TODAY))
    else:
        # A previous insertion has already occurred today.
        # This time we update the values by adding the new values to the old ones.
        updatedValues = [getattr(macroValues, key) + row[key] for key in row.keys()]
        # This time we need question marks that are like "?=?, ?=?, ?=?" for our parameters.
        questionMarks = ", ".join(["{}=?".format(key) for key in row.keys()])
        sqlStatement = "UPDATE Macros SET {} WHERE Date=?".format(questionMarks)
        cursor.execute(sqlStatement, (*updatedValues, TODAY))
    # Now insert the food and weight into the foods table
    # This one is always INSERT INTO
    sqlStatement = "INSERT INTO Foods (Name, Weight, Date) VALUES (?, ?, ?)"
    cursor.execute(sqlStatement, (food, weight, TODAY,))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    # return True to indicate success
    return True

def UpdateUserSettings(macroValues):
    # Update the user's macro target settings
    # input: a Macros namedtuple
    # First, let's build the query
    if macroValues._fields != macros.Macros._fields:
        # Incorrect data?
        print("Incorrect data supplied to UpdateUserSettings()")
        return

    questionMarks = ", ".join(["{}=?".format(field) for field in macros.Macros._fields])
    # No WHERE because there's only one row at all times in this table, which is initialized to 0.
    sqlStatement = "UPDATE Settings SET {}".format(questionMarks)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(sqlStatement, macroValues)
    conn.commit()
    conn.close()
    # Return True to indicate success
    return True

def ShowMacros(date):
    # Show macro data that were logged on <date>
    # Date has to be a string of D/M/Y - 10/8/2019 for 10 August 2019
    if len(date.split("/")) < 3:
        # TODO: Allow just a D/M date to passed,
        # which means that the year parameter defaults to the current year.
        print("Invalid date: {}".format(date))
        return
    query = "SELECT {} FROM Macros WHERE Date=?".format(", ".join(macros.Macros._fields))
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, (date,))
    row = cursor.fetchone()
    if not row:
        return None
    else:
        # For purposes of making the UI loosely coupled, return a tuple here
        result = {}
        for key in row.keys():
            result[key] = row[key]

        return macros.Macros(**result)

def ExportDatabase():
    # Export the database into HTML, SQL, whatever.
    pass

def MergeDatabase():
    # Merge the data from an existing database into a new one.
    # This is useful in case we added more macros after creating
    # a database, but don't want to lose the previous logs.
    pass

def DeleteDatabase():
    # Delete the database file.
    try:
        os.remove(DATABASE)
    except (FileNotFoundError, PermissionError) as exception:
        print("Could not remove database: {}".format(exception))

# SQLite update statement:
# UPDATE table 
# SETcolumn1 = value1, column2 = value2
# WHERE condition

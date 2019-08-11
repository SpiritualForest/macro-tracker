# database.py

# Handle the database stuff for logging user data

import sqlite3
import datetime
import macros
import os

# Paths and filenames
LOCALPATH = os.path.dirname(os.path.realpath(__file__)) + "/"
DATABASE = LOCALPATH + "dietlog.db"
TABLES = LOCALPATH + "make_tables.sql"

def GetTodayString():
    # Return a string of today's date
    # D/M/Y
    date = datetime.date.today()
    return "{}/{}/{}".format(date.day, date.month, date.year)

def MakeDatabase():
    # Create the database
    instructions = ""
    try:
        with open(TABLES) as fd:
            instructions = fd.read().strip()
    except (FileNotFoundError, PermissionError, IOError) as exception:
        print("Database creation failed.")
        print("Could not read SQL instructions file: {}".format(exception))
        return
    # Got the instructions, we can proceed
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.executescript(instructions)
        conn.commit()
        conn.close()
        print("Database created successfully: {}".format(DATABASE))
    except sqlite3.OperationalError as exception:
        print("Database creation failed: {}".format(exception))

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
    today = GetTodayString() # D/M/Y - 10/8/2019 for 10 August 2019
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Select only the macro values from the database, based on today's date (string we made up)
    cursor.execute("SELECT {} FROM Macros WHERE Date=?".format(", ".join(macroValues._fields)), (today,))
    row = cursor.fetchone()
    
    # Now let's start preparing our INSERT or UPDATE statement
    if not row:
        # Nothing from today was found.
        # This means it's the first insertion attempt for today,
        # therefore we use INSERT INTO.
        # Now we generate the parameter-holding question marks,
        # depending on how many macro values we have.
        # Results in a string of "?, ?, ?, [...]" of however many values exist.
        questionMarks = ", ".join(["?" for x in range(len(macroValues._fields))])
        sqlStatement = "INSERT INTO Macros ({}, Date) VALUES ({}, ?)".format(", ".join(macroValues._fields), questionMarks)
        cursor.execute(sqlStatement, (*macroValues, today))
    else:
        # A previous insertion has already occurred today.
        # This time we update the values by adding the new values to the old ones.
        # Get a list of (key, value, key, value, key, value) of updated values
        # and their respective key names.
        updatedValues = [getattr(macroValues, key) + row[key] for key in row.keys()]
        # This time we need question marks that are like "?=?, ?=?, ?=?" for our parameters.
        questionMarks = ", ".join(["{}=?".format(key) for key in row.keys()])
        sqlStatement = "UPDATE Macros SET {} WHERE Date=?".format(questionMarks)
        cursor.execute(sqlStatement, (*updatedValues, today))
    # Now insert the food and weight into the foods table
    # This one is always INSERT INTO
    sqlStatement = "INSERT INTO Foods (Name, Weight, Date) VALUES (?, ?, ?)"
    cursor.execute(sqlStatement, (food, weight, today,))
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# SQLite update statement:
# UPDATE table 
# SETcolumn1 = value1, column2 = value2
# WHERE condition

if __name__ == "__main__":
    UpdateMacros("Potato", 750)

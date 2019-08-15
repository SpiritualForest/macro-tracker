from database import database
from database import macros
from database import datehandler
import sqlite3
import unittest

database.DATABASE = "tests/database.db"

class TestDatabase(unittest.TestCase):
    def test_MakeDatabase(self):
        # Test the MakeDatabase function
        database.MakeDatabase()
        # Now let's make sure all tables exist
        conn = sqlite3.connect(database.DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        names = cursor.fetchall()
        self.assertIn((database.TABLE_MACROS,), names)
        self.assertIn((database.TABLE_SETTINGS,), names)
        self.assertIn((database.TABLE_FOODS,), names)
        cursor.execute("SELECT {} FROM {}".format(", ".join(macros.Macros._fields), database.TABLE_SETTINGS))
        # Verify that all columns in the user settings table have been initialized to zero
        expected = tuple([0 for x in macros.Macros._fields])
        row = cursor.fetchone()
        self.assertEqual(row, expected)

        # Remove the database
        database.RemoveDatabase()

    def test_CalculateMacros(self):
        potato = [77, 0.09, 16.2, 2.2, 2, 79, 6]
        doublePotato = tuple([macro*2 for macro in potato])
        result = macros.CalculateMacros("Potato", 200)
        self.assertEqual(result, doublePotato)

    def test_AddFoodAndGetMacros(self):
        # Test the functions AddFood() and GetMacrosByDate()
        database.MakeDatabase()
        # Add
        database.AddFood("Potato", 100)
        macroValues = (77, 0.09, 16.2, 2.2, 2, 79, 6)
        # Get
        self.assertEqual(database.GetTodayMacros(), macroValues)
        database.RemoveDatabase()

    def test_UpdateAndGetUserSettings(self):
        # Test the functions UpdateUserSettings() and GetUserSettings()
        database.MakeDatabase()
        settings = macros.Macros(Calories=2000, Fat=10, Carbs=360, Fiber=60, Protein=50, Water=1000, Sodium=7000)
        database.UpdateUserSettings(settings)
        # Now check that the settings were added
        self.assertEqual(database.GetUserSettings(), settings)
        database.RemoveDatabase()

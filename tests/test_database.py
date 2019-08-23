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
        expected = tuple([None for x in macros.Macros._fields])
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
        # Test the functions AddFood() and GetMacros()
        database.MakeDatabase()
        # Add
        database.AddFood("Potato", 100)
        macroValues = (77, 0.09, 16.2, 2.2, 2, 79, 6)
        # Get
        self.assertEqual(database.GetMacros(datehandler.GetToday())[datehandler.GetToday()], macroValues)
        database.RemoveDatabase()

    def test_AddFoodAndRemoveFood(self):
        # Test the function RemoveFood()
        database.MakeDatabase()
        database.AddFood("Potato", 100)
        database.AddFood("Apple", 100)
        foods = database.GetFoods(datehandler.GetToday())
        self.assertIn("Potato", foods)
        self.assertIn("Apple", foods)
        self.assertEqual(foods["Potato"], 100)
        self.assertEqual(foods["Apple"], 100)
        # Now remove 50 grams
        database.RemoveFood("Potato", 50)
        database.RemoveFood("Apple", 50)
        foods = database.GetFoods()
        self.assertEqual(foods["Potato"], 50)
        self.assertEqual(foods["Apple"], 50)
        # remove database
        database.RemoveDatabase()

    def test_UpdateAndGetUserSettings(self):
        # Test the functions UpdateUserSettings() and GetUserSettings()
        database.MakeDatabase()
        expectedDate = datehandler.GetToday()
        settings = macros.Macros(Calories=2000, Fat=10, Carbs=360, Fiber=60, Protein=50, Water=1000, Sodium=7000)
        database.UpdateUserSettings(settings)
        # Now check that the settings were added
        self.assertEqual(database.GetUserSettings(), (settings, expectedDate))
        # Now test changing only some of the values.
        # A None value means we don't want to update it
        settings = macros.Macros(Calories=None, Fat=12, Carbs=300, Fiber=None, Protein=None, Water=1200, Sodium=None)
        expectedSettings = macros.Macros(Calories=2000, Fat=12, Carbs=300, Fiber=60, Protein=50, Water=1200, Sodium=7000)
        database.UpdateUserSettings(settings)
        self.assertEqual(database.GetUserSettings(), (expectedSettings, expectedDate))
        # Now test supplying only None values, meaning that nothing should be changed 
        # and the UpdateUserSettings() should abort its operation without querying the database at all.
        settings = macros.Macros(Calories=None, Fat=None, Carbs=None, Fiber=None, Protein=None, Water=None, Sodium=None)
        database.UpdateUserSettings(settings)
        # the "expected" tuple should still match
        self.assertEqual(database.GetUserSettings(), (expectedSettings, expectedDate))
        database.RemoveDatabase()

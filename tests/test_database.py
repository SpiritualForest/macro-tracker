# Run tests on the database module code
import unittest
import sqlite3

import database
from macros import Macros
# Set the database file to our temporary test one
# We create this test database, run all tests on it, and then remove it.
# This file path setting only happens when running tests,
# it does not affect the program's "real" runtime paths.
database.DATABASE = database.LOCALPATH + "tests/test_database.db"

class TestDatabaseFunctions(unittest.TestCase):

    def test_MakeDatabase(self):
        # Test the MakeDatabase() function
        # and ensure all tables are created
        database.MakeDatabase()

        # Check that all tables exist.
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        conn = sqlite3.connect(database.DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        tables = cursor.fetchall()
        
        # Test that all our tables exist
        self.assertIn(('Macros',), tables)
        self.assertIn(('Settings',), tables)
        self.assertIn(('Foods',), tables)
        # Now test that all columns match the ones we need
        # First the Macros table.
        cursor.execute("SELECT * FROM Macros")
        columns = tuple([column[0] for column in cursor.description])
        self.assertEqual(columns, ("ID", *Macros._fields, "Date",))
        # Now the Settings table.
        cursor.execute("SELECT * FROM Settings")
        columns = tuple([column[0] for column in cursor.description])
        self.assertEqual(columns, ("ID", *Macros._fields,))
        # Now the foods table
        cursor.execute("SELECT * FROM Foods")
        columns = tuple([column[0] for column in cursor.description])
        self.assertEqual(columns, ("ID", "Name", "Weight", "Date",))
        database.DeleteDatabase()

    def test_UpdateMacros(self):
        database.MakeDatabase()
        database.UpdateMacros("Potato", 500)
        potato = Macros(Calories=385, Fat=0.45, Carbs=81, Fiber=11, Protein=10, Water=395, Sodium=30)
        query = "SELECT Calories, Fat, Carbs, Fiber, Protein, Water, Sodium FROM Macros WHERE Date=?"
        # Connect
        conn = sqlite3.connect(database.DATABASE)
        cursor = conn.cursor()
        cursor.execute(query, (database.TODAY,))
        row = cursor.fetchone()
        self.assertEqual(row, potato)
        # Now check the Foods database for the entry
        cursor.execute("SELECT Name, Weight FROM Foods WHERE Date=?", (database.TODAY,))
        row = cursor.fetchone()
        self.assertEqual(row, ("Potato", 500))
        database.DeleteDatabase()

    def test_UpdateUserSettings(self):
        database.MakeDatabase()
        settings = Macros(Calories=1800, Fat=15, Carbs=350, Fiber=70, Protein=50, Water=1000, Sodium=7000)
        # Call the function
        database.UpdateUserSettings(settings)
        query = "SELECT Calories, Fat, Carbs, Fiber, Protein, Water, Sodium FROM Settings"
        conn = sqlite3.connect(database.DATABASE)
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        # Assert that the settings are equal
        self.assertEqual(len(row), len(settings))
        self.assertEqual(row, settings)
        database.DeleteDatabase()

    def test_ShowMacros(self):
        database.MakeDatabase()
        # 500g
        potato = Macros(Calories=385, Fat=0.45, Carbs=81, Fiber=11, Protein=10, Water=395, Sodium=30)
        database.UpdateMacros("Potato", 500)
        dbMacros = database.ShowMacros(database.TODAY)
        # Assertions
        self.assertEqual(dbMacros, potato)
        # Now test for non existent date
        self.assertEqual(database.ShowMacros("1/1/1"), None)
        # Update again, check that the correct macros for 1kg of potatoes are set
        database.UpdateMacros("Potato", 500)
        self.assertEqual(database.ShowMacros(database.TODAY), (770, 0.90, 162, 22, 20, 790, 60))
        
        database.DeleteDatabase()

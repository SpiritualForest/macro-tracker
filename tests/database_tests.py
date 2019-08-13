# Run tests on the database module code
import unittest
import sqlite3
import sys
sys.path.append("..") # So we can import our own namespaces

import database
import macros

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
        self.assertEqual(columns, ("ID", *macros.Macros._fields, "Date",))
        # Now the Settings table.
        cursor.execute("SELECT * FROM Settings")
        columns = tuple([column[0] for column in cursor.description])
        self.assertEqual(columns, ("ID", *macros.Macros._fields,))
        # Now the foods table
        cursor.execute("SELECT * FROM Foods")
        columns = tuple([column[0] for column in cursor.description])
        self.assertEqual(columns, ("ID", "Name", "Weight", "Date",))

    def test_UpdateMacros(self):
        pass

try:
    unittest.main()
finally:
    # Clean up - remove the temporary test database
    database.DeleteDatabase()

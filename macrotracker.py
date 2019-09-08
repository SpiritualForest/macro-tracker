#!/usr/bin/env python

# Macro tracker main file
import os
from ui import cli
from database import database
import config

# We launch the command line interface by default
if __name__ == "__main__":
    # Check that the database exists, if not, make it.
    if not os.path.isfile(config.database):
        database.MakeDatabase()
    cli.run()

#!/usr/bin/env python

# Macro tracker main file
import argparse
import os
from ui import ui
from database import database
import config

parser = argparse.ArgumentParser(description="Track macro nutrient consumption.")
parser.add_argument("--gui", action="store_true")

args = parser.parse_args()

# We launch the command line interface by default
if __name__ == "__main__":
    # Check that the database exists, if not, make it.
    if not os.path.isfile(config.database):
        database.MakeDatabase()
    if args.gui:
        ui.run(ui.UI_GUI)
    else:
        ui.run(ui.UI_CLI)

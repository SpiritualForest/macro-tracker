# Macro tracker main file
import argparse
from database import datehandler
from ui import ui

parser = argparse.ArgumentParser(description="Track macro nutrient consumption.")
parser.add_argument("--gui", action="store_true")

args = parser.parse_args()

# We launch the command line interface by default
if args.gui:
    ui.run(ui.UI_GUI)

else:
    ui.run(ui.UI_CLI)

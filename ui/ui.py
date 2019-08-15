from ui import cli
from ui.gui import gui

UI_CLI = "cli"
UI_GUI = "gui"

def run(interface):
    # if cli, run the command line interface
    # if gui, run the graphical one (not yet implemented, Qt)
    # call: run(ui.UI_CLI) for command line
    if interface == UI_CLI:
        cli.run()
    elif interface == UI_GUI:
        gui.run()

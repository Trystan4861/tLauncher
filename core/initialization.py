"""This module contains functions that initialize the application and connect to the main window."""
import sys
from PyQt5 import QtWidgets
from pywinauto import Application
import functions as f
try:
    from config import PROGRAM_NAME
except ImportError:
    from core.config import PROGRAM_NAME

def initialize_app():
    """Initializes the application."""
    app = QtWidgets.QApplication(sys.argv)
    return app

def connect_pywinauto():
    """Connects to the main window of the application."""
    if f.is_compiled():
        executable_path = sys.executable
        Application().connect(path=executable_path).window().set_focus()
    else:
        Application().connect(title=PROGRAM_NAME).window().set_focus()

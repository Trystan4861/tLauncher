import os
import sys
import socket
from PyQt5 import QtWidgets
from plugin_manager import PluginManager
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon

def is_already_running():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 65432))
    except socket.error:
        return True
    return False

class Launcher:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugin_manager = PluginManager(os.path.join(self.base_dir, 'plugins'))
        self.plugin_manager.load_plugins()
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow()
        self.tray_icon = TrayIcon(self.main_window)

    def run(self):
        self.tray_icon.run()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    if is_already_running():
        print("La aplicación ya está en ejecución.")
        sys.exit(0)
    launcher = Launcher()
    launcher.run()

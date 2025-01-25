import sys
import configparser
from PyQt5 import QtWidgets, QtCore
from plugin_manager import PluginManager
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon
import functions as f
from hook import add_hotkey_action, Shortcut, Action

console = f.console

def load_config():
    config_path = f.get_base_path("config.ini")
    config = configparser.ConfigParser()
    if not f.pathExists(config_path):
        config['CONFIG'] = {
            'Hotkey': 'win+space'
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_path)
    return config

class Launcher(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager(f.get_base_path('plugins'))
        self.plugin_manager.load_plugins()
        self.config = load_config()
        self.app = QtWidgets.QApplication(sys.argv)
        hotkey_str = f.get_config_value(self.config, 'CONFIG', 'Hotkey', 'win+space')
        self.main_window = MainWindow(self, f.get_base_path, hotkey_str)
        self.tray_icon = TrayIcon(self.main_window, f.get_base_path)
        self.register_hotkey(hotkey_str)
        self.monitor_signal_file()

    def register_hotkey(self, hotkey_str):
        shortcut = Shortcut(hotkey_str)
        action = Action("main", lambda: self.main_window.display())
        if not add_hotkey_action(shortcut, action):
            console.warning(f"Failed to register hotkey {hotkey_str}")

    @QtCore.pyqtSlot()
    def monitor_signal_file(self):
        if not self.main_window.isVisible() and f.check_signal_file(f.get_base_path(".tlauncher_signal")):
            self.main_window.display()
        if not self.main_window.isVisible():
            QtCore.QTimer.singleShot(500, self.monitor_signal_file)

    def hide_main_window(self):
        self.main_window.hide()
        self.monitor_signal_file()

    def run(self):
        self.main_window.display()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    lock_file_path = f.get_base_path(".tlauncher.lock")
    lock_file = open(lock_file_path, "w")

    if f.is_already_running(lock_file):
        console.info("La aplicación ya está en ejecución.")
        f.create_signal_file(f.get_base_path(".tlauncher_signal"))
        sys.exit(0)

    launcher = Launcher()
    try:
        launcher.run()
    finally:
        # Liberar el bloqueo y cerrar el archivo al salir
        f.unlockFile(lock_file)
        f.silent_remove(lock_file_path)
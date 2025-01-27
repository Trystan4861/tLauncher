import sys
import json
from PyQt5 import QtWidgets, QtCore
from plugin_manager import PluginManager
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon
import functions as f
from hook import add_hotkey_action, Shortcut, Action

console = f.console

class Launcher(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager(f.get_base_path('plugins'))
        self.plugin_manager.load_plugins()
        self.config = f.load_config()
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow(self, f.get_base_path, self.config["hotkey"])
        self.tray_icon = TrayIcon(self.main_window, f.get_base_path)
        self.register_hotkey(self.config["hotkey"])
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
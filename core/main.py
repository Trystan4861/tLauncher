import os
import sys
import platform
import configparser
from PyQt5 import QtWidgets, QtCore
from plugin_manager import PluginManager
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon
from hook import add_hotkey_action, Shortcut, Action
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl

def is_already_running(lock_file):
    try:
        if platform.system() == "Windows":
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return False
    except (IOError, OSError):
        return True

def is_compiled():
    return getattr(sys, 'frozen', False)

def get_base_path(relative_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    if not is_compiled():
        base_path = os.path.abspath(os.path.join(base_path, '..'))
    return os.path.join(base_path, relative_path)

def silent_remove(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    return not os.path.exists(file_path)

def create_signal_file():
    signal_file_path = get_base_path(".tlauncher_signal")
    with open(signal_file_path, "w") as signal_file:
        signal_file.write("show")

def check_signal_file():
    signal_file_path = get_base_path(".tlauncher_signal")
    return os.path.exists(signal_file_path) and silent_remove(signal_file_path)

def load_config():
    config_path = get_base_path("config.ini")
    config = configparser.ConfigParser()
    if not os.path.exists(config_path):
        config['CONFIG'] = {
            'Hotkey': 'win+space'
        }
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_path)
    return config

def get_config_value(config, section, key, default_value):
    if not config.has_section(section):
        config.add_section(section)
    if not config.has_option(section, key):
        config.set(section, key, default_value)
        with open(get_base_path("config.ini"), 'w') as configfile:
            config.write(configfile)
    return config.get(section, key)

class Launcher(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugin_manager = PluginManager(os.path.join(self.base_dir, 'plugins'))
        self.plugin_manager.load_plugins()
        self.config = load_config()
        self.app = QtWidgets.QApplication(sys.argv)
        hotkey_str = get_config_value(self.config, 'CONFIG', 'Hotkey', 'win+space')
        self.main_window = MainWindow(self, get_base_path, hotkey_str)
        self.tray_icon = TrayIcon(self.main_window, get_base_path)
        self.register_hotkey(hotkey_str)
        self.monitor_signal_file()

    def register_hotkey(self, hotkey_str):
        shortcut = Shortcut(hotkey_str)
        action = Action("main", lambda: self.main_window.display())
        if not add_hotkey_action(shortcut, action):
            print(f"Failed to register hotkey {hotkey_str}")

    @QtCore.pyqtSlot()
    def monitor_signal_file(self):
        console.info("Monitoring signal file")
        if not self.main_window.isVisible() and check_signal_file():
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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lock_file_path = os.path.join(base_dir, ".tlauncher.lock")
    lock_file = open(lock_file_path, "w")

    if is_already_running(lock_file):
        print("La aplicación ya está en ejecución.")
        create_signal_file()
        sys.exit(0)

    launcher = Launcher()
    try:
        launcher.run()
    finally:
        # Liberar el bloqueo y cerrar el archivo al salir
        if platform.system() == "Windows":
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(lock_file, fcntl.LOCK_UN)
        lock_file.close()
        os.remove(lock_file_path)
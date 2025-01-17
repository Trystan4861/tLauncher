import os
import sys
import platform
from PyQt5 import QtWidgets
from plugin_manager import PluginManager
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon

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

def get_resource_path(relative_path):
    base_path = os.path.abspath(os.path.dirname(__file__))
    if not is_compiled():
        base_path = os.path.abspath(os.path.join(base_path, '..'))
    return os.path.join(base_path, relative_path)

class Launcher:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugin_manager = PluginManager(os.path.join(self.base_dir, 'plugins'))
        self.plugin_manager.load_plugins()
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = MainWindow(get_resource_path)
        self.tray_icon = TrayIcon(self.main_window, get_resource_path)

    def run(self):
        self.main_window.display()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lock_file_path = os.path.join(base_dir, ".tlauncher.lock")
    lock_file = open(lock_file_path, "w")

    if is_already_running(lock_file):
        print("La aplicación ya está en ejecución.")
        # Restaurar la ventana principal si ya está en ejecución
        app = QtWidgets.QApplication(sys.argv)
        main_window = MainWindow(get_resource_path)
        main_window.display()
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

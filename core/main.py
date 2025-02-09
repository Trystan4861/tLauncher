""" Módulo principal de la aplicación. """
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer
from ui.main_window import MainWindow
from ui.tray_icon import TrayIcon
import functions as f
from hook import add_hotkey_action, Shortcut, Action
try:
    from initialization import initialize_app, connect_pywinauto
except ImportError:
    from core.initialization import initialize_app, connect_pywinauto

console = f.console

class Launcher(QtCore.QObject):
    """Clase principal de la aplicación."""
    def __init__(self):
        super().__init__()
        self.config = f.load_config()
        self.app = initialize_app()
        self.main_window = MainWindow(self, f.get_base_path, self.config["hotkey"])
        self.tray_icon = TrayIcon(self.main_window, f.get_base_path)
        self.register_hotkey(self.config["hotkey"])

    def register_hotkey(self, hotkey_str):
        """Registra un atajo de teclado."""
        shortcut = Shortcut(hotkey_str)
        action = Action("main", self.main_window.display)
        if not callable(action.action):
            console.error("La acción acción %s asociada al atajo %s no puede ser llamada", action.action, shortcut)
        if not add_hotkey_action(shortcut, action):
            console.warning("Fallo al registrar el atajo %s", hotkey_str)

    @QtCore.pyqtSlot()
    def monitor_signal_file(self):
        """Monitorea el archivo de señal para mostrar la ventana principal."""
        if not self.main_window.isVisible() and f.check_signal_file(f.get_base_path(".tlauncher_signal")):
            self.main_window.display()
        if not self.main_window.isVisible():
            QTimer.singleShot(500, self.monitor_signal_file)

    def hide_main_window(self):
        """Oculta la ventana principal."""
        self.main_window.hide()
        self.monitor_signal_file()

    def run(self):
        """Ejecuta la aplicación."""
        self.main_window.display()
        connect_pywinauto()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    lock_file_path = f.get_base_path(".tlauncher.lock")
    lock_file = open(lock_file_path, "w", encoding="utf-8")

    if f.is_already_running(lock_file):
        f.create_signal_file(f.get_base_path(".tlauncher_signal"))
        sys.exit(0)

    launcher = Launcher()
    try:
        launcher.run()
    finally:
        # Liberar el bloqueo y cerrar el archivo al salir
        f.unlock_file(lock_file)
        f.silent_remove(lock_file_path)

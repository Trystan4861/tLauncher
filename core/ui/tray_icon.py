"""This module contains the TrayIcon class, which is a subclass of QSystemTrayIcon and is used to create the tray icon for the application."""
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon, QCursor

class TrayIcon(QSystemTrayIcon):
    """A class that represents the tray icon for the application."""
    def __init__(self, parent=None, get_base_path=None):
        self.get_base_path = get_base_path
        icon_path = self.get_base_path("resources/images/icons/tray.png")
        super().__init__(QIcon(icon_path), parent)
        self.setToolTip("tLauncher")
        self.create_tray_menu()
        self.activated.connect(self.on_tray_icon_activated)
        self.show()

    def create_tray_menu(self):
        """Creates the context menu for the tray icon."""
        tray_menu = QMenu()
        show_action = tray_menu.addAction("Mostrar tLauncher")
        show_action.triggered.connect(self.parent().display)
        exit_action = tray_menu.addAction("Salir")
        exit_action.triggered.connect(QApplication.instance().quit)
        self.setContextMenu(tray_menu)

    def on_tray_icon_activated(self, reason):
        """Handles the tray icon activation event"""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.Context):
            self.contextMenu().popup(QCursor.pos())

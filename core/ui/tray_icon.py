from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon, QCursor

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, get_base_path=None):
        self.get_base_path = get_base_path
        icon_path = self.get_base_path("resources/images/icons/tray.png")
        super().__init__(QIcon(icon_path), parent)
        self.setToolTip("tLauncher")
        self.createTrayMenu()
        self.activated.connect(self.onTrayIconActivated)
        self.show()

    def createTrayMenu(self):
        trayMenu = QMenu()
        showAction = trayMenu.addAction("Mostrar tLauncher")
        showAction.triggered.connect(self.parent().display)
        exitAction = trayMenu.addAction("Salir")
        exitAction.triggered.connect(QApplication.instance().quit)
        self.setContextMenu(trayMenu)

    def onTrayIconActivated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.Context):
            self.contextMenu().popup(QCursor.pos())
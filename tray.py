from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt5.QtGui import QIcon, QCursor

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(QIcon("icon.png"), parent)
        self.setToolTip("tLauncher")
        self.createTrayMenu()
        self.activated.connect(self.onTrayIconActivated)
        self.show()

    def createTrayMenu(self):
        trayMenu = QMenu()
        showAction = trayMenu.addAction("Mostrar tLauncher")
        showAction.triggered.connect(self.parent().showWidget)
        exitAction = trayMenu.addAction("Salir")
        exitAction.triggered.connect(QApplication.instance().quit)
        self.setContextMenu(trayMenu)

    def onTrayIconActivated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.Context):
            self.contextMenu().popup(QCursor.pos())
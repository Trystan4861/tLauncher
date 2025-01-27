import subprocess
import json
import os
import configparser
import sys
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QIcon, QCursor
from dropdown import Dropdown
from tray import TrayIcon
from notification import Notification
from go import GoModule
from settings import SettingsWindow

class TranslucentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.trayIcon = TrayIcon(self)
        self.config = configparser.ConfigParser()
        self.loadConfig()
        self.go_enabled = self.config.getboolean("go", "enabled")
        self.go_module = GoModule(self) if self.go_enabled else None
        self.settingsWindow = SettingsWindow(self)
        QApplication.instance().focusChanged.connect(self.onFocusChanged)

    def loadConfig(self):
        if not os.path.exists("config.ini"):
            self.createDefaultConfig()
        self.config.read("config.ini")
        if "go" not in self.config:
            self.config.add_section("go")
        if "enabled" not in self.config["go"]:
            self.config["go"]["enabled"] = "false"
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def createDefaultConfig(self):
        self.config.add_section("go")
        self.config["go"]["enabled"] = "false"
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)

    def updateGoModule(self, enabled):
        self.go_enabled = enabled
        self.go_module = GoModule(self) if self.go_enabled else None

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(450, 120)

        layout = QVBoxLayout()



        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(QIcon(os.path.join(self.getPath("icons"), "settings.png")))
        self.settingsButton.setFixedSize(40, 40)
        self.settingsButton.clicked.connect(self.showSettings)

        self.textBox = QLineEdit(self)
        self.textBox.setPlaceholderText("Escribe aquí...")
        self.textBox.setFixedSize(420, 65)
        self.textBox.textChanged.connect(self.onTextChanged)
        self.textBox.installEventFilter(self)

        self.dropdown = Dropdown(self, input_widget=self.textBox)
        self.dropdown.setFixedWidth(self.textBox.width())

        layout.addWidget(self.settingsButton, alignment=Qt.AlignRight | Qt.AlignTop)
        layout.addWidget(self.textBox, alignment=Qt.AlignCenter)
        layout.setContentsMargins(10, 0, 10, 10)

        self.setLayout(layout)

    def getPath(self,what="icons"):
                # Obtener la ruta del ejecutable
        if getattr(sys, 'frozen', False):
            executable_path = os.path.dirname(sys.executable)
        else:
            executable_path = os.path.dirname(os.path.abspath(__file__))

        if what == "icons":
            return os.path.join(executable_path, 'icons')
        elif what == "styles":
            return os.path.join(executable_path, 'styles')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hideWidget()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.doIt()
        elif event.key() in (Qt.Key_Up, Qt.Key_Down):
            if self.dropdown.isVisible():
                if event.key() == Qt.Key_Up:
                    self.dropdown.navigateSelection('up')
                elif event.key() == Qt.Key_Down:
                    self.dropdown.navigateSelection('down')
        else:
            super().keyPressEvent(event)

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress and source is self.textBox:
            if event.modifiers() == Qt.AltModifier and Qt.Key_1 <= event.key() <= Qt.Key_9:
                    index = event.key() - Qt.Key_1
                    print(f"Alt+{index + 1} pressed")  # Mensaje de depuración
                    if self.dropdown.isVisible() and index < len(self.dropdown.items):
                        self.dropdown.selected_index = index
                        self.doIt()
                    return True  # Evitar que se escriba en el cuadro de texto
        return super().eventFilter(source, event)

    def addDropdownItem(self):
        index = len(self.dropdown.items) + 1
        self.dropdown.addItem(f"Elemento {index}")
        pos = self.textBox.mapToGlobal(QPoint(0, self.textBox.height()))
        self.dropdown.showDropdown(pos)

    def onTextChanged(self, text):
        pos = self.textBox.mapToGlobal(QPoint(0, self.textBox.height()))
        if text:
            if text.lower().startswith("go ") and self.go_enabled:
                command = text[3:]
                self.dropdown.clear()
                if command.lower().startswith("delete "):
                    self.dropdown.addItem("Uso: go delete [alias]")
                    if len(command) > 7:
                        alias = command[7:].replace("[", "").replace("]", "")
                        self.go_module.filterDropdownItems(alias)
                    else:
                        self.go_module.filterDropdownItems("")
                else:
                    self.dropdown.addItem("Uso: go [comando]")
                    self.go_module.filterDropdownItems(command)
            else:
                if not self.dropdown.items:
                    self.dropdown.addItem(f"Ejecutar {text}")
                else:
                    if text.lower() == "exit":
                        self.dropdown.updateItem(0, "Salir del programa")
                    else:
                        self.dropdown.updateItem(0, f"Ejecutar {text}")
            if not self.dropdown.isVisible():
                self.dropdown.showDropdown(pos)
            self.textBox.setFocus()
        else:
            self.dropdown.hideDropdown()

    def onFocusChanged(self, old, new):
        if not self.isAncestorOf(new) and new != self and not self.dropdown.isAncestorOf(new) and not self.settingsWindow.isAncestorOf(new):
            self.settingsWindow.hide()
        elif self.isAncestorOf(new):
            self.textBox.setFocus()

    def doIt(self):
        text = self.textBox.text()
        if text:
            if text.lower() == "exit":
                QApplication.instance().quit()
            elif text.lower() == "hide":
                self.hideWidget()
                return
            elif text.lower().startswith("go ") and self.go_enabled:
                alias = text[3:] if text[3:] else self.getSelectedAlias()
                if text.lower().startswith("go delete "):
                    alias = text[10:]
                    result = self.go_module.deleteAlias(alias)
                    print(result)
                else:
                    self.go_module.executeGoCommand(alias)
            else:
                try:
                    print(f"Ejecutando comando: {text}")
                    subprocess.Popen(text, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
                except Exception as e:
                    print(f"Error al ejecutar '{text}': {e}")
            self.textBox.clear()

    def getSelectedAlias(self):
        """Obtiene el alias del elemento seleccionado en el desplegable."""
        if self.dropdown.items:
            selected_item = self.dropdown.items[self.dropdown.selected_index]
            alias_label = selected_item.layout().itemAt(0).widget()
            return alias_label.text().split("\n")[0]
        return ""

    def showEvent(self, event):
        super().showEvent(event)
        self.textBox.setFocus()

        screen = QApplication.primaryScreen()
        if (screen):
            geometry = screen.availableGeometry()
            self.move(
                geometry.left() + (geometry.width() - self.width()) // 2,
                geometry.top() + (geometry.height() - self.height()) // 2
            )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        
        brush = QBrush(QColor(50, 50, 50, 200))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)

    def showWidget(self):
        """Función para mostrar el widget y enfocar el input."""
        self.show()
        self.activateWindow()
        QTimer.singleShot(500, lambda: self.textBox.setFocus())

    def hideWidget(self):
        """Función para ocultar el widget."""
        self.hide()
        if self.dropdown.isVisible():
            self.dropdown.hideDropdown()

    def showSettings(self):
        self.settingsWindow.show()
        self.settingsWindow.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TranslucentWidget()
    widget.show()  # Asegúrate de que el widget esté visible al inicio
    sys.exit(app.exec_())

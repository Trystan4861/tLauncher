import subprocess
import json
import os
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QIcon, QCursor
from dropdown import Dropdown
from tray import TrayIcon
from notification import Notification

class TranslucentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.trayIcon = TrayIcon(self)
        QApplication.instance().focusChanged.connect(self.onFocusChanged)
        self.go_data = self.loadGoData()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(450, 120)

        layout = QVBoxLayout()

        self.settingsButton = QPushButton(self)
        self.settingsButton.setIcon(QIcon("settings-icon.png"))
        self.settingsButton.setFixedSize(40, 40)
        self.settingsButton.clicked.connect(self.addDropdownItem)

        self.textBox = QLineEdit(self)
        self.textBox.setPlaceholderText("Escribe aquí...")
        self.textBox.setFixedSize(420, 65)
        self.textBox.textChanged.connect(self.onTextChanged)

        self.dropdown = Dropdown(self, input_widget=self.textBox)
        self.dropdown.setFixedWidth(self.textBox.width())

        layout.addWidget(self.settingsButton, alignment=Qt.AlignRight | Qt.AlignTop)
        layout.addWidget(self.textBox, alignment=Qt.AlignCenter)
        layout.setContentsMargins(10, 0, 10, 10)

        self.setLayout(layout)

    def loadGoData(self):
        if os.path.exists("go.json"):
            with open("go.json", "r") as file:
                return json.load(file)
        return {}

    def saveGoData(self):
        with open("go.json", "w") as file:
            json.dump(self.go_data, file, indent=4)

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

    def addDropdownItem(self):
        index = len(self.dropdown.items) + 1
        self.dropdown.addItem(f"Elemento {index}")
        pos = self.textBox.mapToGlobal(QPoint(0, self.textBox.height()))
        self.dropdown.showDropdown(pos)

    def onTextChanged(self, text):
        pos = self.textBox.mapToGlobal(QPoint(0, self.textBox.height()))
        if text:
            if text.lower().startswith("go "):
                command = text[3:]
                if command.startswith("add "):
                    parts = command[4:].split(" ")
                    if len(parts) == 2 and parts[0].startswith("[") and parts[0].endswith("]") and parts[1].startswith("(") and parts[1].endswith(")"):
                        alias = parts[0][1:-1]
                        url = parts[1][1:-1]
                        self.go_data[alias] = url
                        self.saveGoData()
                        self.dropdown.clear()
                        self.dropdown.addItem(f"Alias '{alias}' agregado con URL '{url}'")
                    else:
                        self.dropdown.clear()
                        self.dropdown.addItem("Formato incorrecto. Use 'go add [alias] (url)'")
                else:
                    self.filterDropdownItems(command)
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

    def filterDropdownItems(self, filter_text):
        """Filtra los elementos del desplegable que concuerden con el texto del filtro."""
        self.dropdown.clear()
        if self.go_data:
            for alias, url in self.go_data.items():
                if filter_text.lower() in alias.lower():
                    self.dropdown.addItem(f"{alias}\n{url}")
            if not self.dropdown.items:
                self.dropdown.addItem(f"No se encontró el alias '{filter_text}'. Use 'go add [{filter_text}] (url)' para crearlo.")
        else:
            self.dropdown.addItem("No existen alias, cree uno con 'go add [alias] (url)'")

    def onFocusChanged(self, old, new):
        if not self.isAncestorOf(new) and new != self and not self.dropdown.isAncestorOf(new):
            self.hideWidget()

    def doIt(self):
        text = self.textBox.text()
        if text:
            if text.lower() == "exit":
                QApplication.instance().quit()
            elif text.lower().startswith("go "):
                alias = text[3:] if text[3:] else self.getSelectedAlias()
                if alias in self.go_data:
                    url = self.go_data[alias]
                    try:
                        subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
                        notification = Notification(f"Abriendo {url}", 3000, self)
                        notification.showNotification()
                    except Exception as e:
                        print(f"Error al abrir '{url}': {e}")
                else:
                    if self.dropdown.items and "No se encontró el alias" not in self.dropdown.items[0].layout().itemAt(0).widget().text():
                        alias = self.getSelectedAlias()
                        url = self.go_data[alias]
                        try:
                            subprocess.Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, start_new_session=True)
                            notification = Notification(f"Abriendo {url}", 3000, self)
                            notification.showNotification()
                        except Exception as e:
                            print(f"Error al abrir '{url}': {e}")
                    else:
                        print(f"No se encontró el alias '{alias}'")
            else:
                try:
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

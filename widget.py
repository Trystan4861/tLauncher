import subprocess
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QIcon, QCursor
from dropdown import Dropdown
from tray import TrayIcon

class TranslucentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.trayIcon = TrayIcon(self)
        QApplication.instance().focusChanged.connect(self.onFocusChanged)

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

        self.dropdown = Dropdown(self,input_widget=self.textBox)
        self.dropdown.setFixedWidth(self.textBox.width())

        layout.addWidget(self.settingsButton, alignment=Qt.AlignRight | Qt.AlignTop)
        layout.addWidget(self.textBox, alignment=Qt.AlignCenter)
        layout.setContentsMargins(10, 0, 10, 10)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
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
            if not self.dropdown.items:
                self.dropdown.addItem(f"Ejecutar {text}")
            else:
                self.dropdown.updateItem(0, f"Ejecutar {text}")
            if not self.dropdown.isVisible():
                self.dropdown.showDropdown(pos)
            self.textBox.setFocus()
        else:
            self.dropdown.hideDropdown()

    def onFocusChanged(self, old, new):
        if not self.isAncestorOf(new) and new != self and not self.dropdown.isAncestorOf(new):
            self.hide()

    def doIt(self):
        text = self.textBox.text()
        if text:
            if text.lower() == "exit":
                QApplication.instance().quit()
            else:
                try:
                    subprocess.Popen(text,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL,start_new_session=True)
                except Exception as e:
                    print(f"Error al ejecutar '{text}': {e}")
                self.textBox.clear()

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

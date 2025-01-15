from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QApplication
from PyQt5.QtGui import QPainter, QBrush, QColor, QIcon
from dropdown import Dropdown

class TranslucentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        QApplication.instance().focusChanged.connect(self.onFocusChanged)

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(450, 120)

        # Estilo directo para asegurar la transparencia
        #self.setStyleSheet("background-color: rgba(30, 30, 30, 180); border-radius: 0px;")

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
            if not self.dropdown.isVisible():  # Verifica si el desplegable no está visible
                self.dropdown.showDropdown(pos)
            self.textBox.setFocus()
        else:
            self.dropdown.hideDropdown()

    def onFocusChanged(self, old, new):
        # Evitar cierre si el nuevo foco está en el desplegable
        if not self.isAncestorOf(new) and new != self and not self.dropdown.isAncestorOf(new):
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def showEvent(self, event):
        super().showEvent(event)
        self.textBox.setFocus()

        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            self.move(
                geometry.left() + (geometry.width() - self.width()) // 2,
                geometry.top() + (geometry.height() - self.height()) // 2
            )
    def paintEvent(self, event):
        # Crear bordes redondeados y fondo translúcido
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        
        brush = QBrush(QColor(50, 50, 50, 200))  # Fondo translúcido
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)
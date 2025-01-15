from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor
import configparser

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(400, 300)
        self.setStyleSheet(self.loadStyles())

        layout = QVBoxLayout()

        header_layout = QHBoxLayout()
        self.titleLabel = QLabel("Configuraciones", self)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.titleLabel)

        self.closeButton = QPushButton("X", self)
        self.closeButton.clicked.connect(self.closeSettings)
        header_layout.addWidget(self.closeButton, alignment=Qt.AlignRight | Qt.AlignTop)

        layout.addLayout(header_layout)

        self.goCheckbox = QCheckBox("Habilitar módulo 'go'", self)
        layout.addWidget(self.goCheckbox)

        button_layout = QHBoxLayout()
        self.acceptButton = QPushButton("Aceptar", self)
        self.acceptButton.clicked.connect(self.saveSettings)
        self.cancelButton = QPushButton("Cancelar", self)
        self.cancelButton.clicked.connect(self.closeSettings)
        button_layout.addWidget(self.acceptButton)
        button_layout.addWidget(self.cancelButton)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.loadSettings()

    def loadStyles(self):
        try:
            with open("style_settings.qss", "r") as f:
                return f.read()
        except FileNotFoundError:
            print("Error: style_settings.qss no encontrado. Asegúrate de que el archivo existe.")
            return ""

    def closeSettings(self):
        self.hide()
        if self.parent():
            self.parent().setFocus()

    def saveSettings(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config["go"]["enabled"] = str(self.goCheckbox.isChecked())
        with open("config.ini", "w") as configfile:
            config.write(configfile)
        self.parent().updateGoModule(self.goCheckbox.isChecked())
        self.closeSettings()

    def loadSettings(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.goCheckbox.setChecked(config.getboolean("go", "enabled"))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        
        brush = QBrush(QColor(50, 50, 50))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)


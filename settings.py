from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor

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
        self.setLayout(layout)

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

 
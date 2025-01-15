from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setFixedSize(400, 300)
        self.setStyleSheet(self.loadStyles())

        layout = QVBoxLayout()

        self.titleLabel = QLabel("Configuraciones", self)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.titleLabel)

        self.closeButton = QPushButton("X", self)
        self.closeButton.clicked.connect(self.close)
        layout.addWidget(self.closeButton, alignment=Qt.AlignRight)

        self.setLayout(layout)

    def loadStyles(self):
        try:
            with open("styles_settings.qss", "r") as f:
                return f.read()
        except FileNotFoundError:
            print("Error: styles_settings.qss no encontrado. Asegúrate de que el archivo existe.")
            return ""

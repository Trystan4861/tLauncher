"""Módulo principal del plugin de alertas."""
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor

# JSON de ejemplo para el plugin
PLUGIN_INFO_TEMPLATE = {
    "plugin": {
        "name": "AlertPlugin",
        "version": "0.1",
        "author": "@trystan4861",
        "description": "Muestra alertas y notificaciones.",
        "default_keyword": "alert"
    }
}

class AlertDialog(QDialog):
    """Diálogo de alerta personalizado."""
    def __init__(self, message, parent=None, with_button=True, timeout=None, min_width=300, min_height=150, font_size=16):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setModal(True)
        self.setMinimumSize(min_width, min_height)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: rgba(50, 50, 50, 200);
                border-radius: 15px;
            }}
            QLabel {{
                color: white;
                font-size: {font_size}px;
                padding: 10px;
                text-align: center;
            }}
            QPushButton {{
                background-color: #5a5a5a;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #7a7a7a;
            }}
        """)

        layout = QVBoxLayout()

        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        if with_button:
            button = QPushButton("Aceptar")
            button.clicked.connect(self.accept)
            layout.addWidget(button)
        elif timeout:
            QTimer.singleShot(timeout, self.accept)

        self.setLayout(layout)

        # Centrar el diálogo sobre el widget padre
        if parent:
            self.move(parent.frameGeometry().center() - self.rect().center())

    def paintEvent(self, event):  # pylint: disable=invalid-name, unused-argument
        """Evento de pintado del diálogo."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        brush = QBrush(QColor(50, 50, 50, 200))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)

def show_alert(message, parent=None, with_button=True, timeout=None, min_width=300, min_height=150, font_size=16):
    """Muestra una alerta con un mensaje."""
    if timeout and with_button:
        with_button = False
    dialog = AlertDialog(message, parent, with_button, timeout, min_width, min_height, font_size)
    dialog.exec_()

def execute(command, parent=None, **kwargs):
    """Ejecuta un comando."""
    parts = command.split(" ", 1)
    if len(parts) == 2:
        if parts[0] == "alert":
            show_alert(parts[1], parent, **kwargs)
        elif parts[0] == "notify":
            show_alert(parts[1], parent, with_button=False, timeout=3000, **kwargs)

def get_plugin_info():
    """Obtiene la información del plugin."""
    return json.dumps(PLUGIN_INFO_TEMPLATE)

def interact(feedback):
    """Interactúa con el usuario."""
    response = {
        "interaction": {
            "message": f"Received feedback: {feedback}",
            "placeholder": "Escribe tu mensaje...",
            "dropdown_items": []
        }
    }
    return json.dumps(response)

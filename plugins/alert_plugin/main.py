"""Módulo principal del plugin de alertas."""
import json
import os
import yaml
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont

def load_plugin_info():
    """Carga la información del plugin desde plugin.yaml."""
    with open(os.path.join(os.path.dirname(__file__), "plugin.yaml"), "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

PLUGIN_INFO_TEMPLATE = load_plugin_info()
# JSON de ejemplo para el plugin
class AlertDialog(QDialog):
    """Diálogo de alerta personalizado."""
    def __init__(self, message, parent=None, button_options=None, timeout=None, min_width=300, min_height=150, font_size=16):
        super().__init__(parent)
        self.setMinimumSize(min_width, min_height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        
        label = QLabel(message)
        label.setAlignment(Qt.AlignCenter)  # Centrar el texto horizontalmente
        font = QFont()
        font.setPointSize(font_size)
        label.setFont(font)
        layout.addWidget(label)

        if button_options is None:
            button_options = {
                "accept_button": True,
                "cancel_button": False,
                "text_accept": "Aceptar",
                "text_cancel": "Cancelar"
            }

        accept_button = button_options.get("accept_button", True)
        cancel_button = button_options.get("cancel_button", False)
        text_accept = button_options.get("text_accept", "Aceptar")
        text_cancel = button_options.get("text_cancel", "Cancelar")

        if accept_button:
            button_accept = QPushButton(text_accept)
            button_accept.clicked.connect(self.accept)
            layout.addWidget(button_accept)

        if cancel_button:
            button_cancel = QPushButton(text_cancel)
            button_cancel.clicked.connect(self.reject)
            layout.addWidget(button_cancel)

        if timeout:
            QTimer.singleShot(timeout, self.accept)

        self.setLayout(layout)

        # Centrar el diálogo sobre el widget padre
        if parent:
            self.move(parent.frameGeometry().center() - self.rect().center())

    def accept(self):
        """Aceptar el diálogo."""
        self.result = True
        super().accept()

    def reject(self):
        """Rechazar el diálogo."""
        self.result = False
        super().reject()

    def paintEvent(self, event):  # pylint: disable=invalid-name, unused-argument
        """Evento de pintado del diálogo."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        brush = QBrush(QColor(50, 50, 50, 200))
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)

def show_alert(message, parent=None, button_options=None, timeout=None, min_width=300, min_height=150, font_size=16):
    """Muestra una alerta con un mensaje."""
    if button_options is None:
        button_options = {
            "accept_button": True,
            "cancel_button": False,
            "text_accept": "Aceptar",
            "text_cancel": "Cancelar"
        }

    if timeout and (button_options.get("accept_button", True) or button_options.get("cancel_button", False)):
        button_options["accept_button"] = False
        button_options["cancel_button"] = False

    dialog = AlertDialog(message, parent, button_options, timeout, min_width, min_height, font_size)
    dialog.exec_()
    return dialog.result

def execute(command, parent=None, **kwargs):
    """Ejecuta un comando."""
    parts = command.split(" ", 1)
    if len(parts) == 2 and len(parts[1]) > 0:
        show_alert(parts[1], parent, **kwargs)
    else:
        show_alert("Debes proporcionar un mensaje.", parent, **kwargs)

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

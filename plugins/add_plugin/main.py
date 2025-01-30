"""Módulo principal del plugin de importación de plugins."""
import json
import os
import subprocess
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor

# JSON de ejemplo para el plugin
PLUGIN_INFO_TEMPLATE = {
    "plugin": {
        "name": "addPlugin",
        "version": "0.1",
        "author": "@trystan4861",
        "description": "Importa nuevos plugins desde una URL de Git.",
        "default_keyword": "addplugin"
    }
}

class ImportDialog(QDialog):
    """Diálogo de importación de plugins."""
    def __init__(self, parent=None, min_width=400, min_height=200, font_size=16):
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
            QLineEdit {{
                background-color: #5a5a5a;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: {font_size}px;
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

        self.label = QLabel("Introduce la URL del repositorio Git:")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)

        button_layout = QHBoxLayout()
        self.import_button = QPushButton("Importar")
        self.import_button.clicked.connect(self.import_plugin)
        button_layout.addWidget(self.import_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
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

    def import_plugin(self):
        """Importa un plugin desde la URL proporcionada."""
        url = self.url_input.text().strip()
        if not url:
            self.label.setText("La URL no puede estar vacía.")
            return

        plugin_name = os.path.basename(url).replace(".git", "")
        plugins_path = os.path.join(os.path.dirname(__file__), "..", "..", "plugins")
        plugin_dir = os.path.join(plugins_path, plugin_name)

        if os.path.exists(plugin_dir):
            self.label.setText("El plugin ya está importado.")
            return

        if not self.is_git_installed():
            self.label.setText("Git no está instalado en el sistema.")
            return

        try:
            subprocess.run(["git", "clone", url, plugin_dir], check=True)
            self.label.setText("Plugin importado con éxito.")
        except subprocess.CalledProcessError:
            self.label.setText("Error al importar el plugin. Verifica la URL.")

    def is_git_installed(self):
        """Comprueba si Git está instalado en el sistema."""
        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def show_import_dialog(parent=None, min_width=400, min_height=200, font_size=16):
    """Muestra un diálogo de importación de plugins."""
    dialog = ImportDialog(parent, min_width, min_height, font_size)
    dialog.exec_()

def execute(command, parent=None, **kwargs):
    """Ejecuta un comando."""
    if command:
        show_import_dialog(parent, **kwargs)

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

"""Módulo principal de la interfaz gráfica de usuario."""

import sys
import os
import importlib.util
import functions as f

from PyQt5 import QtWidgets, QtCore
from pywinauto import Application

try:
    from sizes import Sizes
except ImportError:
    from core.ui.sizes import Sizes # type: ignore

PROGRAM_NAME = "tLauncher"
PLUGINS=[]

console = f.console
class TransparentLineEdit(QtWidgets.QLineEdit):
    """Cuadro de texto transparente para introducir comandos."""
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TransparentLineEdit")
        self.setStyleSheet("background: transparent; color: #ffffff; font-weight: bold;")

# pylint: disable=invalid-name
    def keyPressEvent(self, event):
        """Emite una señal cuando se presiona una tecla."""
        super().keyPressEvent(event)
        self.keyPressed.emit(event)
# pylint: enable=invalid-name
class PlaceholderLineEdit(QtWidgets.QLineEdit):
    """Cuadro de texto de solo lectura para mostrar un placeholder."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PlaceholderLineEdit")
        self.setStyleSheet("background: #202020; color: #d0e0e0;")
        self.setReadOnly(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def set_placeholder(self, text):
        """Establece el texto del placeholder."""
        self.setText(text)

class MainWindow(QtWidgets.QMainWindow):
    """Ventana principal de la aplicación."""
    def __init__(self, launcher, get_base_path, hotkey_str):
        super().__init__()
        self.launcher = launcher
        self.hotkey_str = hotkey_str
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle(PROGRAM_NAME)
        self.setGeometry(0, 0, Sizes.Window.WIDTH, Sizes.CommandInput.HEIGHT)
        f.apply_styles(self, get_base_path("resources/styles/main_window.qss"))
        self.load_plugins(get_base_path("plugins/"))
        self.create_widgets()
        f.center_on_screen(self)

    def load_plugins(self, plugins_path):
        """Carga los plugins disponibles en la ruta especificada."""
        for plugin_name in os.listdir(plugins_path):
            plugin_dir = os.path.join(plugins_path, plugin_name)
            main_file = os.path.join(plugin_dir, "main.py")
            if os.path.isdir(plugin_dir) and os.path.isfile(main_file):
                spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}.main", main_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"Loaded plugin: {plugin_name}")

    def create_widgets(self):
        """Crea los widgets de la ventana principal."""
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Contenedor principal
        container = QtWidgets.QWidget()
        command_imput_wrapper = QtWidgets.QStackedLayout()
        command_imput_wrapper.setObjectName("commandInputWrapper")
        container.setFixedSize(800, 80)

        # Cuadro de texto transparente
        self.command_input = TransparentLineEdit()
        self.command_input.setPlaceholderText("Introduce un comando")
        self.command_input.keyPressed.connect(self.handle_key_press)
        command_imput_wrapper.addWidget(self.command_input)

        # Cuadro de texto para placeholder vitaminado
        self.placeholder_input = PlaceholderLineEdit()
        command_imput_wrapper.addWidget(self.placeholder_input)

        container.setLayout(command_imput_wrapper)
        layout.addWidget(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Franja horizontal para mensajes
        self.message_frame = QtWidgets.QFrame()
        self.message_frame.setFixedHeight(27)
        self.message_frame.setStyleSheet("background-color: #202020;")
        self.message_frame.setObjectName("messageFrame")
        self.message_label = QtWidgets.QLabel()
        self.message_label.setFixedHeight(27)
        self.message_label.setStyleSheet("font-weight: bold; color: #fff;")
        self.message_label.setObjectName("messageLabel")
        message_layout = QtWidgets.QHBoxLayout()
        message_layout.setContentsMargins(0, 0, 0, 0)
        message_layout.setSpacing(0)
        message_layout.addWidget(self.message_label)
        self.message_frame.setLayout(message_layout)
        self.message_frame.hide()  # Ocultar inicialmente

        layout.addWidget(self.message_frame)
        central_widget.setLayout(layout)
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

    def show_message(self, text):
        """Muestra un mensaje en la franja horizontal."""
        if text:
            self.message_label.setText(text)
            self.message_frame.show()
        else:
            self.message_frame.hide()
        self.setFixedHeight(self.get_window_height()) # Ajustar tamaño de la ventana

    def get_window_height(self):
        """Obtiene la altura de la ventana."""
        height = Sizes.CommandInput.HEIGHT
        if self.is_message_visible():
            height += Sizes.Message.HEIGHT
        #2DO: si hay elementos en el desplegable aumentar el tamaño por cada elemento
        return height

    def is_message_visible(self):
        """Indica si el mensaje está visible."""
        return self.message_frame.isVisible()

    def execute_command(self):
        """Ejecuta el comando introducido."""
        command,parameters = self.get_command()
        console.info("Command entered: %s %s",command, parameters)
        if command == "hide":
            self.launcher.hide_main_window()
        elif command == "exit":
            self.quit()
        else:
            #2DO: Aquí iría la lógica para ejecutar el comando y mostrar el resultado
            console.info("Executing: %s ",command)
        self.command_input.clear()

    def display(self):
        """Muestra la ventana principal."""
        f.center_on_screen(self)
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.show()
        self.raise_()
        self.activateWindow()
        QtWidgets.QApplication.setActiveWindow(self)
        self.command_input.setFocus()  # Asegurar que el cuadro de texto reciba el foco
        if f.is_compiled():
            executable_path = sys.executable
            Application().connect(path=executable_path).window().set_focus()
        else:
            Application().connect(title=PROGRAM_NAME).window().set_focus()

    def handle_key_press(self, event):
        """Maneja el evento de presionar una tecla."""
        console.info("Key pressed: %s - %s" ,event.text(),event.key())
        if event.key() == QtCore.Qt.Key_Escape:
            self.launcher.hide_main_window()
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.execute_command()
        else:
            #2DO: Aquí iría la lógica para mostrar el placeholder vitaminado
            self.show_message(self.command_input.text())
            self.keyPressEvent(event)

    def get_command(self):
        """Obtiene el comando introducido."""
        parts = self.command_input.text().strip().split(" ",1)
        return [parts[0].lower() or "", parts[1] if len(parts) > 1 else ""]


    def quit(self):
        """Cierra la aplicación."""
        QtWidgets.QApplication.instance().quit()

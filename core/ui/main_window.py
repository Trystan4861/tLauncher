from PyQt5 import QtWidgets, QtGui, QtCore
from .config_window import ConfigWindow
import pythoncom
from pywinauto import Application
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

class TransparentLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TransparentLineEdit")
        self.setStyleSheet("background: transparent; color: #ffffff; font-weight: bold;")

class PlaceholderLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PlaceholderLineEdit")
        self.setStyleSheet("background: #202020; color: #d0e0e0;")
        self.setReadOnly(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def setPlaceholder(self, text):
        self.setText(text)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, launcher, get_base_path, hotkey_str):
        super().__init__()
        self.launcher = launcher
        self.get_base_path = get_base_path
        self.hotkey_str = hotkey_str
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("tLauncher")
        self.setGeometry(100, 100, 800, 80)
        self.apply_styles()
        self.create_widgets()
        self.center_on_screen()

    def create_widgets(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Contenedor principal
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QStackedLayout()
        container.setFixedSize(800, 80)

        # Cuadro de texto transparente
        self.command_input = TransparentLineEdit()
        self.command_input.setPlaceholderText("Introduce un comando")
        self.command_input.returnPressed.connect(self.execute_command)
        container_layout.addWidget(self.command_input)

        # Cuadro de texto para placeholder vitaminado
        self.placeholder_input = PlaceholderLineEdit()
        container_layout.addWidget(self.placeholder_input)

        container.setLayout(container_layout)
        layout.addWidget(container)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def apply_styles(self):
        # Aplicar estilos desde el archivo QSS
        with open(self.get_base_path("resources/styles/main_window.qss"), "r") as style_file:
            self.setStyleSheet(style_file.read())

    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def execute_command(self):
        command = self.command_input.text().strip()
        console.info(f"Command entered: {command}")
        if command == "hide":
            self.launcher.hide_main_window()
        elif command == "exit":
            self.quit()
        else:
            # Aquí iría la lógica para ejecutar el comando y mostrar el resultado
            result = f"Executing: {command}"
            console.info(result)
            print(result)  # Esto se puede cambiar para mostrar el resultado en la interfaz
        self.command_input.clear()

    def open_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.show()

    def display(self):
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.show()
        self.raise_()
        self.activateWindow()
        QtWidgets.QApplication.setActiveWindow(self)
        self.command_input.setFocus()  # Asegurar que el cuadro de texto reciba el foco

        # Inicializar COM en el modo STA antes de utilizar pywinauto
        pythoncom.CoInitialize()

        # Utilizar pywinauto para forzar que la ventana se convierta en la ventana activa
        app = Application().connect(title="tLauncher")
        window = app.window(title="tLauncher")
        window.restore()
        window.set_focus()

        # Desinicializar COM después de utilizar pywinauto
        pythoncom.CoUninitialize()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.launcher.hide_main_window()
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.execute_command()
        else:
            super().keyPressEvent(event)
    
    def quit(self):        
        QtWidgets.QApplication.instance().quit()
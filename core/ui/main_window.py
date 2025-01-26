from PyQt5 import QtWidgets, QtCore
from .config_window import ConfigWindow
from pywinauto import Application
import sys
import functions as f 
from sizes import Sizes

PROGRAM_NAME = "tLauncher"
PLUGINS=[]

console = f.console
class TransparentLineEdit(QtWidgets.QLineEdit):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TransparentLineEdit")
        self.setStyleSheet("background: transparent; color: #ffffff; font-weight: bold;")

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.keyPressed.emit(event)

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
        self.hotkey_str = hotkey_str
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle(PROGRAM_NAME)
        self.setGeometry(0, 0, Sizes.Window.WIDTH, Sizes.CommandInput.HEIGHT)
        f.apply_styles(self, get_base_path("resources/styles/main_window.qss"))
        self.create_widgets()
        f.center_on_screen(self)

    def create_widgets(self):
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
        if text:
            self.message_label.setText(text)
            self.message_frame.show()
        else:
            self.message_frame.hide()
        self.setFixedHeight(self.getWindowHeight()) # Ajustar tamaño de la ventana

    def getWindowHeight(self):
        height = Sizes.CommandInput.HEIGHT
        if self.is_message_visible():
            height += Sizes.Message.HEIGHT
        #TODO: si hay elementos en el desplegable aumentar el tamaño por cada elemento
        return height


    def is_message_visible(self):
        return self.message_frame.isVisible()

    def execute_command(self):
        command,parameters = self.getCommand()
        console.info(f"Command entered: {command} {parameters}")
        if command == "hide":
            self.launcher.hide_main_window()
        elif command == "exit":
            self.quit()
        else:
            #TODO: Aquí iría la lógica para ejecutar el comando y mostrar el resultado
            console.info(f"Executing: {command}")
        self.command_input.clear()

    def open_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.show()

    def display(self):
        self.center_on_screen()
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
        console.info(f"Key pressed: {event.text()} - {event.key()}")
        if event.key() == QtCore.Qt.Key_Escape:
            self.launcher.hide_main_window()
        elif event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.execute_command()
        else:
            #TODO: Aquí iría la lógica para mostrar el placeholder vitaminado
            self.show_message(self.command_input.text())
            self.keyPressEvent(event)

    def getCommand(self):
        parts = self.command_input.text().strip().split(" ",1)
        return [parts[0].lower() or "", parts[1] if len(parts) > 1 else ""]


    def quit(self):        
        QtWidgets.QApplication.instance().quit()
from PyQt5 import QtWidgets, QtGui, QtCore
from .config_window import ConfigWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, get_resource_path):
        super().__init__()
        self.get_resource_path = get_resource_path
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowTitle("tLauncher")
        self.setGeometry(100, 100, 450, 100)
        self.create_widgets()
        self.apply_styles()
        self.center_on_screen()

    def create_widgets(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Contenedor principal
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QGridLayout()
        container.setFixedSize(450, 100)

        # Encabezado con imagen
        self.header = QtWidgets.QLabel()
        self.header.setPixmap(QtGui.QPixmap(self.get_resource_path("resources/images/icons/gears.png")).scaled(20, 20, QtCore.Qt.KeepAspectRatio))
        self.header.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
        container_layout.addWidget(self.header, 0, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        # Cuadro de texto para ingresar comandos
        self.command_input = QtWidgets.QLineEdit()
        self.command_input.setPlaceholderText("Enter command")
        self.command_input.returnPressed.connect(self.execute_command)
        container_layout.addWidget(self.command_input, 1, 0, 1, 2)

        # Selector de comandos (oculto)
        self.command_select = QtWidgets.QComboBox()
        self.command_select.addItems(["1", "2"])
        self.command_select.setVisible(False)
        container_layout.addWidget(self.command_select, 2, 0, 1, 2)

        container.setLayout(container_layout)
        layout.addWidget(container)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def apply_styles(self):
        # Aplicar estilos desde el archivo QSS
        with open(self.get_resource_path("resources/styles/main_window.qss"), "r") as style_file:
            self.setStyleSheet(style_file.read())

    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def execute_command(self):
        command = self.command_input.text().strip()
        if command == "hide":
            self.hide()
        else:
            # Aquí iría la lógica para ejecutar el comando y mostrar el resultado
            result = f"Executing: {command}"
            print(result)  # Esto se puede cambiar para mostrar el resultado en la interfaz
        self.command_input.clear()

    def open_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.show()

    def display(self):
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

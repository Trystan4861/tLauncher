from PyQt5 import QtWidgets
from .config_window import ConfigWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("tLauncher")
        self.create_widgets()

    def create_widgets(self):
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel("tLauncher")
        layout.addWidget(self.label)

        self.launch_button = QtWidgets.QPushButton("Launch Notepad")
        self.launch_button.clicked.connect(self.launch_notepad)
        layout.addWidget(self.launch_button)

        self.config_button = QtWidgets.QPushButton("Configuración")
        self.config_button.clicked.connect(self.open_config)
        layout.addWidget(self.config_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def launch_notepad(self):
        import subprocess
        subprocess.Popen(['notepad.exe'])

    def open_config(self):
        self.config_window = ConfigWindow(self)
        self.config_window.show()

    def show(self):
        self.show()

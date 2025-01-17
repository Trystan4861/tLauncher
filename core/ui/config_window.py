from PyQt5 import QtWidgets

class ConfigWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración")
        self.create_widgets()

    def create_widgets(self):
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Configuración")
        layout.addWidget(self.label)
        # Aquí puedes añadir más widgets de configuración según sea necesario
        self.setLayout(layout)

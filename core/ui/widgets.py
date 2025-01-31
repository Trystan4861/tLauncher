"""Módulo con widgets personalizados para la interfaz gráfica."""
from PyQt5 import QtWidgets, QtCore

class TransparentLineEdit(QtWidgets.QLineEdit):
    """Cuadro de texto transparente para introducir comandos."""
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TransparentLineEdit")
        self.setStyleSheet("background: transparent; color: #ffffff; font-weight: bold;")

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Emite una señal cuando se presiona una tecla."""
        super().keyPressEvent(event)
        self.keyPressed.emit(event)

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

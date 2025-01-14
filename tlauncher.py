'''
Nombre del Programa: tLauncher
Descripción: Programa alternativo a ulauncher para Windows
Versión: v1.0.6
Autor: @trystan4861

Log de Actualizaciones:
v1.0.6 - 14/01/2025 19:45:
* Fix: Se corrigió el cierre del programa al perder el foco utilizando un monitor global de foco.
v1.0.5 - 14/01/2025 19:30:
* New: La ventana ahora se posiciona automáticamente en el monitor 1 o centrada en la pantalla activa.
v1.0.4 - 14/01/2025 19:00:
* New: Se agregó la funcionalidad de cierre automático al perder el foco.
v1.0.3 - 14/01/2025 18:30:
* New: Aumentado el tamaño del cuadro de texto a 55px de alto.
* New: Agregado un desplegable oculto debajo del cuadro de texto con funciones para agregar y eliminar elementos, y manejo de clics.
v1.0.2 - 14/01/2025 18:00:
* Change: Ajuste del tamaño del widget a 450x120 y del cuadro de texto a 420x50.
v1.0.1 - 14/01/2025 17:40:
* New: Cambio del botón para mostrar un icono, tamaño ajustado.
* New: Cuadro de texto central agregado.
* New: Respuesta a teclas ESC y ENTER implementada.
* New: Configuración inicial para enfoque al cuadro de texto.
v1.0.0 - 14/01/2025 17:20:
* New: Creación inicial del widget translúcido con cierre.
'''

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QScrollArea, QVBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QBrush, QColor, QIcon

class TranslucentWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Monitorear cambios de foco global
        QApplication.instance().focusChanged.connect(self.onFocusChanged)

    def initUI(self):
        # Configuración general del widget
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(450, 120)

        # Crear layout principal
        layout = QVBoxLayout()

        # Crear botón de configuración
        settingsButton = QPushButton(self)
        settingsButton.setIcon(QIcon("settings-icon.png"))
        settingsButton.setIconSize(settingsButton.size())
        settingsButton.setFixedSize(40, 40)
        settingsButton.setStyleSheet(
            "QPushButton {"
            "    border: none;"
            "    border-radius: 20px;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgba(255, 255, 255, 0.2);"
            "}"
        )
        settingsButton.clicked.connect(self.showPrefs)

        # Crear cuadro de texto central
        self.textBox = QLineEdit(self)
        self.textBox.setPlaceholderText("Escribe aquí...")
        self.textBox.setFixedSize(420, 55)
        self.textBox.setStyleSheet(
            "QLineEdit {"
            "    margin: 10px;"
            "    font-size: 16px;"
            "    border-radius: 10px;"
            "    background-color: rgba(255, 255, 255, 0.8);"
            "    padding: 10px;"
            "}"
        )

        # Crear área de despliegue
        self.dropdownArea = QScrollArea(self)
        self.dropdownArea.setFixedSize(420, 0)
        self.dropdownArea.setStyleSheet(
            "QScrollArea {"
            "    border: none;"
            "    background-color: rgba(255, 255, 255, 0.9);"
            "    border-radius: 10px;"
            "}"
        )
        self.dropdownArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dropdownArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.dropdownContent = QWidget()
        self.dropdownLayout = QVBoxLayout(self.dropdownContent)
        self.dropdownLayout.setContentsMargins(0, 0, 0, 0)
        self.dropdownArea.setWidget(self.dropdownContent)
        self.dropdownArea.setWidgetResizable(True)

        # Añadir elementos al layout
        layout.addWidget(settingsButton, alignment=Qt.AlignRight | Qt.AlignTop)
        layout.addWidget(self.textBox, alignment=Qt.AlignCenter)
        layout.addWidget(self.dropdownArea, alignment=Qt.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)

        self.setLayout(layout)

    def showPrefs(self):
        self.clearDropdown()
        for i in range(5):
            self.addDropdownItem(f"Elemento {i + 1}")
        self.dropdownArea.setFixedHeight(200)  # Mostrar desplegable con 5 elementos
        QMessageBox.information(self, "Info", "showPrefs")
        self.close()

    def addDropdownItem(self, text):
        label = QLabel(text, self.dropdownContent)
        label.setStyleSheet(
            "QLabel {"
            "    background-color: rgba(200, 200, 200, 0.8);"
            "    border: none;"
            "    padding: 5px;"
            "    margin: 1px;"
            "    border-radius: 5px;"
            "}"
        )
        label.mousePressEvent = lambda event, idx=len(self.dropdownLayout.children()): self.onItemClicked(idx)
        self.dropdownLayout.addWidget(label)

    def clearDropdown(self):
        while self.dropdownLayout.count():
            child = self.dropdownLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.dropdownArea.setFixedHeight(0)

    def onItemClicked(self, index):
        QMessageBox.information(self, "Item Clicked", f"Índice: {index}")
        self.close()

    def doIt(self):
        QMessageBox.information(self, "Info", "doIt")
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.doIt()

    def onFocusChanged(self, old, new):
        # Cierra el widget si no está enfocado
        if not self.isAncestorOf(new) and new != self:
            self.close()

    def showEvent(self, event):
        super().showEvent(event)
        self.textBox.setFocus()

        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            self.move(
                geometry.left() + (geometry.width() - self.width()) // 2,
                geometry.top() + (geometry.height() - self.height()) // 2
            )

    def paintEvent(self, event):
        # Crear bordes redondeados y fondo translúcido
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        
        brush = QBrush(QColor(50, 50, 50, 200))  # Fondo translúcido
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 15, 15)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = TranslucentWidget()
    widget.show()
    sys.exit(app.exec_())

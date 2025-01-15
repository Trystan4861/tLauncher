'''
Nombre del Programa: Dropdown
Descripción: Clase que implementa un menú desplegable con funcionalidades avanzadas.
Autor: @trystan4861
'''

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QVBoxLayout, QHBoxLayout

class Dropdown(QWidget):
    def __init__(self, parent=None, input_widget=None):
        super().__init__(parent)
        self.input_widget = input_widget
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.loadStyles()

        self.padding = 5
        self.item_height = 40
        self.max_visible_items = 5
        self.items = []  # Lista de widgets de elementos
        self.selected_index = 0

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_area.setWidget(self.scroll_content)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll_area)
        self.updateSize()

    def addItem(self, text):
        """Agrega un nuevo elemento al desplegable."""
        # Widget contenedor (div padre)
        item_widget = QWidget(self.scroll_content)
        item_widget.setFixedSize(
            self.scroll_area.width() - 20,  # Tamaño total del dropdown menos el scroll
            self.item_height
        )

        # Layout interno con display inline-flex
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(0, 0, 0, 0)
        item_layout.setSpacing(0)

        # Div hijo para el texto principal
        text_label = QLabel(item_widget)
        text_label.setFixedSize(
            item_widget.width() - 45,  # Tamaño del elemento menos el tag
            self.item_height
        )
        text_label.setText(text)
        text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Div hijo para el tag (Alt+N)
        tag_label = QLabel(item_widget)
        tag_label.setFixedSize(45, self.item_height)  # Tamaño fijo para el tag
        tag_label.setText(f"Alt+{len(self.items) % 9 + 1}")
        tag_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Agregar hijos al layout del elemento
        item_layout.addWidget(text_label)
        item_layout.addWidget(tag_label)
        item_widget.setLayout(item_layout)

        # Añadir el widget al scroll
        self.items.append(item_widget)
        self.scroll_layout.addWidget(item_widget)

        self.updateSize()
        if len(self.items) == 1:
            self.updateSelection(0)
    def navigateSelection(self, direction):
        """
        Cambia la selección actual hacia arriba o hacia abajo en función de la dirección.
        :param direction: 'up' para mover hacia arriba, 'down' para mover hacia abajo.
        """
        if direction == 'up' and self.selected_index > 0:
            self.selected_index -= 1
            self.updateSelection(self.selected_index)
            self.ensureVisible(self.selected_index)
        elif direction == 'down' and self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.updateSelection(self.selected_index)
            self.ensureVisible(self.selected_index)

    def ensureVisible(self, index):
        """
        Asegura que el elemento en el índice dado sea visible desplazando el scroll si es necesario.
        :param index: Índice del elemento a hacer visible.
        """
        if 0 <= index < len(self.items):
            item_widget = self.items[index]
            # Calcula la posición relativa del elemento
            y_position = item_widget.y()
            if y_position < self.scroll_area.verticalScrollBar().value():
                # El elemento está por encima del área visible, desplaza hacia arriba
                self.scroll_area.verticalScrollBar().setValue(y_position)
            elif y_position + item_widget.height() > (
                self.scroll_area.verticalScrollBar().value() + self.scroll_area.height()
            ):
                # El elemento está por debajo del área visible, desplaza hacia abajo
                self.scroll_area.verticalScrollBar().setValue(
                    y_position + item_widget.height() - self.scroll_area.height()
                )

    def clear(self):
        for item_widget in self.items:
            item_widget.deleteLater()
        self.items = []
        self.updateSize()

    def updateItem(self, index, text):
        """Actualiza el texto del elemento en un índice específico."""
        if 0 <= index < len(self.items):
            item_layout = self.items[index].layout()
            text_label = item_layout.itemAt(0).widget()  # Primer widget es el texto
            text_label.setText(text)

    def updateSize(self):
        """Actualiza el tamaño del desplegable basado en los elementos visibles."""
        if self.input_widget:
            self.scroll_area.setFixedWidth(self.input_widget.width())  # Usa el ancho del cuadro de texto
        visible_count = min(len(self.items), self.max_visible_items)
        total_height = visible_count * self.item_height + self.padding * 2
        self.setFixedSize(self.scroll_area.width(), total_height)

    def showDropdown(self, pos):
        """Muestra el desplegable en una posición específica."""
        adjusted_pos = QPoint(pos.x(), pos.y())
        self.move(adjusted_pos)
        self.show()

    def hideDropdown(self):
        """Oculta el desplegable."""
        self.clear()
        self.hide()

    def onItemClicked(self, index):
        """Maneja el evento de clic en un elemento."""
        self.updateSelection(index)
        parent = self.parent()
        if parent:
            parent.textBox.setFocus()

    def updateSelection(self, index):
        """Actualiza la selección visual de los elementos del desplegable."""
        if 0 <= index < len(self.items):
            for i, item_widget in enumerate(self.items):
                text_label = item_widget.layout().itemAt(0).widget()
                tag_label = item_widget.layout().itemAt(1).widget()
                if i == index:
                    text_label.setProperty("selected", True)
                    tag_label.setProperty("selected", True)
                else:
                    text_label.setProperty("selected", False)
                    tag_label.setProperty("selected", False)
                text_label.setStyleSheet("")  # Aplica el estilo definido en QSS
                tag_label.setStyleSheet("")  # Aplica el estilo definido en QSS
            self.selected_index = index

    def loadStyles(self):
        """Carga estilos desde un archivo QSS."""
        try:
            with open("styles_dd.qss", "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Error: styles_dd.qss no encontrado. Asegúrate de que el archivo existe.")

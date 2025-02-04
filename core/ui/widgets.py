"""Módulo con widgets personalizados para la interfaz gráfica."""
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QIcon, QPixmap, QPainter

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

class SvgIcon(QtCore.QObject):
    """Clase para crear QIcon a partir de texto SVG."""
    def __init__(self, svg_text, fill="#000000", stroke="#ffffff"):
        """
        Inicializa el icono SVG.
        
        Args:
            svg_text (str): Texto del SVG con placeholders {fill} y {stroke}
            fill (str): Color de relleno en formato hex
            stroke (str): Color del trazo en formato hex
        """
        super().__init__()
        self.svg_text = svg_text
        self.fill = fill
        self.stroke = stroke

    def to_qicon(self):
        """Convierte el SVG en un QIcon."""

        # Reemplazar los placeholders con los colores
        svg_data = self.svg_text.format(
            fill=self.fill,
            stroke=self.stroke
        )

        # Crear el renderer SVG
        renderer = QSvgRenderer(svg_data.encode('utf-8'))

        # Crear un pixmap y pintarlo
        pixmap = QPixmap(128, 128)  # Tamaño por defecto
        pixmap.fill(QtCore.Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        return QIcon(pixmap)

class IconButton(QtWidgets.QPushButton):
    """Botón con ícono y/o texto centrado verticalmente."""
    clicked_with_id = QtCore.pyqtSignal(str)  # Señal personalizada que emite el ID

    def __init__(self, button_id, title=None, icon=None, parent=None):
        """
        Inicializa el botón con ícono y/o texto.
        
        Args:
            button_id (str): Identificador único del botón
            title (str, opcional): Texto que se mostrará debajo del ícono
            icon (QIcon, opcional): Ícono que se mostrará en el botón
            parent (QWidget, opcional): Widget padre
        """
        super().__init__(parent)

        if not title and not icon:
            raise ValueError("Debe proporcionarse al menos un título o un ícono")

        self.button_id = button_id

        # Configurar el layout vertical
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(layout)

        # Configurar el ícono si existe
        if icon:
            if isinstance(icon, str):
                icon = SvgIcon(icon).to_qicon()
            self.setIcon(icon)
            self.setIconSize(QtCore.QSize(32, 32))

        # Configurar el texto si existe
        if title:
            self.setText(title)

        # Establecer altura fija
        self.setFixedHeight(80)

        # Configurar el estilo
        self.setStyleSheet("""
            QPushButton {
                text-align: center;
            }
        """)

        # Conectar señal de click
        self.clicked.connect(self._emit_id)

    def _emit_id(self):
        """Emite el ID del botón cuando se hace clic."""
        self.clicked_with_id.emit(self.button_id)


class OptionElement(QtWidgets.QWidget):
    """Widget que simula un elemento option de HTML con título, subtítulo y botones."""
    def __init__(self, titulo="", subtitulo="", botones=None, parent=None):
        super().__init__(parent)
        self.setObjectName("OptionElement")
        self._selected = False

        # Layout principal vertical
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Título
        self.titulo = QtWidgets.QLabel(titulo)
        self.titulo.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
        layout.addWidget(self.titulo)

        # Subtítulo
        self.subtitulo = QtWidgets.QLabel(subtitulo)
        self.subtitulo.setStyleSheet("color: #d0e0e0; font-size: 12px;")
        layout.addWidget(self.subtitulo)

        # Contenedor de botones
        boton_container = QtWidgets.QHBoxLayout()

        # Agregar hasta 3 botones si se proporcionan
        if botones:
            for boton in enumerate(botones[:3]):  # Limitar a 3 botones
                boton_container.addWidget(boton)

        layout.addLayout(boton_container)
        self._update_style()

    @property
    def selected(self):
        """Obtiene el estado de selección."""
        return self._selected

    @selected.setter
    def selected(self, value):
        """Establece el estado de selección y actualiza el estilo."""
        self._selected = value
        self._update_style()

    def _update_style(self):
        """Actualiza el estilo según el estado de selección."""
        base_style = """
            QWidget#OptionElement {
                background-color: %s;
                border-radius: 5px;
                padding: 10px;
                border: 2px solid %s;
            }
        """
        if self._selected:
            self.setStyleSheet(base_style % ('#404040', '#4a9eff'))
            self.titulo.setStyleSheet("color: #4a9eff; font-size: 14px; font-weight: bold;")
        else:
            self.setStyleSheet(base_style % ('#303030', 'transparent'))
            self.titulo.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")

from PyQt5 import QtGui, QtSvg, QtCore
import sys
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

svg_data = """
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <circle cx="32" cy="32" r="32" fill="blue"/>
    <text x="32" y="37" font-size="24" text-anchor="middle" fill="white">SVG</text>
</svg>
"""

def is_compiled():
    return getattr(sys, 'frozen', False)

def svg2icon(svg_data, width=64, height=64):
    svg_renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_data.encode('utf-8')))
    svg_pixmap = QtGui.QPixmap(width, height)
    svg_pixmap.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(svg_pixmap)
    svg_renderer.render(painter)
    painter.end()
    return QtGui.QIcon(svg_pixmap)
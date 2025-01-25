from PyQt5 import QtGui, QtSvg, QtCore
import sys
import logging
import os

import platform

if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl

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

def silent_remove(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    return not os.path.exists(file_path)

def is_already_running(lock_file):
    try:
        if platform.system() == "Windows":
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return False
    except (IOError, OSError):
        return True
    
def create_signal_file(signal_file_path):
    with open(signal_file_path, "w") as signal_file:
        signal_file.write("show")

def check_signal_file(signal_file_path):
    return os.path.exists(signal_file_path) and silent_remove(signal_file_path)

def unlockFile(file):
    if platform.system() == "Windows":
        msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(file, fcntl.LOCK_UN)
    file.close()

def get_base_path(relative_path="", file=__file__):
    base_path = os.path.abspath(os.path.dirname(file))
    if not is_compiled():
        base_path = os.path.abspath(os.path.join(base_path, '..'))
    return os.path.join(base_path, relative_path)

def pathExists(path):
    return os.path.exists(path)

def get_config_value(config, section, key, default_value):
    if not config.has_section(section):
        config.add_section(section)
    if not config.has_option(section, key):
        config.set(section, key, default_value)
        with open(get_base_path("config.ini"), 'w') as configfile:
            config.write(configfile)
    return config.get(section, key)

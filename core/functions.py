import json
import subprocess
from PyQt5 import QtGui, QtSvg, QtCore, QtWidgets
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

def launch_app(app,shell=False,detached=True):
    try:
        subprocess.Popen(app,shell=shell,creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if detached else 0)
        return True
    except Exception as e:
        console.error(f"Error al ejecutar el comando: {e}")
        return False

def center_on_screen(widget):
    screen = QtWidgets.QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    window_geometry = widget.frameGeometry()
    window_geometry.moveCenter(screen_geometry.center())
    widget.move(window_geometry.topLeft())

def apply_styles(widget, style_path):
    with open(style_path, "r") as style_file:
        widget.setStyleSheet(style_file.read())

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

def normalize_json(data):
    if isinstance(data, dict):
        return {k.lower(): v for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_json(i) for i in data]
    else:
        return data
    
def load_config(config_name="config.json",default_config={'hotkey': 'win+space'}):
    config_path = get_base_path(config_name)
    if not pathExists(config_path):
        config = default_config
        with open(config_path, 'w') as configfile:
            json.dump(normalize_json(config), configfile, indent=4)
    else:
        with open(config_path, 'r') as configfile:
            config = normalize_json(json.load(configfile))
    return config
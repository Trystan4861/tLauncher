"""Módulo de funciones auxiliares."""
import json
import subprocess
import sys
import logging
import os
import platform
import importlib.util

from PyQt5 import QtGui, QtSvg, QtCore, QtWidgets

if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl # pylint: disable=import-error

# Configuración del logger
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

def launch_app(app, shell=False, detached=True):
    """
    Lanza una aplicación o comando en un nuevo proceso.

    Args:
        app (str): El comando o aplicación a ejecutar.
        shell (bool): Si se debe ejecutar el comando en el shell.
        detached (bool): Si el proceso debe ser independiente.

    Returns:
        bool: True si el comando se ejecutó correctamente, False en caso contrario.
    """
    try:
        subprocess.Popen(app, shell=shell, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP if detached else 0)
        return True
    except (subprocess.SubprocessError, OSError) as e:
        console.error("Error al ejecutar el comando: %s", e)
        return False

def center_on_screen(widget):
    """
    Centra un widget en la pantalla.

    Args:
        widget (QtWidgets.QWidget): El widget a centrar.
    """
    screen = QtWidgets.QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    window_geometry = widget.frameGeometry()
    window_geometry.moveCenter(screen_geometry.center())
    widget.move(window_geometry.topLeft())

def apply_styles(widget, style_path):
    """
    Aplica estilos desde un archivo QSS a un widget.

    Args:
        widget (QtWidgets.QWidget): El widget al que se aplicarán los estilos.
        style_path (str): La ruta del archivo QSS.
    """
    with open(style_path, "r", encoding="utf-8") as style_file:
        widget.setStyleSheet(style_file.read())

def is_compiled():
    """
    Verifica si la aplicación está compilada.

    Returns:
        bool: True si la aplicación está compilada, False en caso contrario.
    """
    return getattr(sys, 'frozen', False)

def svg2icon(svg_data, width=64, height=64):
    """
    Convierte datos SVG en un ícono de PyQt.

    Args:
        svg_data (str): Los datos SVG.
        width (int): El ancho del ícono.
        height (int): La altura del ícono.

    Returns:
        QtGui.QIcon: El ícono generado.
    """
    svg_renderer = QtSvg.QSvgRenderer(QtCore.QByteArray(svg_data.encode('utf-8')))
    svg_pixmap = QtGui.QPixmap(width, height)
    svg_pixmap.fill(QtCore.Qt.transparent)
    painter = QtGui.QPainter(svg_pixmap)
    svg_renderer.render(painter)
    painter.end()
    return QtGui.QIcon(svg_pixmap)

def silent_remove(file_path):
    """
    Elimina un archivo de manera silenciosa.

    Args:
        file_path (str): La ruta del archivo a eliminar.

    Returns:
        bool: True si el archivo fue eliminado o no existía, False en caso contrario.
    """
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    return not os.path.exists(file_path)

def is_already_running(lock_file):
    """
    Verifica si la aplicación ya está en ejecución.

    Args:
        lock_file (file): El archivo de bloqueo.

    Returns:
        bool: True si la aplicación ya está en ejecución, False en caso contrario.
    """
    try:
        if platform.system() == "Windows":
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return False
    except (IOError, OSError):
        return True
def local_join(elements):
    """
    Enumera los elementos de una lista.

    Args:
        elemts (list): La lista de elementos a enumerar.

    Returns:
        list: La lista de elementos enumerados.
    """
    if len(elements) > 1:
        my_str = ', '.join(elements[:-1]) + ' y ' + elements[-1]
    else:
        my_str = elements[0]
    return my_str

def create_signal_file(signal_file_path):
    """
    Crea un archivo de señal.

    Args:
        signal_file_path (str): La ruta del archivo de señal.
    """
    with open(signal_file_path, "w", encoding="utf-8") as signal_file:
        signal_file.write("show")

def check_signal_file(signal_file_path):
    """
    Verifica si existe un archivo de señal y lo elimina.

    Args:
        signal_file_path (str): La ruta del archivo de señal.

    Returns:
        bool: True si el archivo existía y fue eliminado, False en caso contrario.
    """
    return os.path.exists(signal_file_path) and silent_remove(signal_file_path)

def unlock_file(file):
    """
    Desbloquea un archivo.

    Args:
        file (file): El archivo a desbloquear.
    """
    if platform.system() == "Windows":
        msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        fcntl.flock(file, fcntl.LOCK_UN)
    file.close()

def get_base_path(relative_path="", file=__file__):
    """
    Obtiene la ruta base del archivo actual.

    Args:
        relative_path (str): La ruta relativa a la base.
        file (str): El archivo de referencia.

    Returns:
        str: La ruta base completa.
    """
    base_path = os.path.abspath(os.path.dirname(file))
    if not is_compiled():
        base_path = os.path.abspath(os.path.join(base_path, '..'))
    return os.path.join(base_path, relative_path)

def path_exists(path):
    """
    Verifica si una ruta existe.

    Args:
        path (str): La ruta a verificar.

    Returns:
        bool: True si la ruta existe, False en caso contrario.
    """
    return os.path.exists(path)

def normalize_json(data):
    """
    Normaliza las claves de un JSON a minúsculas.

    Args:
        data (dict or list): El JSON a normalizar.

    Returns:
        dict or list: El JSON con las claves en minúsculas.
    """
    if isinstance(data, dict):
        return {k.lower(): v for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_json(i) for i in data]
    else:
        return data

def load_config(config_name="config.json", default_config=None):
    """
    Carga la configuración desde un archivo JSON.

    Args:
        config_name (str): El nombre del archivo de configuración.
        default_config (dict): La configuración por defecto.

    Returns:
        dict: La configuración cargada.
    """
    if default_config is None:
        default_config = {'hotkey': 'ctr+alt+w', 'plugins': {}} # Configuración por defecto
    config_path = get_base_path(config_name)
    if not path_exists(config_path):
        config = default_config
        with open(config_path, 'w', encoding="utf-8") as configfile:
            json.dump(normalize_json(config), configfile, indent=4)
    else:
        with open(config_path, 'r', encoding="utf-8") as configfile:
            config = normalize_json(json.load(configfile))
    return config

def notify(message, parent=None, button_options=None, timeout=None, min_width=300, min_height=150, font_size=16):
    """
    Muestra una alerta usando el plugin alert_plugin si se encuentra en el sistema.

    Args:
        message (str): El mensaje a mostrar en la alerta.
        parent (QtWidgets.QWidget): El widget padre de la alerta.
        button_options (dict): Opciones para los botones de aceptar y cancelar.
        timeout (int): El tiempo en milisegundos que la alerta debe mostrarse si no tiene botón.
        min_width (int): El ancho mínimo de la alerta.
        min_height (int): La altura mínima de la alerta.
        font_size (int): El tamaño de la letra del mensaje.
    """
    plugin_name = "alert_plugin"
    plugin_dir = os.path.join(get_base_path("plugins"), plugin_name)
    main_file = os.path.join(plugin_dir, "main.py")
    if os.path.isdir(plugin_dir) and os.path.isfile(main_file):
        spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}.main", main_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.show_alert(message, parent, button_options, timeout, min_width, min_height, font_size)
    else:
        console.warning("El plugin alert_plugin no se encuentra en el sistema.")
        return None

def save_json(filepath, data):

    """Guarda un diccionario en un archivo JSON."""

    with open(filepath, 'w', encoding='utf-8') as f:

        json.dump(data, f, ensure_ascii=False, indent=4)

'''
    Nombre: tLauncher
    Descripción: Aplicación que permite ejecutar comandos de forma rápida y sencilla.
    Autor: @trystan4861
    version: 1.1.17
'''
from PyQt5.QtWidgets import QApplication
from widget import TranslucentWidget
import sys
import socket
import json
from threading import Thread

def load_stylesheet(app, path):
    with open(path, "r") as file:
        app.setStyleSheet(file.read())

def is_another_instance_running():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", 65432))
        return False
    except socket.error:
        return True

def notify_existing_instance():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 65432))
    s.sendall(json.dumps({"action": "show"}).encode())
    s.close()

if __name__ == "__main__":
    if is_another_instance_running():
        notify_existing_instance()
        sys.exit(0)

    app = QApplication(sys.argv)
    load_stylesheet(app, "styles/style.qss")
    widget = TranslucentWidget()
    widget.showWidget()  # Asegurar que el input reciba el foco

    def handle_socket_connection():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 65432))
        s.listen(1)
        while True:
            conn, _ = s.accept()
            data = conn.recv(1024)
            message = json.loads(data.decode())
            if message.get("action") == "show":
                widget.showWidget()
            conn.close()

    socket_thread = Thread(target=handle_socket_connection, daemon=True)
    socket_thread.start()

    sys.exit(app.exec_())

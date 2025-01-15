from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QFont

class Notification(QWidget):
    def __init__(self, text, timeout=3000, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet(self.loadStyles())

        layout = QVBoxLayout()
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 12))
        layout.addWidget(self.label)
        self.setLayout(layout)

        QTimer.singleShot(timeout, self.close)

    def loadStyles(self):
        try:
            with open("style_notification.qss", "r") as f:
                return f.read()
        except FileNotFoundError:
            print("Error: style_notification.qss no encontrado. Asegúrate de que el archivo existe.")
            return ""

    def showNotification(self):
        if self.parent():
            parent_rect = self.parent().rect()
            self.move(self.parent().mapToGlobal(parent_rect.center()) - self.rect().center())
        self.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    notification = Notification("Esto es una notificación", 5000)
    notification.showNotification()
    sys.exit(app.exec_())

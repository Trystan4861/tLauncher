from PyQt5.QtWidgets import QApplication
from translucent_widget import TranslucentWidget
import sys

def load_stylesheet(app, path):
    with open(path, "r") as file:
        app.setStyleSheet(file.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    load_stylesheet(app, "styles.qss")
    widget = TranslucentWidget()
    widget.show()
    sys.exit(app.exec_())


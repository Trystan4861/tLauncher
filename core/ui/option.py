"""This module contains the option widget for the main window."""
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt

def labeled_button_with_icon(aQIcon, label_text, width, height, icon_width, icon_height, tooltip_text=""):
    """Creates a button with an icon and a label."""
    button = QPushButton()
    button.setIcon(aQIcon)
    button.setIconSize(QSize(icon_width, icon_height))
    if tooltip_text:
        button.setToolTip(tooltip_text)
    button.setFixedSize(width, height)

    label = QLabel(label_text)
    label.setObjectName("labelButton")
    label.setAlignment(Qt.AlignCenter)

    layout = QVBoxLayout()
    layout.addWidget(button, alignment=Qt.AlignCenter)
    layout.addWidget(label, alignment=Qt.AlignCenter)

    container = QWidget()
    container.setLayout(layout)

    return container

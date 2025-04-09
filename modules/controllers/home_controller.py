from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QStackedWidget
from PySide6.QtCore import Slot


class HomeController:
    def __init__(self, parent=None):
        self.widget = QWidget(parent)
        self.widget.setObjectName(u"home")
        self.widget.setStyleSheet(u"background-image: url(:/images/images/images/PyDracula_vertical.png);\n"
                                "background-position: center;\n"
                                "background-repeat: no-repeat;")
        parent.addWidget(self.widget)
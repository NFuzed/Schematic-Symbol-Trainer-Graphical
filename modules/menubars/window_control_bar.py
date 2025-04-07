from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QIcon, QCursor)
from PySide6.QtWidgets import (QHBoxLayout, QPushButton)

class WindowControlBar(QHBoxLayout):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window

        self.setSpacing(5)
        self.setObjectName(u"horizontalLayout_2")
        self.setContentsMargins(0, 0, 0, 0)

        self.settings_button = self.create_control_button(u"settings_button", u":/icons/images/icons/icon_settings.png", u"Settings")
        self.minimize_button = self.create_control_button(u"minimizeAppBtn", u":/icons/images/icons/icon_minimize.png", u"Minimize")
        self.maximize_button = self.create_control_button(u"maximizeRestoreAppBtn", u":/icons/images/icons/icon_maximize.png", u"Maximize")
        self.close_button = self.create_control_button(u"closeAppBtn", u":/icons/images/icons/icon_close.png", u"Close")


    def create_control_button(self, object_name, image_url, tooltip):
        button = QPushButton(self.parentWidget())
        button.setObjectName(object_name)
        button.setMinimumSize(QSize(28, 28))
        button.setMaximumSize(QSize(28, 28))
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.setText("")
        button.setToolTip(tooltip)
        icon1 = QIcon()
        icon1.addFile(image_url, QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        button.setIcon(icon1)
        button.setIconSize(QSize(20, 20))
        self.addWidget(button)
        return button
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget)

class PageMenuBar(QFrame):
    def __init__(self, sizePolicy, parent=None):
        super().__init__(parent)

        self.sizePolicy = sizePolicy
        self.setObjectName(u"topMenu")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.btn_home = self.create_page_button(u"btn_home", u"background-image: url(:/icons/images/icons/cil-home.png);")
        self.btn_view = self.create_page_button(u"btn_view", u"background-image: url(:/icons/images/icons/cil-satelite.png);")
        self.btn_entities = self.create_page_button(u"btn_entities", u"background-image: url(:/icons/images/icons/cil-3d.png);")
        self.btn_new = self.create_page_button(u"btn_new", u"background-image: url(:/icons/images/icons/cil-file.png);")
        self.btn_save = self.create_page_button(u"btn_save", u"background-image: url(:/icons/images/icons/cil-save.png);")
        self.btn_load = self.create_page_button(u"btn_load", u"background-image: url(:/icons/images/icons/cil-description.png)")
        self.btn_exit = self.create_page_button(u"btn_exit", u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.layout.addWidget(self, 0, Qt.AlignmentFlag.AlignTop)


    def create_page_button(self, object_name, image_url):
        button = QPushButton(self)
        button.setObjectName(object_name)
        self.sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(self.sizePolicy)
        button.setMinimumSize(QSize(0, 45))
        # button.setFont(font)
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        button.setStyleSheet(image_url)

        self.layout.addWidget(button)
        return button


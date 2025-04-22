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

class BottomMenuBar(QFrame):
    def __init__(self, sizePolicy, parent=None):
        super().__init__(parent)

        self.sizePolicy = sizePolicy
        self.setObjectName(u"bottomMenu")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self, 0, Qt.AlignmentFlag.AlignBottom)

    def create_toggle_button(self, object_name, image_url):
        toggle_button = QPushButton(self)
        toggle_button.setObjectName(object_name)
        self.sizePolicy.setHeightForWidth(toggle_button.sizePolicy().hasHeightForWidth())
        toggle_button.setSizePolicy(self.sizePolicy)
        toggle_button.setMinimumSize(QSize(0, 45))
        toggle_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        toggle_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        toggle_button.setStyleSheet(image_url)

        self.layout.addWidget(toggle_button)
        return toggle_button
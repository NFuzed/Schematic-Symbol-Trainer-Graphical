from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal

from src.core import Entity, EntityManager
import numpy as np

from src.utilities.observable import Observable


class EntityDisplayer:
    """Manages an entity display widget (composition pattern)"""

    def __init__(self, entity : Entity, entity_manager : EntityManager):

        self.widget = QFrame()
        self.widget.setFrameShape(QFrame.StyledPanel)
        self.widget.setLineWidth(1)
        self.widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.widget.setFixedSize(220, 220)  # Fixed size for grid alignment
        self.widget.setStyleSheet("")

        layout = QVBoxLayout(self.widget)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.set_image(self.numpy_to_qimage(entity.image))
        layout.addWidget(self.image_label, 1)

        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedHeight(25)
        self.delete_button.clicked.connect(lambda: entity_manager.remove_entity(entity))
        layout.addWidget(self.delete_button)

    def set_image(self, image: QImage):
        """Set the image to display"""
        pixmap = QPixmap.fromImage(image)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(
                200, 200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

    def numpy_to_qimage(self, np_array: np.ndarray):
        """Convert a NumPy array back to QImage"""
        height, width, channel = np_array.shape
        bytes_per_line = 4 * width

        if np_array.dtype != np.uint8:
            np_array = np_array.astype(np.uint8)

        return QImage(
            np_array.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGBA8888
        )

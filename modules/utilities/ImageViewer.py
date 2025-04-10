from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                               QRubberBand, QFileDialog, QVBoxLayout, QHBoxLayout,
                               QWidget, QPushButton, QComboBox, QLabel, QScrollArea)
from PySide6.QtGui import QPixmap, QImage, QPainter
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal, QTime
import numpy as np

class ImageViewer(QGraphicsView):
    image_snipped = Signal(QImage)  # Signal emitted when image is snipped

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.image_item = None
        self.pixmap = None
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        # Selection tools
        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.origin = QPoint()
        self.snip_rect = QRect()
        self.scale_factor = 1.0

        # Configure view
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QPainter.Antialiasing)

    def load_image(self, file_path):
        """Load an image file into the viewer"""
        self.pixmap = QPixmap(file_path)
        if self.pixmap.isNull():
            return False

        self.scene.clear()
        self.image_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.image_item)
        self.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.scale_factor = 1.0
        return True

    def wheelEvent(self, event):
        """Handle zooming with mouse wheel"""
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)
        self.scale_factor *= factor

    def mousePressEvent(self, event):
        """Start selection on right click"""
        if event.button() == Qt.MouseButton.RightButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Update selection rectangle"""
        if self.rubber_band.isVisible():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            if self.rubber_band.isVisible():
                event.accept()
                self.snip_rect = self.rubber_band.geometry()
                self.rubber_band.hide()

                # Only emit if we actually have a valid selection
                if not self.snip_rect.isNull() and self.snip_rect.isValid():
                    self.emit_snipped_image()
            return  # Skip parent handling for right button
        super().mouseReleaseEvent(event)

    def emit_snipped_image(self):
        """Convert selection to QImage and emit signal"""
        print(f"Emitting at {QTime.currentTime().toString('hh:mm:ss.zzz')}")

        if self.pixmap and not self.snip_rect.isNull():
            scene_rect = self.mapToScene(self.snip_rect).boundingRect().toRect()
            snipped_image = self.pixmap.copy(scene_rect).toImage()
            self.image_snipped.emit(snipped_image)

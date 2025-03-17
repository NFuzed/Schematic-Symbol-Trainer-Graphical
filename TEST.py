import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, \
    QRubberBand
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtCore import Qt, QRect, QPoint
from PyQt6.QtCore import QSize



class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.image_item = None
        self.pixmap = None
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.origin = QPoint()
        self.snip_rect = QRect()

        self.scale_factor = 1.0

    def load_image(self, file_path):
        self.pixmap = QPixmap(file_path)
        if self.pixmap.isNull():
            return
        self.scene.clear()
        self.image_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.image_item)
        self.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event):
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)
        self.scale_factor *= factor

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.rubber_band.isVisible():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.rubber_band.isVisible():
            self.snip_rect = self.rubber_band.geometry()
            self.rubber_band.hide()
            self.snip_image()
        super().mouseReleaseEvent(event)

    def snip_image(self):
        if self.pixmap and not self.snip_rect.isNull():
            # Convert scene coordinates to image coordinates
            scene_rect = self.mapToScene(self.snip_rect).boundingRect().toRect()
            cropped_pixmap = self.pixmap.copy(scene_rect)
            cropped_pixmap.save("snipped_image.png")  # Save the cropped region
            print("Snipped image saved as snipped_image.png")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Snipping Tool")
        self.setGeometry(100, 100, 800, 600)

        self.viewer = ImageViewer(self)
        self.setCentralWidget(self.viewer)

        self.open_image()

    def open_image(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open Image File", "",
                                                   "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            self.viewer.load_image(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
import numpy as np
from PySide6.QtGui import QImage

def q_image_to_numpy(q_image: QImage):
    """Convert QImage to numpy array (works in PySide6 6.4+)"""
    q_image = q_image.convertToFormat(QImage.Format.Format_RGBA8888)
    buffer = q_image.constBits()

    arr = np.frombuffer(buffer, dtype=np.uint8).reshape(
        q_image.height(),
        q_image.width(),
        4  # RGBA
    )
    return arr.copy()
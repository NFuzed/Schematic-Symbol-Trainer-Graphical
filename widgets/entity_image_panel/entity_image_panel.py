from PyQt6.QtWidgets import QWidget
from src.core import Entity

class EntityImagePanel(QWidget):
    def __init__(self, entityImage, parent=None):
        super(EntityImagePanel, self).__init__(parent)
        

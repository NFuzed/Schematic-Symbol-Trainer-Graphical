from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                              QRubberBand, QFileDialog, QVBoxLayout, QHBoxLayout,
                              QWidget, QPushButton, QComboBox, QLabel, QScrollArea)
from PySide6.QtGui import QPixmap, QImage, QPainter
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal
from core import Core
import numpy as np

class DiagramController:
    def __init__(self, image_viewer, core: Core, parent=None):
        self.widget = QWidget(parent)
        self.core = core
        parent.addWidget(self.widget)

        # Main components
        self.image_viewer = image_viewer
        self.current_image_path = None

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """Initialize all UI components"""
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(10)

        # Control Panel
        self.setup_control_panel()

        # Image Viewer Area in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_viewer)
        self.main_layout.addWidget(scroll_area, 1)

        # Entity Selection
        self.setup_entity_selection()
        self.register_for_events()

    def setup_control_panel(self):
        """Create the control buttons"""
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        self.load_button = QPushButton("Load Diagram")
        self.load_button.setObjectName("loadButton")
        self.load_button.setFixedSize(120, 30)

        self.save_button = QPushButton("Save Selection")
        self.save_button.setObjectName("saveButton")
        self.save_button.setFixedSize(120, 30)
        self.save_button.setEnabled(False)

        control_layout.addWidget(self.load_button)
        control_layout.addWidget(self.save_button)
        control_layout.addStretch()

        self.main_layout.addWidget(control_panel)

    def setup_entity_selection(self):
        """Setup entity selection dropdown"""
        entity_panel = QWidget()
        entity_layout = QHBoxLayout(entity_panel)

        self.entity_dropdown = QComboBox()
        self.entity_dropdown.setObjectName("entityDropdown")
        self.entity_dropdown.setFixedSize(200, 30)
        self.entity_dropdown.setEnabled(False)

        entity_layout.addWidget(QLabel("Save as Entity:"))
        entity_layout.addWidget(self.entity_dropdown)
        entity_layout.addStretch()

        self.main_layout.addWidget(entity_panel)

    def setup_connections(self):
        """Connect signals to slots"""
        self.load_button.clicked.connect(self.load_diagram)
        self.save_button.clicked.connect(self.save_selection)
        self.image_viewer.image_snipped.connect(self.handle_snipped_image)

    def load_diagram(self):
        """Load an image file into the viewer"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.widget,
            "Open Diagram",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path and self.image_viewer.load_image(file_path):
            self.current_image_path = file_path
            self.save_button.setEnabled(True)
            self.entity_dropdown.setEnabled(True)

    def handle_snipped_image(self, image):
        """Handle the snipped image (connect your custom logic here)"""
        if not image.isNull() and self.entity_dropdown.itemData(self.entity_dropdown.currentIndex()):
            converted_image = self.q_image_to_numpy(image)
            entity_manager = self.entity_dropdown.itemData(self.entity_dropdown.currentIndex())
            entity_manager.create_entity(converted_image)

    def save_selection(self):
        """Trigger image snipping (handled via the image_snipped signal)"""
        # May not be required
        pass

    def set_entities(self, entities):
        """Populate the entity dropdown"""
        self.entity_dropdown.clear()
        self.entity_dropdown.addItems(entities)

    def set_styles(self):
        """Apply Dracula theme styling"""
        self.widget.setStyleSheet("""
            #loadButton, #saveButton {
                background-color: #44475a;
                color: #f8f8f2;
                border: 1px solid #6272a4;
                border-radius: 4px;
            }
            #loadButton:hover, #saveButton:hover {
                background-color: #6272a4;
            }
            #loadButton:pressed, #saveButton:pressed {
                background-color: #ff79c6;
                color: #282a36;
            }
            #entityDropdown {
                background-color: #44475a;
                color: #f8f8f2;
                border: 1px solid #6272a4;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                color: #bd93f9;
            }
            QScrollArea {
                background-color: #282a36;
                border: 1px solid #44475a;
            }
        """)

    def register_for_events(self):
        """Connect to entity manager changes"""
        self.core.database.created_entity_manager_observer.bind(self._add_entity_to_dropdown)
        self.core.database.destroyed_entity_manager_observer.bind(self._remove_entity_from_dropdown)

    def _add_entity_to_dropdown(self, entity_manager):
        """Add an entity to the dropdown"""
        self.entity_dropdown.addItem(entity_manager.entity_manager_name, entity_manager)

    def _remove_entity_from_dropdown(self, entity_manager):
        """Remove an entity from the dropdown"""
        index = self._find_entity_index(entity_manager)
        if index >= 0:
            self.entity_dropdown.removeItem(index)

    def _find_entity_index(self, entity_manager):
        """Find the combo box index for an entity manager"""
        for i in range(self.entity_dropdown.count()):
            if self.entity_dropdown.itemData(i) == entity_manager:
                return i
        return -1

    def get_current_entity(self):
        """Get the currently selected entity manager"""
        if self.entity_dropdown.currentIndex() >= 0:
            return self.entity_dropdown.itemData(self.entity_dropdown.currentIndex())
        return None

    def q_image_to_numpy(self, q_image: QImage):
        """Convert QImage to numpy array (works in PySide6 6.4+)"""
        q_image = q_image.convertToFormat(QImage.Format.Format_RGBA8888)
        buffer = q_image.constBits()

        arr = np.frombuffer(buffer, dtype=np.uint8).reshape(
            q_image.height(),
            q_image.width(),
            4  # RGBA
        )
        return arr.copy()
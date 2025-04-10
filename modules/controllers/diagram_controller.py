from PySide6.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                              QRubberBand, QFileDialog, QVBoxLayout, QHBoxLayout,
                              QWidget, QPushButton, QComboBox, QLabel, QScrollArea)
from PySide6.QtGui import QPixmap, QImage, QPainter
from PySide6.QtCore import Qt, QRect, QPoint, QSize, Signal

class DiagramController:
    def __init__(self, image_viewer, parent=None):
        self.widget = QWidget(parent)
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
        if not image.isNull() and self.entity_dropdown.currentText():
            entity_name = self.entity_dropdown.currentText()
            print(f"Processing snipped image for entity: {entity_name}")
            #todo: handle the QImage as needed

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
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLineEdit, QLabel, QTabWidget, QFileDialog, QSizePolicy, QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from core import Core
from ..utilities import style_sheet_loader, ImageViewer
from ..utilities.entity_drop_down_selector import EntityDropDownSelector
from ..utilities import image_numpy_converter
import os

class DiagramController:
    def __init__(self, core: Core, parent=None):
        self.core = core
        self.widget = QWidget(parent)
        parent.addWidget(self.widget)

        self.image_path_to_viewer : dict[str, ImageViewer]= {}
        self.viewer_to_image_path : dict[ImageViewer, str]= {}

        self.tab_widget = QTabWidget()
        self.add_button = QPushButton("Add Diagram")
        self.add_batch_button = QPushButton("Add Batch Diagrams")
        self.remove_diagram = QPushButton("Remove Diagram")
        self.clear_diagrams = QPushButton("Clear Diagrams")

        self.entity_dropdown = EntityDropDownSelector(core)

        self.setup_ui()
        self.setup_connections()
        style_sheet_loader.load_style_sheet("diagram_page.qss", self.widget)

        self.register_subscriptions()

    def setup_ui(self):
        self.widget.setObjectName("diagramController")
        main_layout = QVBoxLayout(self.widget)

        self.add_button.setObjectName("diagram_buttons")
        self.add_batch_button.setObjectName("diagram_buttons")
        self.remove_diagram.setObjectName("diagram_buttons")
        self.clear_diagrams.setObjectName("diagram_buttons")

        title_panel = QHBoxLayout()
        title_label = QLabel("DIAGRAMS")
        title_label.setObjectName("title_label")
        title_panel.addWidget(title_label)

        # Top section
        entity_layout = QHBoxLayout()
        entity_layout.addWidget(QLabel("Save as Entity:"))
        entity_layout.addWidget(self.entity_dropdown.widget)
        entity_layout.addStretch()

        top_panel = QWidget()
        top_layout = QGridLayout(top_panel)
        top_layout.setContentsMargins(5, 5, 5, 5)

        entity_widget = QWidget()
        entity_widget.setLayout(entity_layout)
        top_layout.addWidget(entity_widget, 1, 0, 1, 4)
        top_layout.addWidget(self.add_button, 0, 0)
        top_layout.addWidget(self.add_batch_button, 0, 1)
        top_layout.addWidget(self.remove_diagram, 0, 2)
        top_layout.addWidget(self.clear_diagrams, 0, 3)

        # Tab content area
        self.tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add everything to main layout
        main_layout.addLayout(title_panel)
        main_layout.addWidget(top_panel)
        main_layout.addWidget(self.tab_widget)

    def setup_connections(self):
        self.add_button.clicked.connect(self.add_diagram)
        self.add_batch_button.clicked.connect(self.add_batch_diagrams)
        self.remove_diagram.clicked.connect(self.remove_current_diagram)
        self.clear_diagrams.clicked.connect(self.clear_all_diagrams)

    def remove_current_diagram(self):
        if isinstance(self.tab_widget.currentWidget(), ImageViewer):
            image : ImageViewer = self.tab_widget.currentWidget()
            self.core.database.diagrams.remove_diagram(self.viewer_to_image_path.get(image))

    def clear_all_diagrams(self):
        self.core.database.diagrams.clear_diagrams()

    def add_diagram(self):
        file_path, _ = QFileDialog.getOpenFileName(self.widget, "Select Diagram", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            self.core.database.diagrams.add_diagram(file_path)

    def add_batch_diagrams(self):
        folder_path = QFileDialog.getExistingDirectory(self.widget, "Select Folder")
        if folder_path:
            import os
            for f in os.listdir(folder_path):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    self.core.database.diagrams.add_diagram(os.path.join(folder_path, f))

    def register_subscriptions(self):
        self.core.database.diagrams.added_diagram_observer.bind(self.create_tab)
        self.core.database.diagrams.deleted_diagram_observer.bind(self.remove_tab)

    def remove_tab(self, image_file_path):
        widget = self.image_path_to_viewer.get(image_file_path)
        if widget is None:
            return

        index = self.tab_widget.indexOf(widget)
        if index >= 0:
            self.tab_widget.removeTab(index)

        self.viewer_to_image_path.pop(widget)
        self.image_path_to_viewer.pop(image_file_path)

    def create_tab(self, image_file_path):
        if image_file_path in self.image_path_to_viewer:
            return

        pixmap = QPixmap(image_file_path)
        if pixmap.isNull():
            self.core.database.diagrams.remove_diagram(image_file_path)
            return

        image_viewer = ImageViewer(pixmap, self.tab_widget)
        image_viewer.image_snipped.connect(self.handle_snipped_image)
        self.image_path_to_viewer[image_file_path] = image_viewer
        self.viewer_to_image_path[image_viewer] = image_file_path
        self.tab_widget.addTab(image_viewer, os.path.basename(image_file_path))

    def handle_snipped_image(self, image):
        """Handle the snipped image (connect your custom logic here)"""
        if not image.isNull() and self.entity_dropdown.widget.itemData(self.entity_dropdown.widget.currentIndex()):
            converted_image = image_numpy_converter.q_image_to_numpy(image)
            entity_manager = self.entity_dropdown.widget.itemData(self.entity_dropdown.widget.currentIndex())
            entity_manager.create_entity(converted_image)
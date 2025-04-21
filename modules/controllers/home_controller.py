from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QGroupBox,
    QScrollArea, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from ..utilities import style_sheet_loader

class HomeController:
    def __init__(self, parent=None):
        self.widget = QWidget(parent)
        self.setup_ui()
        parent.addWidget(self.widget)

    def setup_ui(self):
        style_sheet_loader.load_style_sheet("home_page.qss", self.widget)

        main_layout = QHBoxLayout(self.widget)

        # Left side layout (Entity managers + optional bottom panel)
        left_panel = QVBoxLayout()

        # Entity Manager List
        self.entity_group = QGroupBox("ENTITIES")
        entity_layout = QVBoxLayout()
        self.entity_list = QListWidget()
        entity_layout.addWidget(self.entity_list)
        self.entity_group.setLayout(entity_layout)
        left_panel.addWidget(self.entity_group)

        # Placeholder bottom left panel (could be logs, recent actions, diagram preview, etc.)
        self.bottom_left_group = QGroupBox()
        self.bottom_left_group.setMinimumHeight(200)
        self.bottom_left_group.setTitle("LOGS")
        self.bottom_left_group.setLayout(QVBoxLayout())
        left_panel.addWidget(self.bottom_left_group)

        main_layout.addLayout(left_panel, 2)

        # Right side layout (Model Configuration)
        right_panel = QVBoxLayout()
        self.config_group = QGroupBox("MODEL CONFIGURATION")
        config_layout = QVBoxLayout()
        self.config_group.setLayout(config_layout)
        right_panel.addWidget(self.config_group, stretch=1)

        # Buttons section
        button_grid = QGridLayout()

        self.import_button = QPushButton("Import")
        self.new_button = QPushButton("New")
        self.analysis_button = QPushButton("Analysis")
        self.train_button = QPushButton("Train")
        self.validate_button = QPushButton("Validate")
        self.run_button = QPushButton("Run")
        self.run_batch_button = QPushButton("Run Batch")
        self.export_button = QPushButton("Export")

        button_grid.addWidget(self.new_button, 0, 0, 1, 2)
        button_grid.addWidget(self.import_button, 0, 2, 1, 2)
        button_grid.addWidget(self.export_button, 0, 4, 1, 2)
        button_grid.addWidget(self.train_button, 1, 0, 1, 3)
        button_grid.addWidget(self.validate_button, 1, 3, 1, 3)
        button_grid.addWidget(self.run_button, 2, 0, 1, 3)
        button_grid.addWidget(self.run_batch_button, 2, 3, 1, 3)
        button_grid.addWidget(self.analysis_button, 3, 0, 1, 6)

        right_panel.addLayout(button_grid)
        main_layout.addLayout(right_panel, 3)

    def add_entity_manager(self, name: str, count: int):
        item = QListWidgetItem(f"{name}\t{count}")
        self.entity_list.addItem(item)

    def set_bottom_left_content(self, widget: QWidget):
        layout = self.bottom_left_group.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        layout.addWidget(widget)
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
        self.entity_group = QGroupBox("Entities")
        entity_layout = QVBoxLayout()
        self.entity_list = QListWidget()
        entity_layout.addWidget(self.entity_list)
        self.entity_group.setLayout(entity_layout)
        left_panel.addWidget(self.entity_group)

        # Placeholder bottom left panel (could be logs, recent actions, diagram preview, etc.)
        self.bottom_left_group = QGroupBox()
        self.bottom_left_group.setMinimumHeight(200)
        self.bottom_left_group.setTitle("Details / Preview / Logs")
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

        self.export_button = QPushButton("EXPORT")
        self.validate_button = QPushButton("VALIDATE")
        self.train_button = QPushButton("TRAIN")
        self.run_button = QPushButton("RUN")
        self.run_batch_button = QPushButton("RUN BATCH")

        button_grid.addWidget(self.export_button, 0, 1)
        button_grid.addWidget(self.validate_button, 1, 1)
        button_grid.addWidget(self.train_button, 0, 0)
        button_grid.addWidget(self.run_button, 1, 0)
        button_grid.addWidget(self.run_batch_button, 2, 1)

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
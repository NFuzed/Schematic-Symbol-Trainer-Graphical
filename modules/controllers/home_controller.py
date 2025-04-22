from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QGroupBox,
    QScrollArea, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt

from src.core import EntityManager
from ..utilities import style_sheet_loader
from ..utilities.entity_row_widget import EntityRow
from ..utilities.log_panel import LogPanel
from core import Core
from ..utilities.model_config_panel import ModelConfigPanel


class HomeController:
    def __init__(self, core : Core, parent=None):
        self.core = core
        self.manager_to_widget_row : dict[EntityManager, EntityRow] = {}
        self.widget = QWidget(parent)
        self.setup_ui()
        self.register_subscribers()
        parent.addWidget(self.widget)

    def setup_ui(self):
        style_sheet_loader.load_style_sheet("home_page.qss", self.widget)

        main_layout = QHBoxLayout(self.widget)

        # Left side layout (Entity managers + optional bottom panel)
        left_panel = QVBoxLayout()

        # Entity Manager List Section
        self.entity_group = QGroupBox("ENTITIES")
        entity_group_layout = QVBoxLayout()

        # Scrollable container for entity rows
        self.entity_scroll_container = QWidget()
        self.entity_scroll_layout = QVBoxLayout(self.entity_scroll_container)
        self.entity_scroll_layout.setContentsMargins(5, 5, 5, 5)
        self.entity_scroll_layout.setSpacing(6)

        # Scroll area wrapping the container
        self.entity_scroll_area = QScrollArea()
        self.entity_scroll_area.setWidgetResizable(True)
        self.entity_scroll_area.setWidget(self.entity_scroll_container)

        entity_group_layout.addWidget(self.entity_scroll_area)
        self.entity_group.setLayout(entity_group_layout)
        left_panel.addWidget(self.entity_group)

        # Placeholder bottom left panel (could be logs, recent actions, diagram preview, etc.)
        self.log_panel = LogPanel()
        left_panel.addWidget(self.log_panel.widget)

        for i in range(100):
            self.log_panel.write("TEST")

        main_layout.addLayout(left_panel, 2)

        # Right side layout (Model Configuration)
        right_panel = QVBoxLayout()
        self.config_group = QGroupBox("MODEL CONFIGURATION")
        config_layout = QVBoxLayout()
        self.config_group.setLayout(config_layout)
        right_panel.addWidget(self.config_group, stretch=1)
        self.model_config_panel = ModelConfigPanel()
        config_layout.addWidget(self.model_config_panel.widget)

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

    def register_subscribers(self):
        self.core.database.created_entity_manager_observer.bind(self.create_entity_row)
        self.core.database.destroyed_entity_manager_observer.bind(self.delete_entity_row)

    def create_entity_row(self, entity_manager : EntityManager):
        row = EntityRow(entity_manager)
        self.entity_scroll_layout.addWidget(row.widget)
        self.manager_to_widget_row[entity_manager] = row

    def delete_entity_row(self, entity_manager : EntityManager):
        if entity_manager in self.manager_to_widget_row:
            entity_row = self.manager_to_widget_row[entity_manager]
            entity_row.widget.deleteLater()
            self.manager_to_widget_row.pop(entity_manager)

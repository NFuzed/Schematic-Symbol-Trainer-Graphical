import threading

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QGroupBox,
    QScrollArea, QGridLayout, QSizePolicy, QFileDialog
)
from PySide6.QtCore import Qt

from src.core.entity_manager import EntityManager
from src.model.multi_class_dataset import MultiClassSymbolDataset
from ..utilities import style_sheet_loader
from ..utilities.entity_row_widget import EntityRow
from ..utilities.log_panel import LogPanel
from core import Core
from ..utilities.model_config_panel import ModelConfigPanel


class HomeController:
    def __init__(self, core: Core, parent=None):
        self.core = core
        self.dataset = None
        self.manager_to_widget_row: dict[EntityManager, EntityRow] = {}
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
        self.generate_dataset_button = QPushButton("Generate Dataset")
        self.analysis_button = QPushButton("Analysis")
        self.train_button = QPushButton("Train")
        self.validate_button = QPushButton("Validate")
        self.run_button = QPushButton("Run")
        self.run_batch_button = QPushButton("Run Batch")
        self.export_button = QPushButton("Export")

        button_grid.addWidget(self.generate_dataset_button, 0, 0, 1, 2)
        button_grid.addWidget(self.import_button, 0, 2, 1, 2)
        button_grid.addWidget(self.export_button, 0, 4, 1, 2)
        button_grid.addWidget(self.train_button, 1, 0, 1, 3)
        button_grid.addWidget(self.validate_button, 1, 3, 1, 3)
        button_grid.addWidget(self.run_button, 2, 0, 1, 3)
        button_grid.addWidget(self.run_batch_button, 2, 3, 1, 3)
        button_grid.addWidget(self.analysis_button, 3, 0, 1, 6)

        right_panel.addLayout(button_grid)
        main_layout.addLayout(right_panel, 3)

        self.train_button.clicked.connect(self.train_model)
        self.export_button.clicked.connect(self.export_model)
        self.import_button.clicked.connect(self.import_model)
        self.generate_dataset_button.clicked.connect(self.generate_dataset)
        self.run_button.clicked.connect(self.run_model)
        self.run_batch_button.clicked.connect(self.run_model_batch)

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
        self.core.symbol_detector.update_logger_observer.bind(self.log_panel.write)

    def create_entity_row(self, entity_manager: EntityManager):
        row = EntityRow(entity_manager)
        self.entity_scroll_layout.addWidget(row.widget)
        self.manager_to_widget_row[entity_manager] = row

    def delete_entity_row(self, entity_manager: EntityManager):
        if entity_manager in self.manager_to_widget_row:
            entity_row = self.manager_to_widget_row[entity_manager]
            entity_row.widget.deleteLater()
            self.manager_to_widget_row.pop(entity_manager)

    # BUTTON CONNECTIONS

    def generate_dataset(self):
        config = self.model_config_panel.get_config()

        self.dataset = MultiClassSymbolDataset(
            entity_managers=self.core.database.get_entity_managers(),
            image_size=config["image_size"],
            samples_per_image=config["samples_per_class"],
            rotation=config["augment_rotation"],
            flip=config["augment_flip"],
            noise=config["augment_noise"],
        )

        self.log_panel.write(f"Dataset created with {len(self.dataset)} samples.")

    def train_model(self):
        if not self.dataset:
            self.log_panel.write("Dataset has not been generated, please create one before training.")
            return

        config = self.model_config_panel.get_config()

        num_classes = len(self.core.database.entity_managers) + 1
        num_epochs = config["epochs"]
        lr = config["learning_rate"]

        self.log_panel.write("Model Training Process Started")

        thread = threading.Thread(
            target=lambda: self.core.symbol_detector.train(self.dataset, num_classes, num_epochs, lr))
        thread.start()

    def export_model(self):
        path, _ = QFileDialog.getSaveFileName(self.widget, "Export Model", "", "Model Files (*.pth)")
        if path:
            self.core.symbol_detector.export_model(path)
            self.log_panel.write(f"Model exported to {path}")

    def import_model(self):
        path, _ = QFileDialog.getOpenFileName(self.widget, "Load Model", "", "Model Files (*.pth)")
        if path:
            num_classes = len(self.core.database.get_entity_managers()) + 1
            self.core.symbol_detector.load_model(num_classes=num_classes, path=path)
            self.log_panel.write(f"Model loaded from {path}")

    def run_model(self, file_path=None, folder=None):
        config = self.model_config_panel.get_config()

        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self.widget,
                "Open Diagram",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
            )

        if not folder:
            folder = QFileDialog.getExistingDirectory(self.widget, "Select Export Folder")
            if not folder:
                return

        if file_path:
            thread = threading.Thread(target= lambda: self.core.symbol_detector.detect(file_path, config["threshold"], export_folder=folder))
            thread.start()

    def run_model_batch(self):

        export_folder = QFileDialog.getExistingDirectory(self.widget, "Select Export Folder")
        if not export_folder:
            return

        folder_path = QFileDialog.getExistingDirectory(self.widget, "Select Folder")
        if folder_path:
            import os
            for f in os.listdir(folder_path):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    self.run_model(os.path.join(folder_path, f), export_folder)




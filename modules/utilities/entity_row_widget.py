from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from src.core.entity_manager import EntityManager

class EntityRow:
    def __init__(self, entity_manager: EntityManager):
        self.entity_manager = entity_manager
        self.widget = QWidget()
        self.layout = QHBoxLayout(self.widget)
        self.layout.setContentsMargins(8, 4, 8, 4)
        self.layout.setSpacing(10)

        self.name_label = QLabel(entity_manager.entity_manager_name)
        self.name_label.setStyleSheet("color: rgb(248, 248, 242); font-weight: bold;")

        self.count_label = QLabel(f"({len(entity_manager.entities)} images)")
        self.count_label.setStyleSheet("color: rgb(189, 147, 249);")

        self.layout.addWidget(self.name_label)
        self.layout.addStretch()
        self.layout.addWidget(self.count_label)

        self.register_subscribers()

    def register_subscribers(self):
        self.entity_manager.created_entity_observer.bind(lambda _: self.update_count())
        self.entity_manager.deleted_entity_observer.bind(lambda _: self.update_count())

    def update_count(self):
        self.count_label.setText(f"({len(self.entity_manager.entities)} images)")
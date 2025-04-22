from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                               QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal, QSize

from modules.utilities.entity_displayer import EntityDisplayer
from src.core.entity import Entity
from src.core.entity_manager import EntityManager

class EntityGallery:
    """Container widget that displays entities in a wrapping grid"""
    def __init__(self, entity_manager: EntityManager, parent=None):
        self.widget = QWidget(parent)
        self.entity_manager = entity_manager
        self.entity_display_map: Dict[Entity, EntityDisplayer] = {}

        self.setup_ui()
        self.max_columns = 4  # Items per row before wrapping
        self.item_size = QSize(220, 220)  # Matches EntityDisplayer
        self.register_for_events()

    def setup_ui(self):
        """Initialize the UI components"""
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area for the gallery
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container for grid layout
        self.gallery_container = QWidget()
        self.grid_layout = QGridLayout(self.gallery_container)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)
        self.grid_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.scroll_area.setWidget(self.gallery_container)
        self.main_layout.addWidget(self.scroll_area)

    def add_entity(self, entity: Entity):
        """Add a new entity to the grid"""
        displayer = EntityDisplayer(entity, self.entity_manager)
        self.entity_display_map[entity] = displayer


        # Calculate position in grid
        count = self.grid_layout.count()
        row = count // self.max_columns
        col = count % self.max_columns

        self.grid_layout.addWidget(displayer.widget, row, col)
        return displayer

    def remove_entity(self, entity: Entity):
        """Remove an entity from the grid"""
        # Find and remove the widget
        displayer = self.entity_display_map[entity]
        del self.entity_display_map[entity]
        for i in range(self.grid_layout.count()):
            if self.grid_layout.itemAt(i).widget() == displayer.widget:
                self.grid_layout.removeWidget(displayer.widget)
                displayer.widget.deleteLater()
                self.reorganize_grid()  # Reflow remaining items
                break

    def reorganize_grid(self):
        """Reorganize items after deletion to prevent empty spaces"""
        # Temporarily remove all widgets
        widgets = []
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                widgets.append(item.widget())

        # Re-add in proper grid order
        for i, widget in enumerate(widgets):
            row = i // self.max_columns
            col = i % self.max_columns
            self.grid_layout.addWidget(widget, row, col)

    def clear_entities(self):
        """Remove all entities from the gallery"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()


    def register_for_events(self):
        self.entity_manager.deleted_entity_observer.bind(self.remove_entity)
        self.entity_manager.created_entity_observer.bind(self.add_entity)
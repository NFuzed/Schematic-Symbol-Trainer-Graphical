from PySide6.QtWidgets import QWidget, QComboBox
from core import Core

class EntityDropDownSelector:
    def __init__(self, core: Core):
        self.core = core
        self.widget = QComboBox()
        self.widget.setObjectName("entityDropdown")
        self.widget.setFixedSize(200, 30)
        self.widget.setEnabled(False)

        self.register_for_events()

    def register_for_events(self):
        """Connect to entity manager changes"""
        self.core.database.created_entity_manager_observer.bind(self._add_entity_to_dropdown)
        self.core.database.destroyed_entity_manager_observer.bind(self._remove_entity_from_dropdown)

    def _add_entity_to_dropdown(self, entity_manager):
        """Add an entity to the dropdown"""
        self.widget.addItem(entity_manager.entity_manager_name, entity_manager)

    def _remove_entity_from_dropdown(self, entity_manager):
        """Remove an entity from the dropdown"""
        index = self._find_entity_index(entity_manager)
        if index >= 0:
            self.widget.removeItem(index)

    def _find_entity_index(self, entity_manager):
        """Find the combo box index for an entity manager"""
        for i in range(self.widget.count()):
            if self.widget.itemData(i) == entity_manager:
                return i
        return -1

    def get_current_entity(self):
        """Get the currently selected entity manager"""
        if self.widget.currentIndex() >= 0:
            return self.widget.itemData(self.widget.currentIndex())
        return None


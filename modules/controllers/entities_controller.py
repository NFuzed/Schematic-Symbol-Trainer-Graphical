from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStackedWidget, QTabWidget, QTextEdit,
    QVBoxLayout, QWidget, QMessageBox, QDialog, QFormLayout, QDialogButtonBox)
import os
from pathlib import Path
from core import Core
from src.core import EntityManager

DIALOG_QSS = "dialog.qss"


class EntityController:
    def __init__(self, core : Core, parent=None):
        self.widget = QWidget(parent)
        self.core : Core = core
        parent.addWidget(self.widget)

        self.entity_manager_to_widget: Dict(EntityManager, QWidget) = {}
        self.widget_to_entity_manager: Dict(QWidget, EntityManager) = {}

        self.tab_widget = QTabWidget()
        self.filter_button = QPushButton("Filter")
        self.new_entity_button = QPushButton("New Entity")
        self.search_input = QLineEdit()
        self.main_layout = QVBoxLayout(self.widget)

        self.setup_ui()
        self.setup_styles("entities_page.qss", self.widget)
        self.register_for_events()

    def setup_ui(self):
        """Initialize all UI components"""
        self.widget.setObjectName("entities")
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Search/Filter Section
        self.setup_search_section()

        # Tab Section
        self.setup_tab_section()

    def setup_search_section(self):
        """Create the search/filter section at the top"""
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_frame.setMinimumHeight(110)
        search_frame.setFrameShape(QFrame.Shape.NoFrame)

        # Title
        title_frame = QFrame()
        title_frame.setMaximumHeight(35)
        title_label = QLabel("ENTITIES")
        title_label.setObjectName("titleLabel")

        title_layout = QVBoxLayout(title_frame)
        title_layout.addWidget(title_label)

        # Search controls
        content_frame = QFrame()
        self.search_input.setPlaceholderText("Type here")
        self.search_input.setObjectName("searchInput")

        self.filter_button.setObjectName("filterButton")
        self.filter_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.filter_button.setIcon(QIcon(":/icons/images/icons/cil-equalizer.png"))
        self.filter_button.clicked.connect(self.filter_entities)

        self.new_entity_button.setObjectName("newEntityButton")
        self.new_entity_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.new_entity_button.setIcon(QIcon(":/icons/images/icons/cil-plus.png"))
        self.new_entity_button.clicked.connect(self.show_new_entity_dialog)

        filter_label = QLabel("Filter for Entities")
        filter_label.setObjectName("filterLabel")

        search_grid = QGridLayout()
        search_grid.addWidget(self.search_input, 0, 0)
        search_grid.addWidget(self.filter_button, 0, 1)
        search_grid.addWidget(self.new_entity_button, 0, 2)
        search_grid.addWidget(filter_label, 1, 0, 1, 2)

        content_layout = QHBoxLayout(content_frame)
        content_layout.addLayout(search_grid)

        # Combine sections
        search_layout = QVBoxLayout(search_frame)
        search_layout.addWidget(title_frame)
        search_layout.addWidget(content_frame)

        self.main_layout.addWidget(search_frame)

    def setup_tab_section(self):
        """Create the tab widget section with close confirmation"""
        tab_frame = QFrame()
        tab_frame.setObjectName("tabFrame")
        tab_frame.setMinimumHeight(150)

        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("entityTabWidget")
        self.tab_widget.setFont(QFont("Segoe UI", 10))
        self.tab_widget.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.confirm_tab_close)

        tab_layout = QVBoxLayout(tab_frame)
        tab_layout.addWidget(self.tab_widget)

        self.main_layout.addWidget(tab_frame)

    def confirm_tab_close(self, index):
        """Show confirmation dialog before closing tab"""
        widget = self.tab_widget.widget(index)
        if widget is None:
            return

        entity_manager = self.widget_to_entity_manager.get(widget)
        if entity_manager is None:
            return

        tab_name = self.tab_widget.tabText(index)

        dialog = QMessageBox(self.widget)
        dialog.setWindowTitle("Confirm Deletion")
        dialog.setIcon(QMessageBox.Question)
        dialog.setText(f"Delete entity '{tab_name}'?")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        self.setup_styles(DIALOG_QSS, dialog)

        if dialog.exec() == QMessageBox.Yes:
            self.core.database.delete_entity_manager(entity_manager)

    def show_new_entity_dialog(self):
        """Show dialog for creating new entity"""

        dialog = QDialog(self.widget)
        dialog.setWindowTitle("New Entity")
        dialog.setMinimumWidth(300)
        self.setup_styles(DIALOG_QSS, dialog)


        layout = QFormLayout(dialog)

        # Entity name input
        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter entity name")
        layout.addRow("Name:", name_input)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(lambda: self.add_tab(dialog, name_input.text()))
        buttons.rejected.connect(dialog.reject)
        self.setup_styles(DIALOG_QSS, buttons)
        layout.addRow(buttons)

        dialog.exec()

    def setup_styles(self, file_name, widget):
        """Apply consistent styling to all components"""
        # Using pathlib for more reliable path handling
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent  # Go up two levels from controllers
        styles_dir = project_root / "styles"
        qss_file = styles_dir / file_name

        if qss_file.exists():
            with open(qss_file, "r", encoding="utf-8") as f:
                style = f.read()
                widget.setStyleSheet(style)
        else:
            print(f"Stylesheet not found: {qss_file}")

    def add_tab(self, widget, entity_name):
        """Add a new tab to the tab widget

        Args:
            widget (QWidget): The widget to add as a tab
            entity_name (str): The title for the tab
        """
        widget.accept()
        self.core.database.create_entity_manager(entity_name)

    def remove_tab(self, entity_manager: EntityManager):
        """Remove tab and perform any cleanup"""
        widget = self.entity_manager_to_widget.get(entity_manager)
        if widget is not None:
            index = self.tab_widget.indexOf(widget)
            if index >= 0:
                self.tab_widget.removeTab(index)

            del self.entity_manager_to_widget[entity_manager]
            if widget in self.widget_to_entity_manager:
                del self.widget_to_entity_manager[widget]

    def register_for_events(self):
        self.core.database.created_entity_manager_observer.bind(lambda entity_manager: self.create_tab(entity_manager))
        self.core.database.destroyed_entity_manager_observer.bind(lambda entity_manager: self.remove_tab(entity_manager))

    def create_tab(self, entity_manager: EntityManager):
        """Create a new tab for the entity manager"""
        tab_widget = QWidget()
        self.entity_manager_to_widget[entity_manager] = tab_widget
        self.widget_to_entity_manager[tab_widget] = entity_manager
        self.tab_widget.addTab(tab_widget, entity_manager.entity_manager_name)

    def clear_tabs(self):
        """Remove all tabs"""
        while self.tab_widget.count() > 0:
            self.tab_widget.removeTab(0)

    def filter_entities(self):
        query = self.search_input.text()

        tab_count = self.tab_widget.count()

        for i in range(tab_count):
            if query in self.tab_widget.tabText(i):
                self.tab_widget.setTabVisible(i, True)
            else:
                self.tab_widget.setTabVisible(i, False)

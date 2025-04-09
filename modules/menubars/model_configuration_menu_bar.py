from PySide6.QtWidgets import (QFrame, QVBoxLayout, QGridLayout, QLabel,
                               QPushButton, QTextEdit)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QCursor


class ModelConfigurationMenuBar:
    def __init__(self, parent, size_policy, font, app_layout):
        self.widget = self._create_main_widget(parent)
        self._setup_layouts()
        self._create_top_bar()
        self._create_content_area(size_policy, font)
        app_layout.addWidget(self.widget)

    def _create_main_widget(self, parent):
        """Create and configure the main widget"""
        widget = QFrame(parent)
        widget.setObjectName("extraLeftBox")
        widget.setMinimumSize(0, 0)
        widget.setMaximumSize(0, 16777215)
        widget.setFrameShape(QFrame.NoFrame)
        widget.setFrameShadow(QFrame.Raised)
        return widget

    def _setup_layouts(self):
        """Set up the main layout structure"""
        self.main_layout = QVBoxLayout(self.widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def _create_top_bar(self):
        """Create the top bar with icon, label and close button"""
        # Top background frame
        top_bg = QFrame(self.widget)
        top_bg.setObjectName("extraTopBg")
        top_bg.setFixedHeight(50)
        top_bg.setFrameShape(QFrame.NoFrame)

        # Top bar layout
        top_layout = QVBoxLayout(top_bg)
        top_layout.setContentsMargins(0, 0, 0, 0)

        # Grid layout for top bar contents
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setContentsMargins(10, 0, 10, 0)

        # Icon
        icon = QFrame(top_bg)
        icon.setObjectName("extraIcon")
        icon.setFixedSize(20, 20)
        icon.setFrameShape(QFrame.NoFrame)
        grid_layout.addWidget(icon, 0, 0)

        # Label
        self.label = QLabel(top_bg)
        self.label.setObjectName("extraLabel")
        self.label.setMinimumWidth(150)
        grid_layout.addWidget(self.label, 0, 1)

        # Close button
        self.close_btn = QPushButton(top_bg)
        self.close_btn.setObjectName("extraCloseColumnBtn")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.close_btn.setIcon(QIcon(":/icons/images/icons/icon_close.png"))
        self.close_btn.setIconSize(QSize(20, 20))
        grid_layout.addWidget(self.close_btn, 0, 2)

        top_layout.addLayout(grid_layout)
        self.main_layout.addWidget(top_bg)

    def _create_content_area(self, size_policy, font):
        """Create the main content area with buttons and text"""
        content_frame = QFrame(self.widget)
        content_frame.setObjectName("extraContent")
        content_frame.setFrameShape(QFrame.NoFrame)

        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Menu buttons
        self._create_menu_buttons(content_frame, size_policy, font, content_layout)

        # Text area
        self._create_text_area(content_frame, content_layout)

        # Bottom area (empty for now)
        bottom_frame = QFrame(content_frame)
        bottom_frame.setObjectName("extraBottom")
        bottom_frame.setFrameShape(QFrame.NoFrame)
        content_layout.addWidget(bottom_frame)

        self.main_layout.addWidget(content_frame)

    def _create_menu_buttons(self, parent, size_policy, font, layout):
        """Create the menu buttons section"""
        menu_frame = QFrame(parent)
        menu_frame.setObjectName("extraTopMenu")
        menu_frame.setFrameShape(QFrame.NoFrame)

        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)

        # Button factory
        buttons = [
            ("Share", "btn_share", "cil-share-boxed.png"),
            ("Adjustments", "btn_adjustments", "cil-equalizer.png"),
            ("More", "btn_more", "cil-layers.png")
        ]

        for text, obj_name, icon in buttons:
            btn = QPushButton(menu_frame)
            btn.setObjectName(obj_name)
            btn.setSizePolicy(size_policy)
            btn.setMinimumHeight(45)
            btn.setFont(font)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setStyleSheet(f"background-image: url(:/icons/images/icons/{icon});")
            btn.setText(text)
            menu_layout.addWidget(btn)

        layout.addWidget(menu_frame, alignment=Qt.AlignTop)

    def _create_text_area(self, parent, layout):
        """Create the text edit area"""
        text_frame = QFrame(parent)
        text_frame.setObjectName("extraCenter")
        text_frame.setFrameShape(QFrame.NoFrame)

        text_layout = QVBoxLayout(text_frame)

        self.text_edit = QTextEdit(text_frame)
        self.text_edit.setObjectName("textEdit")
        self.text_edit.setMinimumWidth(222)
        self.text_edit.setStyleSheet("background: transparent;")
        self.text_edit.setFrameShape(QFrame.NoFrame)
        self.text_edit.setReadOnly(True)

        text_layout.addWidget(self.text_edit)
        layout.addWidget(text_frame)
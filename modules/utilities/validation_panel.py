from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QGridLayout, QSizePolicy
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
import numpy as np

class ValidationPanel:
    def __init__(self, core, detections, path):
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.label_to_name = {
            i + 1: mgr.entity_manager_name
            for i, mgr in enumerate(core.database.entity_managers)
        }

        for det in detections:
            det["image"] = self.extract_crop(path, det["box"])

        # Scrollable grid of validation items
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        self.grid_layout = QGridLayout(container)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(15)

        scroll_area.setWidget(container)
        self.layout.addWidget(scroll_area)

        # Bottom button panel
        button_panel = QHBoxLayout()
        self.apply_button = QPushButton("Apply Feedback")
        self.clear_button = QPushButton("Clear")
        button_panel.addStretch()
        button_panel.addWidget(self.apply_button)
        button_panel.addWidget(self.clear_button)
        self.layout.addLayout(button_panel)

        # Display detections
        self.detections = detections  # [{image: np.ndarray, label: int, score: float}]
        self.feedback = {}  # index: True/False
        self.populate_grid()

    def populate_grid(self):
        for index, det in enumerate(self.detections):
            cell = self.create_validation_cell(index, det)
            row = index // 4
            col = index % 4
            self.grid_layout.addWidget(cell, row, col)

    def create_validation_cell(self, index, det):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Image preview
        image = QImage(det["image"].data, det["image"].shape[1], det["image"].shape[0], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(image).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Label and score
        label = QLabel(f"Label: {self.label_to_name[det['label']]}\nScore: {det['score']:.2f}")
        label.setAlignment(Qt.AlignCenter)

        # Approve / Reject
        button_row = QHBoxLayout()
        accept = QPushButton("ACC")
        reject = QPushButton("REJ")
        accept.setFixedWidth(40)
        reject.setFixedWidth(40)

        def mark_feedback(value):
            self.feedback[index] = value
            accept.setStyleSheet("background-color: #50fa7b;" if value else "")
            reject.setStyleSheet("background-color: #ff5555;" if not value else "")

        accept.clicked.connect(lambda: mark_feedback(True))
        reject.clicked.connect(lambda: mark_feedback(False))

        button_row.addWidget(accept)
        button_row.addWidget(reject)
        button_row.setAlignment(Qt.AlignCenter)

        layout.addWidget(image_label)
        layout.addWidget(label)
        layout.addLayout(button_row)
        return widget

    def get_feedback(self):
        accepted = [self.detections[i] for i, approved in self.feedback.items() if approved]
        rejected = [self.detections[i] for i, approved in self.feedback.items() if not approved]
        return {"accepted": accepted, "rejected": rejected}

    def extract_crop(self, image_path, box):
        import cv2
        x1, y1, x2, y2 = map(int, box)
        img = cv2.imread(image_path)
        crop = img[y1:y2, x1:x2]
        return cv2.cvtColor(crop, cv2.COLOR_BGR2RGBA)
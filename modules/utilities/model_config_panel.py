from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFormLayout, QSpinBox, QCheckBox,
    QComboBox, QDoubleSpinBox, QPushButton
)

class ModelConfigPanel:
    def __init__(self, parent=None):
        self.widget = QWidget(parent)
        self.layout = QVBoxLayout(self.widget)

        self.form = QFormLayout()
        self.widget.setLayout(self.layout)
        self.layout.addLayout(self.form)

        # Dataset options
        self.data_mode = QComboBox()
        self.data_mode.addItems(["Synthetic", "Real", "Hybrid"])

        self.samples_per_class = QSpinBox()
        self.samples_per_class.setMinimum(1)
        self.samples_per_class.setValue(6)

        self.image_size = QSpinBox()
        self.image_size.setRange(128, 2048)
        self.image_size.setValue(640)

        self.augment_rotation = QCheckBox("Enable Rotation")
        self.augment_flip = QCheckBox("Enable Flip")
        self.augment_noise = QCheckBox("Enable Noise")

        # Training options
        self.epochs = QSpinBox()
        self.epochs.setRange(1, 100)
        self.epochs.setValue(30)

        self.learning_rate = QDoubleSpinBox()
        self.learning_rate.setDecimals(4)
        self.learning_rate.setSingleStep(0.0001)
        self.learning_rate.setValue(0.001)

        self.batch_size = QSpinBox()
        self.batch_size.setRange(1, 64)
        self.batch_size.setValue(4)

        self.model_type = QComboBox()
        self.model_type.addItems(["Faster R-CNN", "RetinaNet"])

        # Add fields to form
        self.form.addRow("Data Mode:", self.data_mode)
        self.form.addRow("Samples/Class:", self.samples_per_class)
        self.form.addRow("Image Size:", self.image_size)
        self.form.addRow("", self.augment_rotation)
        self.form.addRow("", self.augment_flip)
        self.form.addRow("", self.augment_noise)
        self.form.addRow("Epochs:", self.epochs)
        self.form.addRow("Learning Rate:", self.learning_rate)
        self.form.addRow("Batch Size:", self.batch_size)
        self.form.addRow("Model Type:", self.model_type)

        # Action button
        self.train_button = QPushButton("Start Training")
        self.layout.addWidget(self.train_button)

    def get_config(self):
        """Return config as a dictionary"""
        return {
            "data_mode": self.data_mode.currentText(),
            "samples_per_class": self.samples_per_class.value(),
            "image_size": self.image_size.value(),
            "augment_rotation": self.augment_rotation.isChecked(),
            "augment_flip": self.augment_flip.isChecked(),
            "augment_noise": self.augment_noise.isChecked(),
            "epochs": self.epochs.value(),
            "learning_rate": self.learning_rate.value(),
            "batch_size": self.batch_size.value(),
            "model_type": self.model_type.currentText(),
        }
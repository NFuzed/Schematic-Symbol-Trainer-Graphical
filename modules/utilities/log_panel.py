from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QTextEdit

class LogPanel:
    def __init__(self, parent=None):
        self.widget = QGroupBox("Logs", parent)
        self.widget.setMinimumHeight(200)

        self.layout = QVBoxLayout(self.widget)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.layout.addWidget(self.log_area)

    def write(self, message: str):
        self.log_area.append(message)
from PySide6.QtCore import Slot


class HomeController:
    def __init__(self, ui_home_page):
        self.ui = ui_home_page  # HomePage UI instance injected from MainController

        # Connect UI signals to controller slots
        if hasattr(self.ui, "example_button"):
            self.ui.example_button.clicked.connect(self.handle_example_action)

    @Slot()
    def handle_example_action(self):
        """Handle the HomePage's example button click."""
        # Implement the logic that should happen when the button is clicked
        print("Home button was clicked - performing action...")
        # e.g., update UI elements or call business logic functions
        # self.ui.status_label.setText("Action performed!")
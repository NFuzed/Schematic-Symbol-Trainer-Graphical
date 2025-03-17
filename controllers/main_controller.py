from ui.main_window import MainWindow
from controllers.home_controller import HomeController
from controllers.entities_controller import EntitiesController
from controllers.settings_controller import SettingsController


class MainController:
    def __init__(self):
        # Initialize the main window UI
        self.main_window = MainWindow()

        # Create controllers for each page, passing the UI instances
        self.home_controller = HomeController(self.main_window.home_page)
        self.entities_controller = EntitiesController(self.main_window.entities_page)
        self.settings_controller = SettingsController(self.main_window.settings_page)

        # Connect main window navigation to controller methods (if main_window has nav buttons or menu)
        # For example, if MainWindow had a toolbar or menu for navigation:
        # self.main_window.home_action.triggered.connect(self.show_home_page)
        # self.main_window.entities_action.triggered.connect(self.show_entities_page)
        # self.main_window.settings_action.triggered.connect(self.show_settings_page)

    def show_home_page(self):
        """Switch to Home page in the main window."""
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.home_page)

    def show_entities_page(self):
        """Switch to Entities page."""
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.entities_page)

    def show_settings_page(self):
        """Switch to Settings page."""
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.settings_page)

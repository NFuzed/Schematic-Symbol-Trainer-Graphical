# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import threading

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *

os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

from core import Core
import cv2
import threading
from src.utilities import database_exporter, database_importer

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////

class MainWindow(QMainWindow):
    def __init__(self, core :Core):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.core = core
        self.ui.setupUi(self, self.core)
        self.widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "Schematic Symbol Trainer"
        description = "Schematic Symbol Trainer"
        # APPLY TEXTS
        self.setWindowTitle(title)
        self.widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        self.widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        # self.widgets.tabWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.widgets.lineEdit.text()

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        self.widgets.page_menu_bar.btn_home.clicked.connect(self.buttonClick)
        self.widgets.page_menu_bar.btn_view.clicked.connect(self.buttonClick)
        self.widgets.page_menu_bar.btn_entities.clicked.connect(self.buttonClick)
        self.widgets.page_menu_bar.btn_new.clicked.connect(self.buttonClick)
        self.widgets.page_menu_bar.btn_save.clicked.connect(self.buttonClick)
        self.widgets.page_menu_bar.btn_load.clicked.connect(self.buttonClick)
        # self.widgets.pushButton.clicked.connect(self.buttonClick)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        self.widgets.stackedWidget.setCurrentWidget(self.widgets.home.widget)
        self.widgets.page_menu_bar.btn_home.setStyleSheet(UIFunctions.selectMenu(self.widgets.page_menu_bar.btn_home.styleSheet()))


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btn_name = btn.objectName()

        # SHOW HOME PAGE
        if btn_name == "btn_home":
            self.widgets.stackedWidget.setCurrentWidget(self.widgets.home.widget)
            UIFunctions.resetStyle(self, btn_name)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btn_name == "btn_entities":
            self.widgets.stackedWidget.setCurrentWidget(self.widgets.entities.widget)
            UIFunctions.resetStyle(self, btn_name)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW DIAGRAM PAGE
        if btn_name == "btn_view":
            self.widgets.stackedWidget.setCurrentWidget(self.widgets.diagram.widget)
            UIFunctions.resetStyle(self, btn_name)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btn_name == "btn_new":
            self.core.database.clear_database()

        if btn_name == "btn_save":
            file_path, _ = QFileDialog.getSaveFileName(self.ui.stackedWidget, "Save Database", "", "Model (*.pkl)")
            if not file_path:
                return
            database_exporter.export_database(self.core.database, file_path)

        if btn_name == "btn_load":
            file_path, _ = QFileDialog.getOpenFileName(self.ui.stackedWidget, "Load Database","","Model (*.pkl)")
            if not file_path:
                return
            database_importer.import_database(self.core.database, file_path)

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    core = Core()
    window = MainWindow(core)
    sys.exit(app.exec())

import sqlite3

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem

from classes.insert_dialog_window import InsertDialogWindow
from classes.search_student_window import SearchStudentWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Menu Items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        search_student_action = QAction("Search", self)
        search_student_action.triggered.connect(self.search_student)
        edit_menu_item.addAction(search_student_action)

        # For Mac Users
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        # Create the table
        self.table = QTableWidget()

        # Define the columns
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        # Connecting the database
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        # Iterating over the rows and columns
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialogWindow(self)
        dialog.exec()

    def search_student(self):
        search_dialog = SearchStudentWindow(self)
        search_dialog.exec()

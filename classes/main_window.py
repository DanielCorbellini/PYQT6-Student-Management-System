import sqlite3
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QToolBar, QStatusBar, QPushButton
from classes.about_dialog_window import AboutDialog
from classes.delete_dialog import DeleteDialog
from classes.edit_dialog import EditDialog
from classes.insert_dialog_window import InsertDialogWindow
from classes.search_student_window import SearchStudentWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Menu Items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add student Action
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.__insert)
        file_menu_item.addAction(add_student_action)

        # Search student Action
        search_student_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_student_action.triggered.connect(self.__search_student)
        edit_menu_item.addAction(search_student_action)

        # About Action
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        # For Mac Users
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.__about)

        # Create the table
        self.table = QTableWidget()

        # Define the columns
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # Create statusbar and add status bar elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.__cell_clicked)

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

    def __cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.__edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.__delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def __insert(self):
        dialog = InsertDialogWindow(self)
        dialog.exec()

    def __search_student(self):
        search_dialog = SearchStudentWindow(self)
        search_dialog.exec()

    def __edit(self):
        dialog = EditDialog(self)
        dialog.exec()

    def __delete(self):
        dialog = DeleteDialog(self)
        dialog.exec()

    def __about(self):
        dialog = AboutDialog()
        dialog.exec()

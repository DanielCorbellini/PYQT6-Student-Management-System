from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox
from PyQt6.QtGui import QAction
import sys
import sqlite3


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
        dialog = InsertDialogWindow()
        dialog.exec()

    def search_student(self):
        search_dialog = SearchStudentWindow()
        search_dialog.exec()


class InsertDialogWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Making the layout
        layout = QVBoxLayout()

        # Add student name Widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        # Add combo box of courses
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)

        # Add mobile Widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")

        # Add a submit button
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)

        # Showing the Widgets
        layout.addWidget(self.student_name)
        layout.addWidget(self.course_name)
        layout.addWidget(self.mobile)
        layout.addWidget(button)
        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchStudentWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Set the window title and size
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Create layout
        search_layout = QVBoxLayout()

        # Create input widget and button
        self.search_student_name = QLineEdit()
        self.search_student_name.setPlaceholderText("Name")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)

        # Load the widgets and set the layout
        search_layout.addWidget(self.search_student_name)
        search_layout.addWidget(search_button)
        self.setLayout(search_layout)

    def search(self):
        name = self.search_student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()



app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

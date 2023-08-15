import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog


class SearchStudentWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = self.main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        for item in items:
            self.main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()

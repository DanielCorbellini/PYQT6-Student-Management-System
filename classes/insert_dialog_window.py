import sqlite3

from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog, QComboBox


class InsertDialogWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
        self.main_window.load_data()

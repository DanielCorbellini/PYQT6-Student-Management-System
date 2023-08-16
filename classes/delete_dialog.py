import sqlite3

from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QMessageBox


class DeleteDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Delete Student Data")

        # Making the GUI
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        self.setLayout(layout)

        yes_button.clicked.connect(self.__delete_student)
        no_button.clicked.connect(self.close)

    def __delete_student(self):
        # Get index and student id
        index = self.main_window.table.currentRow()
        student_id = self.main_window.table.item(index, 0).text()

        # Delete the selected row
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        self.main_window.load_data()

        self.close()

        # Create the confirmation message box
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully!")

        confirmation_widget.exec()

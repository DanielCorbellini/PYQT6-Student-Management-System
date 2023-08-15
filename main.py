import sys

from PyQt6.QtWidgets import QApplication

from classes.main_window import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())

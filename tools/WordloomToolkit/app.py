from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(900, 520)
    w.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
import sys

from PySide6.QtWidgets import QApplication

from modules.overlay import MainOverlay
from modules.ui import MainWindow


def main():
    app = QApplication([])
    overlay = MainOverlay()
    window = MainWindow()
    
    overlay.show()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
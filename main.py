import os
import sys

from PySide6.QtWidgets import QApplication

from modules.overlay import MainOverlay
from modules.ui import MainWindow


def main():
    app = QApplication([])
    
    path = os.path.join(os.path.dirname(__file__), 'resources/style.qss')
    with open(path, 'r') as file:
        style = file.read()
        app.setStyleSheet(style)
    
    overlay = MainOverlay()
    window = MainWindow()
    
    overlay.show()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
import os
import sys

from PySide6.QtWidgets import QApplication

from modules.overlay import MainOverlay
from modules.ui import MainWindow


def main():
    app = QApplication(sys.argv)
    
    path = os.path.join(os.path.dirname(__file__), 'resources/style.qss')
    with open(path, 'r') as file:
        style = file.read()
        app.setStyleSheet(style)
    
    overlay = MainOverlay()
    window = MainWindow()
    
    overlay.destroyed.connect(lambda *e: print(1))
    window.destroyed.connect(lambda *e: print(2))
    
    overlay.show()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
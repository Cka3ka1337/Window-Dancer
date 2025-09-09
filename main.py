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
    
    overlay.set_movie('resources/example.gif')
    overlay.set_scale(0.5)
    
    overlay.show()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
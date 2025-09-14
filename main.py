import os
import sys
import ctypes

import win32api

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QMouseEvent, QPainter, QPen, QColor, QPaintEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget

from modules.ui import MainWindow
from scripts.shared import SharedData
from modules.overlay import MainOverlay
from scripts.config_system import ConfigSystem

    
def update_style(app) -> None:
    path = os.path.join(os.path.dirname(__file__), 'resources/style.qss')
    with open(path, 'r') as file:
        style = file.read()
        app.setStyleSheet(style)


def main() -> None:
    config = ConfigSystem()
    print(config.config)
    
    app = QApplication(sys.argv)
    
    update_style(app)
    update_style_timer = QTimer()
    update_style_timer.timeout.connect(lambda: update_style(app))
    update_style_timer.start(100)
    
    overlay = MainOverlay()
    window = MainWindow()

    overlay.show()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
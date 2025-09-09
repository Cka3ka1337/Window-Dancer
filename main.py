import os
import sys

from PySide6.QtWidgets import (
    QApplication
)
from PySide6.QtCore import (
    QTimer,
)

from modules.overlay import MainOverlay
from modules.ui import MainWindow
        
    
def update_style(app) -> None:
    path = os.path.join(os.path.dirname(__file__), 'resources/style.qss')
    with open(path, 'r') as file:
        style = file.read()
        app.setStyleSheet(style)


def main():
    app = QApplication(sys.argv)
    
    update_style(app)
    update_style_timer = QTimer()
    update_style_timer.timeout.connect(lambda: update_style(app))
    update_style_timer.start(100)
    
    overlay = MainOverlay()
    window = MainWindow()
    
    overlay.set_movie('resources/example.gif')
    overlay.set_scale(0.5)
    
    # overlay.show()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
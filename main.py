import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from modules.ui import MainWindow
from modules.overlay import MainOverlay
from scripts.config_system import ConfigSystem
        
    
def update_style(app) -> None:
    path = os.path.join(os.path.dirname(__file__), 'resources/style.qss')
    with open(path, 'r') as file:
        style = file.read()
        app.setStyleSheet(style)


# def load_startup_animation(overlay: MainOverlay, path: str) -> None:
#     if not os.path.exists(path):
#         return
    
#     overlay.set_movie(path)


def main() -> None:
    config = ConfigSystem()
    config._init()
    
    app = QApplication(sys.argv)
    
    update_style(app)
    update_style_timer = QTimer()
    update_style_timer.timeout.connect(lambda: update_style(app))
    update_style_timer.start(100)
    
    overlay = MainOverlay()
    window = MainWindow()
    
    # startup_path = config.get('startup.path')
    # if startup_path: load_startup_animation(overlay, startup_path)
    
    overlay.show()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
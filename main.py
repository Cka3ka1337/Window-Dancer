import os
import sys
import json

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from modules.ui import MainWindow
from modules.overlay import MainOverlay
from scripts.constants import LocalPath
from scripts.config_system import ConfigSystem

    
def update_style(app) -> None:
    local_path = LocalPath()
    
    path = os.path.join(local_path.path, 'resources/style.qss')
    
    with open(path, 'r') as file:
        style = file.read()
        app.setStyleSheet(style)


def main() -> None:
    config = ConfigSystem()
    print(json.dumps(config.config, indent=4))
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
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
    LocalPath().path = os.path.dirname(__file__)
    main()
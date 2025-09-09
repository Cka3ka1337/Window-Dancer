from PySide6.QtWidgets import (
    QMainWindow
)
from PySide6.QtCore import (
    Qt
)


class MainOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainOverlay')
        
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
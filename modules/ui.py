from PySide6.QtWidgets import (
    QMainWindow
)
from PySide6.QtCore import (
    Qt
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainWindow')
        
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
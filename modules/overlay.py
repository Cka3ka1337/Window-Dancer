from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QLabel, QWidget
)
from PySide6.QtCore import (
    Qt
)


class MainOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainOverlay')
        self.setGeometry(100, 100, 100, 100)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)# | Qt.Tool)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        
        layout.addWidget(QLabel('This is MainOverlay'))
        
        
        layout.setContentsMargins(0, 0, 0, 0)
        
        
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
    
    
    def closeEvent(self, event):
        QApplication.instance().quit()
        super().closeEvent(event)
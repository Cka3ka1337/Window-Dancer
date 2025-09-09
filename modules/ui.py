from PySide6.QtWidgets import (
    QApplication, QMainWindow
)
from PySide6.QtCore import (
    Qt
)
from PySide6.QtGui import (
    QMouseEvent
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainWindow')
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        self._is_dragging = False
        self._drag_position = None
    
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._drag_position = event.globalPosition() - self.frameGeometry().topLeft()
        

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_dragging:
            move = event.globalPosition().toPoint() - self._drag_position.toPoint()
            self.move(move)
            

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False


    def closeEvent(self, event):
        QApplication.instance().quit()
        super().closeEvent(event)
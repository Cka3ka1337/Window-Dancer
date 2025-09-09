from PySide6.QtWidgets import (
    QApplication, QMainWindow
)
from PySide6.QtCore import (
    Qt, QTimer
)
from PySide6.QtGui import (
    QMouseEvent, QKeyEvent, QPainter,
    QBrush, QColor, QPen
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MainWindow')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0)
        
        self._is_dragging = False
        self._drag_position = None
        self._opacity = self.windowOpacity()
        
        self.opening_timer = QTimer()
        self.opening_timer.timeout.connect(self.__opening_timer)
        self.opening_timer.start(10)
        
    
    def __opening_timer(self) -> None:
        target_opacity = 0.9
        step_scale = 0.1
        
        self._opacity += (target_opacity - self._opacity) * step_scale
        
        if self._opacity + 0.01 >= target_opacity:
            self.opening_timer.stop()
            return

        self.setWindowOpacity(
            self._opacity
        )
      
    
    def paintEvent(self, event) -> None:
        palette = self.palette()
        color = palette.color(self.backgroundRole())
        
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rounded_rect = self.rect().adjusted(0, 0, 0, 0)
        painter.setBrush(QBrush(QColor(color.name())))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRoundedRect(rounded_rect, 10, 10)


    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Pause:
            self.close()
            
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._is_dragging = True
            self._drag_position = event.globalPosition() - self.frameGeometry().topLeft()
        

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_dragging:
            move = event.globalPosition().toPoint() - self._drag_position.toPoint()
            self.move(move)
            

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._is_dragging = False


    def closeEvent(self, event) -> None:
        QApplication.instance().quit()
        super().closeEvent(event)
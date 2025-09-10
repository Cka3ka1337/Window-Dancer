import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout
)
from PySide6.QtCore import (
    Qt, QTimer, QPointF
)
from PySide6.QtGui import (
    QMouseEvent, QKeyEvent, QPainter,
    QBrush, QColor, QPen, QLinearGradient,
    QPaintEvent
)
from .components.titlebar import TitleBar
from .components.main_group import MainGroup


class MainWindow(QMainWindow):
    set_movie = None
    set_scale = None
    _is_dragging = False
    _drag_position = None
    _opacity = 0
    
    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_widgets()
        self._init_timers()
        
    
    def _init_timers(self) -> None:
        self.opening_timer = QTimer()
        self.opening_timer.timeout.connect(self.__opening_timer)
        self.opening_timer.start(5)
    
    
    def _init_widgets(self) -> None:
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        title_bar = TitleBar('Window Dancer')
        title_bar.closed = self.close
        title_bar.minimized = self.showMinimized
        title_bar.init_ui()
        
        main_group = MainGroup()
        
        self.setCentralWidget(central_widget)
        layout.addWidget(title_bar)
        # layout.addStretch()
        layout.addWidget(main_group)
    
    
    def _init_window(self) -> None:
        self.setWindowTitle('MainWindow')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0)
        self.setFixedSize(200, 250)
    
    
    def __opening_timer(self) -> None:
        target_opacity = 1
        step_scale = 0.1
        
        self._opacity += (target_opacity - self._opacity) * step_scale
        
        if self._opacity + 0.01 >= target_opacity:
            self.opening_timer.stop()
            return

        self.setWindowOpacity(
            self._opacity
        )
      
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(QPointF(0, 0), QPointF(self.width(), self.height()))
        gradient.setColorAt(0.0, QColor(20, 10, 40, 240))
        gradient.setColorAt(1.0, QColor(15, 30, 70, 200))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.SolidLine)
        painter.drawRoundedRect(self.rect(), 7, 7)


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
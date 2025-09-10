import win32api
import win32gui
import win32con

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QLabel, QWidget
)
from PySide6.QtCore import (
    Qt, QSize, QTimer
)
from PySide6.QtGui import (
    QMovie, QPainter, QPaintEvent, QCloseEvent
)

from scripts.targets import get_target_window


class MainOverlay(QMainWindow):
    prev_rect = (0, 0, 0, 0)
    
    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_ui()
        self._init_timers()
    
    
    def _init_timers(self) -> None:
        self.update_window_pos_timer = QTimer()
        self.update_window_pos_timer.timeout.connect(self._update_window_pos)
        self.update_window_pos_timer.start(1)
    
    
    def _init_window(self) -> None:
        self.setWindowTitle('MainOverlay')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    
    def _init_ui(self) -> None:
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.movie = QMovie()
        self.movie.frameChanged.connect(self.update)
        self.label = QLabel() # Container for movie :/
        
        layout.addWidget(self.label)

        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
    
    
    def _update_window_pos(self) -> None:
        rect, type, wname, hwnd = get_target_window()
        x, y, w, h = rect
        overlay = self.size()
        
        if type == 'window' or type == 'cursor':
        
            if rect != self.prev_rect:
            
                self.move(
                    int(x + w / 2 - overlay.width() / 2),
                    int(y - overlay.height())
                )
                
                self.prev_rect = rect
        
        elif type == 'desktop':
            
            if rect != self.prev_rect:
                
                self.move(
                    int(x + w / 2 - overlay.width() / 2),
                    int(y + h - overlay.height())
                )
                
                self.prev_rect = rect
        
        # print(rect, type)
        
    
    
    def set_movie(self, path: str) -> None:
        self.movie.stop()
        self.movie.setFileName(path)
        self.movie.start()
        self.set_scale(1)
    
    
    def set_scale(self, scale: float) -> None:
        frame_rect = self.movie.frameRect()
        
        size = QSize(
            int(frame_rect.width() * scale), 
            int(frame_rect.height() * scale)
        )
        
        self.movie.setScaledSize(size)
        self.setFixedSize(size)
    
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        if self.movie.isValid():
            painter.drawPixmap(0, 0, self.movie.currentPixmap())
    
    
    def closeEvent(self, event: QCloseEvent) -> None:
        QApplication.instance().quit()
        super().closeEvent(event)
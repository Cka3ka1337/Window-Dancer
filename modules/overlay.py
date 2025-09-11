import ctypes

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QLabel, QWidget
)
from PySide6.QtCore import (
    Qt, QSize, QTimer, Slot
)
from PySide6.QtGui import (
    QMovie, QPainter, QPaintEvent, QCloseEvent
)

from scripts import calculate
from scripts.shared import SharedData
from scripts.targets import get_target_window
from scripts.config_system import ConfigSystem


class MainOverlay(QMainWindow):
    prev_rect = (0, 0, 0, 0)
    path = ''
    scale = 1
    gif_size = None
    prev_valid_pos = (0, 0)
    config = ConfigSystem()
    shared = SharedData()
    
    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_ui()
        self._init_timers()
        self._init_hooks()
    
    
    def _init_hooks(self) -> None:
        self.shared.set('movie.get', self.get_movie)
        self.shared.set('movie.set', self.set_movie)
        self.shared.set('scale.get', self.get_scale)
        self.shared.set('scale.set', self.set_scale)
    
    
    def _init_timers(self) -> None:
        self.update_window_pos_timer = QTimer()
        self.update_window_pos_timer.timeout.connect(self._update_window_pos)
        self.update_window_pos_timer.start(self.config.get('overlay.update_pos_delay_ms'))
    
    
    def _init_window(self) -> None:
        self.setWindowTitle('MainOverlay')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        hwnd = int(self.winId())
        GWL_EXSTYLE = -20
        WS_EX_LAYERED = 0x00080000
        WS_EX_TRANSPARENT = 0x00000020
        
        current_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        new_style = current_style | WS_EX_LAYERED | WS_EX_TRANSPARENT
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, new_style)
        
    
    def _init_ui(self) -> None:
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.movie = QMovie()
        self.movie.frameChanged.connect(self.update)
        self.movie.setScaledSize(QSize(5, 5)) # Bug fix
        
        self.label = QLabel() # Container for movie :/
        
        layout.addWidget(self.label)

        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
    
    
    @Slot()
    def _update_window_pos(self) -> None:
        rect, type, wname, hwnd = get_target_window()
        x, y, w, h = rect
        overlay = self.size()
        
        if type == 'window' or type == 'cursor':
        
            if rect != self.prev_rect:
                
                pos = calculate.window_cursor(x, y, w, h, overlay)
                if pos[1] <= 0:
                    rect, type, wname, hwnd = get_target_window(True)
                    x, y, w, h = rect
                    
                    pos = calculate.desktop(x, y, w, h, overlay)
                
                self.move(*pos)
                
                self.prev_rect = rect
        
        elif type == 'desktop':
            
            if rect != self.prev_rect:
                
                pos = calculate.desktop(x, y, w, h, overlay)
                self.move(*pos)
                
                self.prev_rect = rect
        
    
    def set_movie(self, path: str, reload: bool=False) -> None:
        if path == self.path and not reload:
            return 
        
        self.path = path
        temp_movie = QMovie(path)
        temp_movie.jumpToNextFrame()
        
        self.gif_size = temp_movie.frameRect()
        
        temp_movie.stop()
        temp_movie.deleteLater()
        
        self.movie.stop()
        self.movie.setFileName(path)
        self.movie.start()
            
        self.__set_scale()
        
    
    def __set_scale(self) -> None:
        size = QSize(
            int(self.gif_size.width() * self.scale), 
            int(self.gif_size.height() * self.scale)
        )
        
        self.prev_rect = (0, 0, 0, 0)
        self.movie.setScaledSize(size)
        self.setFixedSize(size)
    
    
    def set_scale(self, scale: float) -> None:
        self.scale = scale
        
        if self.path:
            self.set_movie(self.path, True)
    
    
    def get_movie(self) -> str:
        return self.path
    
    
    def get_scale(self) -> float:
        return self.scale
    
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        if self.movie.isValid():
            painter.drawPixmap(0, 0, self.movie.currentPixmap())
    
    
    def closeEvent(self, event: QCloseEvent) -> None:
        QApplication.instance().quit()
        super().closeEvent(event)
    
    
    def mousePressEvent(self, event):
        event.ignore()
        
    def mouseReleaseEvent(self, event):
        event.ignore()
        
    def mouseDoubleClickEvent(self, event):
        event.ignore()
        
    def mouseMoveEvent(self, event):
        event.ignore()
        
    def wheelEvent(self, event):
        event.ignore()
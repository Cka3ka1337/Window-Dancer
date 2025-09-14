import ctypes

import numpy as np

from scipy import interpolate
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout,
    QLabel, QWidget
)
from PySide6.QtCore import (
    Qt, QSize, QTimer, Slot
)
from PySide6.QtGui import (
    QMovie, QPainter, QPaintEvent
)

from scripts.shared import SharedData
from scripts.targets import get_target_position
from scripts.config_system import ConfigSystem
from scripts.interpolation import Interpolation
from modules.components.gif_view import GifView


class MainOverlay(QMainWindow):
    shared = SharedData()
    config = ConfigSystem()
    interpolation = Interpolation()
    
    smooth = 0.125 if config.get('startup.smooth') is None else config.get('startup.smooth')
    
    target = (0, 0)
    previous = (0, 0)
    current = (0, 0)
    
    
    
    def __init__(self):
        super().__init__()
        self.movie = GifView(self.setFixedSize)
        self.overlay_pos = [self.pos().x(), self.pos().y()]
        
        self._init_window()
        self._init_ui()
        self._init_timers()
        self._init_hooks()
        
    
    def _init_hooks(self) -> None:
        self.shared.set('movie.get', self.movie.get_movie)
        self.shared.set('movie.set', self.movie.set_movie)
        self.shared.set('scale.get', self.movie.get_scale)
        self.shared.set('scale.set', self.movie.set_scale)
        self.shared.set('smooth.get', self.get_smooth)
        self.shared.set('smooth.set', self.set_smooth)
        
        self.shared.set('target.get', self.get_target)
        self.shared.set('previous.get', self.get_previous)
        self.shared.set('current.get', self.get_current)
        
        self.movie.frameChanged.connect(self.update)
    
    
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
        
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
    
    
    @Slot()
    def _update_window_pos(self) -> None:
        target = get_target_position(self.size())
        animated_movement = bool(self.shared.get('animated_movement'))

        
        offset_x, offset_y = self.interpolation.next(self.overlay_pos.copy(), target, self.smooth)
        self.overlay_pos[0] += offset_x
        self.overlay_pos[1] += offset_y
        
        # self.move(round(self.overlay_pos[0]), round(self.overlay_pos[1]))
        self.move(self.overlay_pos[0], self.overlay_pos[1])
    
    
    def get_target(self) -> tuple:
        return self.target
    
    
    def get_previous(self) -> tuple:
        return self.previous

    
    def get_current(self) -> tuple:
        return self.current

    
    def set_smooth(self, value: float) -> None:
        self.smooth = (self.transform(value / 100))

    
    def get_smooth(self, transform=True) -> float:
        if transform:
            value = self.transform(self.smooth)
        else:
            value = self.smooth
        return value
    
    
    def transform(self, value: float, min=0.05, max=0.25) -> float:
        # Transforming value through normalization, scaling and denormalization.
        delta = max - min
        difference = (value / max * 100)
        scale = (-1 - max) / 100 * difference + (1 + max)

        return min + delta * scale
    
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        if self.movie.isValid():
            painter.drawPixmap(0, 0, self.movie.currentPixmap())
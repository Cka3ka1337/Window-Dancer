import ctypes

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget
)
from PySide6.QtCore import (
    Qt, QTimer, Slot
)
from PySide6.QtGui import (
    QPainter, QPaintEvent
)

from scripts.constants import *
from scripts.shared import SharedData
from scripts.config_system import ConfigSystem
from scripts.targets import get_target_position
from modules.components.gif_view import GifView
from scripts.interpolation import Instant, Linear, SmoothedDirection


class MainOverlay(QMainWindow):
    shared = SharedData()
    config = ConfigSystem()
    
    instant = Instant()
    linear = Linear()
    SDInterpolation = SmoothedDirection()
    
    smooth = config.get(ConfigKeys.SMOOTH, InterpolationParams.SMOOTHNESS_DEFAULT)
    min = InterpolationParams.SMOOTHNESS_MIN
    max = InterpolationParams.SMOOTHNESS_MAX
    
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
        self.shared.set(Methods.MOVIE_GET,      self.movie.get_movie)
        self.shared.set(Methods.MOVIE_SET,      self.movie.set_movie)
        self.shared.set(Methods.SCALE_GET,      self.movie.get_scale)
        self.shared.set(Methods.SCALE_SET,      self.movie.set_scale)
        self.shared.set(Methods.SMOOTH_GET,           self.get_smooth)
        self.shared.set(Methods.SMOOTH_SET,           self.set_smooth)
        self.shared.set(Methods.TARGET_GET,           self.get_target)
        self.shared.set(Methods.CURRENT_GET,          self.get_current)
        self.shared.set(Methods.PREVIOUS_GET,         self.get_previous)
        
        self.movie.frameChanged.connect(self.update)
    
    
    def _init_timers(self) -> None:
        self.update_window_pos_timer = QTimer()
        self.update_window_pos_timer.timeout.connect(self._update_window_pos)
        self.update_window_pos_timer.start(self.config.get(ConfigKeys.UPDATE_OVERLAY_DELAY, ConfigDefaults.UPDATE_OVERLAY_DELAY))
    
    
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
        # print(self.smooth)
        target = get_target_position(self.size())
        animated_movement = self.shared.get(Variables.ANIMATED_MOVEMENT)
        
        # offset_x, offset_y = self.SDInterpolation.next(self.overlay_pos.copy(), target, self.transform(self.smooth) / InterpolationParams.SMOOTHNESS_DEVIDER)
        offset_x, offset_y = self.linear.next(self.overlay_pos.copy(), target, self.transform(self.smooth) / InterpolationParams.SMOOTHNESS_DEVIDER)
        
        self.overlay_pos[0] += offset_x
        self.overlay_pos[1] += offset_y
        
        self.move(self.overlay_pos[0], self.overlay_pos[1])
    
    
    def get_target(self) -> tuple:
        return self.target
    
    
    def get_previous(self) -> tuple:
        return self.previous

    
    def get_current(self) -> tuple:
        return self.current

    
    def set_smooth(self, value: float) -> None:
        self.smooth = value

    
    def get_smooth(self) -> float:
        return self.smooth
    
    
    def transform(self, value: float) -> float:
        min = InterpolationParams.SMOOTHNESS_MIN
        max = InterpolationParams.SMOOTHNESS_MAX
        
        if value < min or value > max:
            result = max
            assert OverflowError('OutOfRange')
        
        result = min + max * (-1 / max * value + 1)
        
        return result
    
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        if self.movie.isValid():
            painter.drawPixmap(0, 0, self.movie.currentPixmap())
import ctypes

import numpy as np

from scipy import interpolate
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout,
    QLabel, QWidget, QGroupBox,
    QHBoxLayout
)
from PySide6.QtCore import (
    Qt, QSize, QTimer, Slot
)
from PySide6.QtGui import (
    QMovie, QPainter, QPaintEvent, QPen
)

from scripts.shared import SharedData
from scripts.targets import get_target_position
from scripts.config_system import ConfigSystem


class InteractiveInterpolation(QMainWindow):
    shared = SharedData()
    
    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_ui()
        self._init_timers()
        
    
    def _init_timers(self) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)
    
    
    def _init_window(self) -> None:
        self.move(0, 0)
        self.setFixedSize(1920, 1080)
        self.setWindowTitle('Interpolation demonstration')
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
        layout_v = QVBoxLayout(central_widget)
        layout_h = QHBoxLayout(central_widget)
        layout_v.addLayout(layout_h)
        
        box = QGroupBox('Interpolation')
        box_layout = QHBoxLayout(box)
        
        box_layout.addWidget(QLabel('Interpolation demonstration'))
        
        layout_h.addWidget(box)
        layout_h.addStretch()
        layout_v.addStretch()
        
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout_v)
    
    
    def draw_interpolation(self, painter, algorithm, color):
        target = self.shared.get('target.get')()
        previous = self.shared.get('previous.get')()
        current = self.shared.get('current.get')()
        
        points = self.parametric_interpolation([previous, current, target], algorithm, 1000)
        if points[0] is None:
            return

        pen = QPen()
        pen.setWidth(2)
        
        pen.setColor(color)
        painter.setPen(pen)
        
        for x, y in zip(*points):
            painter.drawPoint(x, y)  # Точка в координатах (50, 50)
    
    
    @Slot()
    def paintEvent(self, event):
        painter = QPainter(self)
        
        self.draw_interpolation(painter, interpolate.CubicSpline, Qt.cyan)
        # self.draw_interpolation(painter, interpolate.Akima1DInterpolator, Qt.red)
        # self.draw_interpolation(painter, interpolate.PchipInterpolator, Qt.blue)
    

    def parametric_interpolation(self, points, algorithm, num_points=5):
        points = np.array(points)
        
        t = np.zeros(len(points))
        for i in range(1, len(points)):
            dx = points[i, 0] - points[i - 1, 0]
            dy = points[i, 1] - points[i - 1, 1]
            t[i] = t[i - 1] + np.sqrt(dx ** 2 + dy ** 2)
        
        t_norm = t / t[-1]
        
        t_dense = np.linspace(0, 1, num_points)
        
        try:
            interp_x = algorithm(t_norm, points[:, 0])
            interp_y = algorithm(t_norm, points[:, 1])

            x_interp = interp_x(t_dense)
            y_interp = interp_y(t_dense)
            
            return x_interp, y_interp
            
        except Exception as e:
            return None, None
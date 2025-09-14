import ctypes

import numpy as np

from scipy import interpolate
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout,
    QLabel, QWidget, QGroupBox,
    QHBoxLayout
)
from PySide6.QtCore import (
    Qt, QTimer, Slot
)
from PySide6.QtGui import (
    QPainter, QPaintEvent, QPen
)

from scripts.shared import SharedData
from scripts.interpolation import parametric_interpolation


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
        layout_h = QHBoxLayout()
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
        
        points = parametric_interpolation([previous, current, target], algorithm, 1000)
        if not points:
            return

        pen = QPen()
        pen.setWidth(2)
        
        pen.setColor(color)
        painter.setPen(pen)
        
        for x, y in points:
            painter.drawPoint(x, y)
    
    
    @Slot()
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        
        self.draw_interpolation(painter, interpolate.CubicSpline, Qt.cyan)
        self.draw_interpolation(painter, interpolate.Akima1DInterpolator, Qt.red)
        self.draw_interpolation(painter, interpolate.PchipInterpolator, Qt.green)
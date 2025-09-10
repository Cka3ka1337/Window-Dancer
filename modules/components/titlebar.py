from PySide6.QtWidgets import (
    QHBoxLayout, QWidget,
    QLabel, QPushButton
)
from PySide6.QtCore import (
    Signal
)

from .buttons import (
    TitleBarButton
)


class TitleBar(QWidget):
    closed = Signal()
    minimized = Signal()
    maximized = Signal()
    
    
    def __init__(self, title: str):
        super().__init__()
        self.title = title
    
    
    def init_ui(self):
        self._setup_ui(self.title)
        self._setup_signals()
    
    
    def _setup_ui(self, title) -> None:
        layout = QHBoxLayout(self)
        self.setFixedHeight(14)
        self.title_label = QLabel(title)
        
        self.min_btn = TitleBarButton('#ffbd44', '#f0ad4e')
        self.close_btn = TitleBarButton('#ed6a5e', '#da5448')
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)
    
    
    def _setup_signals(self):
        self.close_btn.clicked.connect(self.closed)
        self.min_btn.clicked.connect(self.minimized)
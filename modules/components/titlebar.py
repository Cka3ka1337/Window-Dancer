from PySide6.QtWidgets import (
    QHBoxLayout, QWidget, QLabel
)

from modules.components.buttons import TitleBarButton


class TitleBar(QWidget):
    def __init__(self, title: str, close, minimized):
        super().__init__()
        self.closed = close
        self.minimized = minimized
        
        self._init_ui(title)
        self._init_signals()
    
    
    def _init_ui(self, title: str) -> None:
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
    
    
    def _init_signals(self) -> None:
        self.close_btn.clicked.connect(self.closed)
        self.min_btn.clicked.connect(self.minimized)
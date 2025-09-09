from PySide6.QtWidgets import (
    QHBoxLayout, QWidget,
    QLabel, QPushButton
)
from PySide6.QtCore import (
    Signal
)


class ButtonMin(QPushButton):
    def __init__(self):
        super().__init__('')


class ButtonClose(QPushButton):
    def __init__(self):
        super().__init__('')


class TitleLabel(QLabel):
    def __init__(self, *args):
        super().__init__(*args)


class TitleBar(QWidget):
    closed = Signal()
    minimized = Signal()
    maximized = Signal()
    
    def __init__(self, title: str):
        super().__init__()
        
        self._setup_ui(title)
        self._setup_signals()
    
    
    def _setup_ui(self, title) -> None:
        layout = QHBoxLayout(self)
        self.title_label = TitleLabel(title)
        self.min_btn = ButtonMin()
        self.close_btn = ButtonClose()
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        layout.addWidget(self.title_label)
        layout.addStretch()
        layout.addWidget(self.min_btn)
        layout.addWidget(self.close_btn)
    
    
    def _setup_signals(self):
        if hasattr(self, 'close_btn'):
            self.close_btn.clicked.connect(self.closed.emit)
            
        if hasattr(self, 'min_btn'):
            self.min_btn.clicked.connect(self.minimized.emit)
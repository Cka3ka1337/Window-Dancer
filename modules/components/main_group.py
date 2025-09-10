from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout
)
from .buttons import ChoiceGifButton


class MainGroup(QGroupBox):
    def __init__(self, set_movie, set_scale):
        super().__init__()
        self.set_movie = set_movie
        self.set_scale = set_scale
        self._init_ui()
        
    
    def _init_ui(self) -> None:
        vertical = QVBoxLayout(self)
        self.choice_gif_btn = ChoiceGifButton('Choice animation', self.set_movie)
        
        vertical.addWidget(self.choice_gif_btn)
        vertical.addStretch()
        
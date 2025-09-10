from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout
)
from .buttons import ChoiceGifButton


class MainGroup(QGroupBox):
    set_movie = None
    set_scale = None
    
    def __init__(self):
        super().__init__()
        
    
    def init_ui(self) -> None:
        vertical = QVBoxLayout(self)
        self.choice_gif_btn = ChoiceGifButton('Choice animation')
        self.choice_gif_btn.set_movie = self.set_movie
        
        vertical.addWidget(self.choice_gif_btn)
        vertical.addStretch()
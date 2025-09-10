from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout
)
from .buttons import ChoiceGifButton
from .slider import ScaleSlider


class MainGroup(QGroupBox):
    set_movie = None
    set_scale = None
    
    def __init__(self):
        super().__init__()
        
    
    def init_ui(self) -> None:
        vertical = QVBoxLayout(self)
        self.choice_gif_btn = ChoiceGifButton('Choice animation')
        self.choice_gif_btn.set_movie = self.set_movie
        
        slider_group = QGroupBox('Scale')
        slider_layout = QHBoxLayout(slider_group)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        self.scale_slider = ScaleSlider(5, 100, 50, 100)
        self.scale_slider.set_scale = self.set_scale
        self.scale_slider.update_scale()
        slider_layout.addWidget(self.scale_slider)
        
        vertical.addWidget(self.choice_gif_btn)
        vertical.addWidget(slider_group)
        vertical.addStretch()
from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout
)
from .buttons import ChoiceGifButton, SetStartupButtom, ClearStartupButtom
from .slider import ScaleSlider


class MainGroup(QGroupBox):
    set_movie = None
    set_scale = None
    get_movie = None
    get_scale = None
    
    def __init__(self):
        super().__init__()
        
    
    def init_ui(self) -> None:
        vertical = QVBoxLayout(self)
        
        slider_group = QGroupBox('Scale')
        slider_layout = QHBoxLayout(slider_group)
        config_layout = QHBoxLayout()
        
        self.scale_slider = ScaleSlider(5, 100, 50, 100)
        self.scale_slider.set_scale = self.set_scale
        self.scale_slider.update_scale()
        
        self.choice_gif_btn = ChoiceGifButton('Choice animation')
        self.choice_gif_btn.set_movie = self.set_movie
        
        self.config_set_btn = SetStartupButtom('Set Startup')
        self.config_set_btn.get_movie = self.get_movie
        self.config_set_btn.get_scale = self.get_scale
        
        self.config_clear_btn = ClearStartupButtom('Clear Startup')
        self.config_clear_btn.get_movie = self.get_movie
        self.config_clear_btn.get_scale = self.get_scale
        
        slider_layout.setContentsMargins(0, 0, 0, 0)
        
        slider_layout.addWidget(self.scale_slider)
        config_layout.addWidget(self.config_clear_btn)
        config_layout.addWidget(self.config_set_btn)
        
        vertical.addWidget(self.choice_gif_btn)
        vertical.addWidget(slider_group)
        vertical.addStretch()
        vertical.addLayout(config_layout)
        
        
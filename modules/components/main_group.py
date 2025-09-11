from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout
)

from modules.components.buttons import (
    ChoiceGifButton, SetStartupButtom, ClearStartupButtom)
from modules.components.slider import ScaleSlider
from modules.components.check_box import CheckBox


class MainGroup(QGroupBox):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    
    def init_ui(self) -> None:
        vertical = QVBoxLayout(self)
        slider_group = QGroupBox('Scale')
        slider_layout = QHBoxLayout(slider_group)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        config_layout = QHBoxLayout()
        
        self.scale_slider = ScaleSlider(5, 100, 50, 100)
        self.config_set_btn = SetStartupButtom('Set Startup')
        self.config_clear_btn = ClearStartupButtom('Clear Startup')
        self.choice_gif_btn = ChoiceGifButton('Choice animation')
        self.animated_movement = CheckBox(
            'checkbox.animated_movement',
            'Animated Overlay Movement'
        )
        
        slider_layout.addWidget(self.scale_slider)
        
        config_layout.addWidget(self.config_clear_btn)
        config_layout.addWidget(self.config_set_btn)
        
        vertical.addWidget(self.choice_gif_btn)
        vertical.addWidget(slider_group)
        vertical.addWidget(self.animated_movement)
        vertical.addStretch()
        vertical.addLayout(config_layout)
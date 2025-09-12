from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Slot

from scripts.shared import SharedData
from modules.components.slider import Slider
from modules.components.check_box import CheckBox
from modules.components.buttons import (
    ChoiceGifButton, SetStartupButtom, ClearStartupButtom)


class MainGroup(QGroupBox):
    shared = SharedData()
    
    def __init__(self):
        super().__init__()
        self._init_buttons()
        self._init_sliders()
        self._init_ui()
    
    
    def _init_sliders(self) -> None:
        self.scale_slider = Slider('scale', 5, 100, 100) # 0.05-1.0
        self.scale_slider.valueChanged.connect(self.slot)
        
        self.smoothness_slider = Slider('smooth', 5, 25, 1) # 0.05 - 0.25
        self.smoothness_slider.valueChanged.connect(self.slot)
        
    
    def _init_buttons(self) -> None:    
        self.config_set_btn = SetStartupButtom('Set Startup')
        self.config_clear_btn = ClearStartupButtom('Clear Startup')
        self.choice_gif_btn = ChoiceGifButton('Choice animation')
        self.animated_movement = CheckBox(
            'animated_movement',
            'Smooth movement'
        )
    
    
    def _init_ui(self) -> None:
        # Inits
        vertical = QVBoxLayout(self)
        
        slider_group = QGroupBox('Scale')
        slider_layout = QHBoxLayout(slider_group)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        
        smoothness_group = QGroupBox('Smoothness')
        smoothness_layout = QHBoxLayout(smoothness_group)
        smoothness_layout.setContentsMargins(0, 0, 0, 0)
        
        config_layout = QHBoxLayout()
        
        # adds
        slider_layout.addWidget(self.scale_slider)
        smoothness_layout.addWidget(self.smoothness_slider)
        
        config_layout.addWidget(self.config_clear_btn)
        config_layout.addWidget(self.config_set_btn)
        
        vertical.addWidget(self.choice_gif_btn)
        vertical.addWidget(slider_group)
        vertical.addWidget(smoothness_group)
        vertical.addWidget(self.animated_movement)
        
        vertical.addStretch()
        vertical.addLayout(config_layout)
    
    
    @Slot()
    def slot(self, value) -> None:
        sender = self.sender()
        func = self.shared.get(f'{sender.path}.set')
        if func is None:
            return
        
        func(value / sender.divider)
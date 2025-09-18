from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout

from scripts.constants import *
from scripts.shared import SharedData
from modules.components.slider import Slider
from modules.components.check_box import CheckBox
from modules.components.combo_box import ComboBox
from scripts.config_system import ConfigSystem
from modules.components.buttons import (
    ChoiceGifButton, SetStartupButtom, ClearStartupButtom)


class MainGroup(QGroupBox):
    shared = SharedData()
    config = ConfigSystem()
    
    
    def __init__(self):
        super().__init__()
        self._init_elements()
        self._init_ui()
    
    
    def _init_elements(self) -> None:
        self.scale_slider = Slider(
            Methods.SCALE_GET,
            Methods.SCALE_SET,
            Ui.SCALE_MIN,
            Ui.SCALE_MAX
        )
        self.scale_slider.valueChanged.connect(self.slot)
        
        self.smoothness_slider = Slider(
            Methods.SMOOTH_GET,
            Methods.SMOOTH_SET,
            Ui.SMOOTHNESS_MIN,
            Ui.SMOOTHNESS_MAX
        )
        self.smoothness_slider.valueChanged.connect(self.slot)
        
        self.config_set_btn = SetStartupButtom('Set Startup')
        self.config_clear_btn = ClearStartupButtom('Clear Startup')
        self.choice_gif_btn = ChoiceGifButton('Choice animation')
        self.interpolation_combo = ComboBox(InterpolationParams.INTERPOLATION_TYPES, 'Movement Mode', Variables.INTERPOLATION_TYPE)
        self.interpolation_combo.slot(self.config.get(ConfigKeys.INTERPOLATION_TYPE, ConfigDefaults.INTERPOLATION_TYPE))
    
    
    def _init_ui(self) -> None:
        vertical = QVBoxLayout(self)
        
        slider_group = QGroupBox('Scale')
        slider_layout = QHBoxLayout(slider_group)
        slider_layout.setContentsMargins(0, 0, 0, 0)
        
        smoothness_group = QGroupBox('Smoothness')
        smoothness_layout = QHBoxLayout(smoothness_group)
        smoothness_layout.setContentsMargins(0, 0, 0, 0)
        
        interpolation_group = QGroupBox('Movement mode')
        interpolation_layout = QHBoxLayout(interpolation_group)
        # interpolation_layout.setContentsMargins(0, 0, 0, 0)
        
        config_layout = QHBoxLayout()
        
        # adds
        slider_layout.addWidget(self.scale_slider)
        smoothness_layout.addWidget(self.smoothness_slider)
        interpolation_layout.addWidget(self.interpolation_combo)
        
        config_layout.addWidget(self.config_clear_btn)
        config_layout.addWidget(self.config_set_btn)
        
        vertical.addWidget(self.choice_gif_btn)
        vertical.addWidget(slider_group)
        vertical.addWidget(smoothness_group)
        vertical.addWidget(interpolation_group)
        
        vertical.addStretch()
        vertical.addLayout(config_layout)
    
    
    @Slot()
    def slot(self, value) -> None:
        sender = self.sender()
        
        func = self.shared.get(sender.set_id)
        
        if func is None:
            return
        
        func(value)
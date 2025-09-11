from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt, Slot

from scripts.shared import SharedData
# from scripts.config_system import ConfigSystem


class ScaleSlider(QSlider):
    shared = SharedData()
    
    def __init__(self,
                 min: int=0,
                 max: int=100,
                 default: int=50,
                 divider: float=1):
        super().__init__(Qt.Orientation.Horizontal)
        
        self.min = min
        self.max = max
        self.default = default
        self.divider = divider
        
        self.setMinimum(self.min)
        self.setMaximum(self.max)
        self.setValue(self.default)
        
        self.valueChanged.connect(self.update_scale)
        self.update_scale()
        
    
    @Slot()
    def update_scale(self) -> None:
        set_scale = self.shared.get('scale.set')
        if set_scale is None:
            return
        
        set_scale(self.value() / self.divider)
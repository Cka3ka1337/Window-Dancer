from PySide6.QtWidgets import (
    QSlider
)
from PySide6.QtCore import (
    Qt
)


class ScaleSlider(QSlider):
    set_scale = None
    
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
        
        self.setMinimum(min)
        self.setMaximum(max)
        self.setValue(default)
        
        self.valueChanged.connect(self.update_scale)
        
    
    def update_scale(self) -> None:
        self.set_scale(self.value() / self.divider)
    

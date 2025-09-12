from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

from scripts.shared import SharedData


class Slider(QSlider):
    shared = SharedData()
    
    def __init__(self,
                 path: str,
                 min: int=0,
                 max: int=100,
                 divider: float=1,
                 ):
        super().__init__(Qt.Orientation.Horizontal)
        
        self.path = path
        self.min = min
        self.max = max
        self.divider = divider
        
        self.setMinimum(self.min)
        self.setMaximum(self.max)
        
        if path != 'smooth':
            value = self.shared.get(f'{self.path}.get')()
            self.set_scale(value)
        
        else:
            value = self.shared.get(f'{self.path}.get')() * 100
            self.setValue(value)
            print('SliderSet', value)
    
    
    def set_scale(self, scale: float) -> None:
        # print(scale, 'SetSlider', self.min + (self.max - self.min) * scale)
        self.setValue(
            self.min + (self.max - self.min) * scale
        )
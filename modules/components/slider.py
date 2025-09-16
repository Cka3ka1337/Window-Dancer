from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt

from scripts.constants import *
from scripts.shared import SharedData


class Slider(QSlider):
    shared = SharedData()
    
    def __init__(self,
                 get_id: int,
                 set_id: int,
                 min: int=0,
                 max: int=100
                 ):
        super().__init__(Qt.Orientation.Horizontal)
        
        self.get_id = get_id
        self.set_id = set_id
        self.min = min
        self.max = max
        
        self.setMinimum(self.min)
        self.setMaximum(self.max)
        
        value = self.shared.get(self.get_id)()
        self.setValue(value)
        
    
    # def set_scale(self, scale: float) -> None:
    #     self.setValue(
    #         scale
    #     )
    #     print(self.min + (self.max - self.min) * scale, self.get_id, scale)
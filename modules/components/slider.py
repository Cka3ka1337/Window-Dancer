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
                 max: int=100,
                 divider: float=1,
                 ):
        super().__init__(Qt.Orientation.Horizontal)
        
        self.get_id = get_id
        self.set_id = set_id
        self.min = min
        self.max = max
        self.divider = divider
        
        self.setMinimum(self.min)
        self.setMaximum(self.max)
        
        # if get_id == Methods.SMOOTH_GET:
        #     value = self.shared.get(Methods.SMOOTH_GET)() * 100
        #     self.setValue(value)
            
        # else:
        #     value = self.shared.get(Methods.SCALE_GET)()
        #     self.set_scale(value)
        
    
    def set_scale(self, scale: float) -> None:
        self.setValue(
            self.min + (self.max - self.min) * scale
        )
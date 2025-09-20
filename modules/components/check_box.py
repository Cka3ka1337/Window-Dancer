from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from scripts.shared import SharedData
from scripts.config_system import ConfigSystem


class CheckBox(QCheckBox):
    config = ConfigSystem()
    
    
    def __init__(self, path: str, text: str):
        super().__init__(text)
        self.shared = SharedData()
        self.path = path
        self.stateChanged.connect(self.updated)
        
        value = self.config.get(path)
        self.setChecked(value if value is not None else False)
        self.updated()
    
    
    @Slot()
    def updated(self, *args) -> None:
        self.shared.set(self.path, self.isChecked())
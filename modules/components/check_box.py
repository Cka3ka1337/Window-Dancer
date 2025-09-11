from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from scripts.shared import SharedData


class CheckBox(QCheckBox):
    def __init__(self, path: str, text: str):
        super().__init__(text)
        self.shared = SharedData()
        self.path = path
        self.stateChanged.connect(self.updated)
    
    
    @Slot()
    def updated(self, *args) -> None:
        self.shared.set(self.path, self.isChecked())
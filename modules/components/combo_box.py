from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QComboBox, QStyledItemDelegate, QSizePolicy

from scripts.constants import *
from scripts.shared import SharedData
from scripts.config_system import ConfigSystem


class CenteredItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        
        super().paint(painter, option, index)
        

class ComboBox(QComboBox):
    shared = SharedData()
    config = ConfigSystem()
    
    def __init__(self, items: list[str], tooltip: str='', shared_id: int=-1):
        super().__init__()
        self.addItems(items)
        self.setMaxVisibleItems(99)
        self.setToolTip(tooltip)
        
        self.setItemDelegate(CenteredItemDelegate())
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        self.items = items
        self.shared_id = shared_id
        self.currentIndexChanged.connect(self.slot)
            
    
    @Slot()
    def slot(self, e):
        self.shared.set(self.shared_id, e)
        self.setCurrentText(self.items[e])
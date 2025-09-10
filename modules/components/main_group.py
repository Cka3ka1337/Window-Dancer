from PySide6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout
)
from .buttons import ChoiceGifButton


class MainGroup(QGroupBox):
    def __init__(self):
        super().__init__()
        
        vertical = QVBoxLayout(self)
        vertical.addWidget(ChoiceGifButton('Choice'))
        
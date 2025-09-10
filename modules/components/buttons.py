from PySide6.QtWidgets import (
    QPushButton
)


class TitleBarButton(QPushButton):
    def __init__(self, color: any, hover_color: any):
        super().__init__('')

        style = f'''
        TitleBarButton {{
            background-color: {color};
            border-radius: 6px;
            width: 12px;
            height: 12px;
            border: none;
        }}
            
        TitleBarButton:hover {{
            background-color: {hover_color};
        }}
        '''
        self.setStyleSheet(style)

        
class ChoiceGifButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
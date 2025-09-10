from PySide6.QtWidgets import (
    QPushButton, QFileDialog
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
    def __init__(self, text: str, set_movie):
        super().__init__(text)
        self.set_movie = set_movie
        self.clicked.connect(self.open_file_dialog)
        
    
    def open_file_dialog(self) -> None:
        path, filter = QFileDialog.getOpenFileName(
            parent=None,
            caption='Select content',
            dir='.',
            filter="Anim Files (*.gif)"
        )
        
        if not path:
            return
        
        if self.set_movie is not None:
            self.set_movie(path)
from PySide6.QtWidgets import (
    QPushButton, QFileDialog
)

from scripts.config_system import ConfigSystem


class SetStartupButtom(QPushButton):
    get_movie = None
    get_scale = None
    config = ConfigSystem()
    
    def __init__(self, title: str):
        super().__init__(title)
        self.clicked.connect(self.set_startup)
        
    
    def set_startup(self) -> None:
        if self.get_movie is None or self.get_scale is None:
            return
        
        self.config.set('startup.path', self.get_movie())
        self.config.set('startup.scale', self.get_scale())


class ClearStartupButtom(QPushButton):
    get_movie = None
    get_scale = None
    config = ConfigSystem()
    
    def __init__(self, title: str):
        super().__init__(title)
        self.clicked.connect(self.set_startup)
        
    
    def set_startup(self) -> None:
        if self.get_movie is None or self.get_scale is None:
            return
        
        self.config.set('startup.path', '')
        self.config.set('startup.scale', 0.5)


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
    set_movie = None
    
    def __init__(self, text: str):
        super().__init__(text)
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
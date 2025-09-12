from PySide6.QtWidgets import QPushButton, QFileDialog

from scripts.shared import SharedData
from scripts.config_system import ConfigSystem


class SetStartupButtom(QPushButton):
    config = ConfigSystem()
    shared = SharedData()
    
    def __init__(self, title: str):
        super().__init__(title)
        self.clicked.connect(self.set_startup)
        
    
    def set_startup(self) -> None:
        get_movie = self.shared.get('movie.get')
        get_scale = self.shared.get('scale.get')
        get_smoot = self.shared.get('smooth.get')
        
        if set is None:
            return
        
        self.config.set('startup.path', get_movie())
        self.config.set('startup.scale', get_scale())
        self.config.set('startup.animated_movement', self.shared.get('animated_movement'))
        self.config.set('startup.smooth', get_smoot(False))


class ClearStartupButtom(QPushButton):
    config = ConfigSystem()
    
    def __init__(self, title: str):
        super().__init__(title)
        self.clicked.connect(self.set_startup)
        
    
    def set_startup(self) -> None:
        self.config.set('startup.path', '')
        self.config.set('startup.scale', 0.5)
        self.config.set('startup.animated_movement', False)
        self.config.set('startup.smoothness', 0.125)


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
    shared = SharedData()
    
    def __init__(self, text: str):
        super().__init__(text)
        self.clicked.connect(self.open_file_dialog)
        
    
    def open_file_dialog(self) -> None:
        set_movie = self.shared.get('movie.set')
        if set_movie is None:
            return
        
        path, _ = QFileDialog.getOpenFileName(
            parent=None,
            caption='Select content',
            dir='.',
            filter="Anim Files (*.gif);;All Files (*)"
        )
        
        if not path:
            return
        
        set_movie(path)
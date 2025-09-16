from PySide6.QtWidgets import QPushButton, QFileDialog

from scripts.constants import *
from scripts.shared import SharedData
from scripts.config_system import ConfigSystem


class SetStartupButtom(QPushButton):
    config = ConfigSystem()
    shared = SharedData()
    
    
    def __init__(self, title: str):
        super().__init__(title)
        self.clicked.connect(self.set_startup)
        
    
    def set_startup(self) -> None:
        self.config.set(ConfigKeys.PATH,              self.shared.get(Methods.MOVIE_GET)())
        self.config.set(ConfigKeys.SCALE,             self.shared.get(Methods.SCALE_GET)())
        self.config.set(ConfigKeys.ANIMATED_MOVEMENT, self.shared.get(Variables.ANIMATED_MOVEMENT))
        self.config.set(ConfigKeys.SMOOTH,            self.shared.get(Methods.SMOOTH_GET)())
        self.config.save_config()


class ClearStartupButtom(QPushButton):
    config = ConfigSystem()
    
    
    def __init__(self, title: str):
        super().__init__(title)
        self.clicked.connect(self.set_startup)
        
    
    def set_startup(self) -> None:
        self.config.set(ConfigKeys.PATH,              ConfigDefaults.PATH)
        self.config.set(ConfigKeys.scale,             ConfigDefaults.SCALE)
        self.config.set(ConfigKeys.ANIMATED_MOVEMENT, ConfigDefaults.ANIMATED_MOVEMENT)
        self.config.set(ConfigKeys.SMOOTH,            ConfigDefaults.SMOOTH)
        self.config.save_config()


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
        set_movie = self.shared.get(Methods.MOVIE_SET)
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
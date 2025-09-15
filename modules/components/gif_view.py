from PySide6.QtGui import QMovie
from PySide6.QtCore import QSize

from scripts.constants import *
from scripts.shared import SharedData
from scripts.config_system import ConfigSystem


class GifView(QMovie):
    shared = SharedData()
    config = ConfigSystem()
    
    path = config.get(ConfigKeys.PATH, ConfigDefaults.PATH)
    scale = config.get(ConfigKeys.SCALE, ConfigDefaults.SCALE)
    gif_size = None
    
    
    def __init__(self, setFixedSize):
        super().__init__()
        self.setScaledSize(QSize(5, 5))
        self.setFixedSize = setFixedSize
        self.set_scale(self.scale)
        self.set_movie(self.path, True)
    
    
    def set_movie(self, path: str, reload: bool=False) -> None:
        if (path == self.path and not reload) or not path:
            return 
        
        self.path = path
        temp_movie = QMovie(path)
        temp_movie.jumpToNextFrame()
        
        self.gif_size = temp_movie.frameRect()
        
        temp_movie.stop()
        temp_movie.deleteLater()
        
        self.stop()
        self.setFileName(path)
        self.start()
            
        self.__set_scale()
        
    
    def __set_scale(self) -> None:
        size = QSize(
            int(self.gif_size.width() * self.scale), 
            int(self.gif_size.height() * self.scale)
        )
        
        self.setScaledSize(size)
        self.setFixedSize(size)
    
    
    def set_scale(self, scale: float) -> None:
        self.scale = scale
        
        if self.path:
            self.set_movie(self.path, True)
    
    
    def get_movie(self) -> str:
        return self.path
    
    
    def get_scale(self) -> float:
        return self.scale
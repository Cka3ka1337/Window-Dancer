from PySide6.QtCore import Signal, QObject


class SharedData(QObject):
    __instance = None
    change_event = Signal(tuple)
    _shared_data = {}
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SharedData, cls).__new__(cls)
            cls.__instance._shared_data = {}
            
        return cls.__instance
    
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True
    
    
    def get(self, path: str):
        path = str(path)
        path = path.split('.')
        result = self._shared_data
        
        for p in path:
            result = result.get(p)
            
            if result is None:
                return None
        
        return result
    

    def set(self, path: str, value):
        path = str(path)
        _path = path.split('.')
        result = self._shared_data
        
        for p in _path[:-1]:
            if p not in result:
                result[p] = {}
            
            result = result[p]
        
        result[_path[-1]] = value
        self.change_event.emit((path, value))
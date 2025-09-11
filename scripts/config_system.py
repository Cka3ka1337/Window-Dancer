import os

import tomli
import tomli_w
import win32api

from pathlib import Path


class ConfigSystem:
    __instance = None
    _config_path = os.path.join(
        win32api.GetSystemDirectory()[:2],
        'Users',
        os.getlogin(),
        'Documents',
        'Window-Dancer'
    )
    _config_name = 'config.toml'
    
    
    def _init(self) -> None:
        self.config_path = Path(self._config_path)
        self.config_dir = self.config_path.parent
        self.config_dir.mkdir(parents=True, exist_ok=True)
    

    def save_config(self):
        try:
            
            with open(self.config_path, "wb") as f:
                tomli_w.dump(self.config, f)
                
            return True
        
        except Exception as e:
            return False
    
    
    def load_config(self) -> any:
        if self.config_path.exists():
            
            try:
                
                with open(self.config_path, "rb") as file:
                    return tomli.load(file)
                
            except (tomli.TOMLDecodeError, FileNotFoundError) as e:
                return self.get_default_config()
            
        else:
            return self.get_default_config()
    
    
    def get_default_config(self):
        return {
            "window": {
                "width": 1024,
                "height": 768
            },
            "overlay": {
                "update_pos_delay_ms": 10
            },
            "startup": {
                "load": False,
                "path": ""
            }
        }
    
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        
        try:
            
            for k in keys:
                value = value[k]
                
            return value
        
        except (KeyError, TypeError):
            return default
    
    
    def set(self, key, value):
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            
            if k not in config:
                config[k] = {}
                
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ConfigSystem, cls).__new__(cls)
            
            
        return cls.__instance
import os
import tomllib

import tomli_w

from pathlib import Path

from scripts.constants import *


class ConfigSystem:
    __instance = None
    config = {}
    _config_path = os.path.join(
        'C:/Users', os.getlogin(), 'Documents/Window-Dancer/config.toml'
    )


    def save_config(self):
        try:
            
            with open(self.config_path, 'wb') as f:
                tomli_w.dump(self.config, f)
                pass
                
            return True
        
        except Exception as e:
            return False
    
    
    def load_config(self) -> None:
        if self.config_path.exists():
            try:
                
                with open(self.config_path, 'rb') as file:
                    self.config.update(tomllib.load(file))
                
            except (tomllib.TOMLDecodeError, FileNotFoundError) as e:
                self.config = self.get_default_config(self)
                self.save_config(self)
            
        else:
            self.config = self.get_default_config(self)
            self.save_config(self)
    
    
    def get_default_config(self):
        return {
            'window': {
                'width': 300,
                'height': 300
            },
            'overlay': {
                'update_delay': 10
            },
            'startup': {
                'path': ConfigDefaults.PATH,
                'scale': ConfigDefaults.SCALE,
                'animated_movement': ConfigDefaults.ANIMATED_MOVEMENT,
                'smooth': ConfigDefaults.SMOOTH
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
            if default is not None:
                self.set(key, default)
                
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
        
            cls.config_path = Path(cls._config_path)
            cls.config_dir = cls.config_path.parent
            print(f'Path: {cls.config_path}', f'Dir: {cls.config_dir}')
            cls.config_dir.mkdir(parents=True, exist_ok=True)
            
            cls.load_config(cls)
        
        return cls.__instance
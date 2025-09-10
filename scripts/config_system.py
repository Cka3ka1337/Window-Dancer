import os

import win32api


class ConfigSystem:
    __instance = None
    _config_path = os.path.join(
        win32api.GetSystemDirectory()[:2],
        'Users',
        os.getlogin(),
        'Documents'
    )
    _folder_name = 'Window-Dancer'
    _config_name = ''
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ConfigSystem, cls).__new__(cls)
            
        return cls.__instance
import win32api
import win32gui

from PySide6.QtCore import QSize, QPoint
from PySide6.QtWidgets import QApplication


def get_monitor_info(point: tuple) -> dict:
    try:
        monitor_handle = win32api.MonitorFromPoint(point)
        monitor_info = win32api.GetMonitorInfo(monitor_handle)
        return {
            'work': monitor_info['Work'],
            'monitor': monitor_info['Monitor']
        }
    except:
        return None
    

def get_target_position(overlay_size: QSize) -> tuple:
    cursor_pos = win32api.GetCursorPos()
    monitor_info = get_monitor_info(cursor_pos)
    
    if not monitor_info:
        primary_screen = QApplication.primaryScreen()
        screen_geometry = primary_screen.availableGeometry()
        return (
            screen_geometry.x() + screen_geometry.width() / 2 - overlay_size.width() / 2,
            screen_geometry.y() + screen_geometry.height() - overlay_size.height()
        )
    
    app = QApplication.instance()
    cursor_point = QPoint(*cursor_pos)
    
    for screen in app.screens():
        screen_geometry = screen.availableGeometry()
        if screen_geometry.contains(cursor_point):
            break
    else:
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
    
    default_pos = (
        screen_geometry.x() + screen_geometry.width() / 2 - overlay_size.width() / 2,
        screen_geometry.y() + screen_geometry.height() - overlay_size.height()
    )
    
    hWnd = win32gui.GetForegroundWindow()
    if win32gui.GetWindowText(hWnd):
        try:
            x1, y1, x2, y2 = win32gui.GetWindowRect(hWnd)
            
            window_top_left = QPoint(x1, y1)
            window_bottom_right = QPoint(x2, y2)
            
            window_screen = None
            for screen in app.screens():
                if screen.geometry().contains(window_top_left) or screen.geometry().contains(window_bottom_right):
                    window_screen = screen
                    break
                
            if window_screen:
                logical_x1 = window_screen.geometry().x() + (x1 - window_screen.geometry().x()) / window_screen.devicePixelRatio()
                logical_y1 = window_screen.geometry().y() + (y1 - window_screen.geometry().y()) / window_screen.devicePixelRatio()
                logical_x2 = window_screen.geometry().x() + (x2 - window_screen.geometry().x()) / window_screen.devicePixelRatio()
                logical_y2 = window_screen.geometry().y() + (y2 - window_screen.geometry().y()) / window_screen.devicePixelRatio()
                
                width = logical_x2 - logical_x1
                # height = logical_y2 - logical_y1
                
                window_pos = (
                    logical_x1 + width / 2 - overlay_size.width() / 2,
                    logical_y1 - overlay_size.height()
                )
                
                if (
                    win32api.MonitorFromPoint((
                        int(window_pos[0]),
                        int(window_pos[1]))) and # top left
                    win32api.MonitorFromPoint((
                        int(window_pos[0] + overlay_size.width()),
                        int( window_pos[1]))) and # top right
                    win32api.MonitorFromPoint((
                        int(window_pos[0] + overlay_size.width()),
                        int(window_pos[1] + overlay_size.height()))) and # bottom right
                    win32api.MonitorFromPoint((
                        int(window_pos[0]),
                        int(window_pos[1] + overlay_size.height()))) # bottom left
                ):
                    return window_pos
                    
        except Exception as e:
            print(f"Ошибка при обработке окна: {e}")
            pass
    
    return default_pos
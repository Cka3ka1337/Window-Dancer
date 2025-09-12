import win32api
import win32gui

from PySide6.QtCore import QSize


def get_monitor_info(point: tuple) -> tuple:
    point = tuple(map(int, point))
    
    # Validation with try-except block xD
    # If handled exception - overlay moved to central bottom monitor position
    try:
        monitor_info = win32api.GetMonitorInfo(
            win32api.MonitorFromPoint(point)
        )
    except:
        return None
    
    work_area = monitor_info['Work']
    
    # Calculating monitor rect
    monitor = (
        work_area[0],
        work_area[1],
        work_area[2] - work_area[0],
        work_area[3] - work_area[1]
    )
    
    return monitor


def get_target_position(overlay_size: QSize) -> tuple[int, int, int, int]:
    '''
    Returns the active window or
    monitor where the cursor is located.
    '''
    
    # initial variables
    cursor_pos = win32api.GetCursorPos()
    hWnd = win32gui.GetForegroundWindow()
    monitor_on_cursor = get_monitor_info(cursor_pos)

    # Overlay move on window
    if win32gui.GetWindowText(hWnd):
        # Calculating window size
        x1, y1, x2, y2 = win32gui.GetWindowRect(hWnd)
        width, height = x2 - x1, y2 - y1
        
        # Absolute overlay position on window
        move_pos = (
            x1 + width / 2 - overlay_size.width() / 2,
            y1 - overlay_size.height()
        )
                
        if (
            get_monitor_info((move_pos[0], 
                                move_pos[1])) and
            get_monitor_info((move_pos[0] + overlay_size.width(),
                                move_pos[1] + overlay_size.height()))
        ):
            return move_pos
    
    # Absolute overlay position on monitor
    mx, my, mw, mh = monitor_on_cursor
    move_pos = (
        mx + mw / 2 - overlay_size.width() / 2, 
        my + mh - overlay_size.height()
    )
    
    return move_pos
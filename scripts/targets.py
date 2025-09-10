import win32api
import win32gui


def get_target_window() -> tuple[tuple, str, str, int]:
    '''
    Returns the active window or
    monitor where the cursor is located.
    
    return: (rect, type, window text, hWnd)
    '''
    
    hWnd = win32gui.GetForegroundWindow()
    wname = win32gui.GetWindowText(hWnd)
    cursor_pos = win32api.GetCursorPos()
    
    if not hWnd:
        monitor_info = win32api.GetMonitorInfo(
            win32api.MonitorFromPoint(cursor_pos)
        )
        
        work_area = monitor_info['Work']
        width = work_area[2] - work_area[0]
        height = work_area[3] - work_area[1]
        
        return (*work_area[:2], width, height), 'cursor', wname, hWnd

    elif win32gui.GetWindowText(hWnd):
        x1, y1, x2, y2 = win32gui.GetWindowRect(hWnd)
        return (x1, y1, x2 - x1, y2 - y1), 'window', wname, hWnd
    else:
        rect = win32gui.GetWindowRect(hWnd)
        window_center_x = (rect[0] + rect[2]) // 2
        window_center_y = (rect[1] + rect[3]) // 2
        
        monitor_info = win32api.GetMonitorInfo(
            win32api.MonitorFromPoint((window_center_x, window_center_y))
        )
        
        work_area = monitor_info['Work']
        width = work_area[2] - work_area[0]
        height = work_area[3] - work_area[1]
        
        return (*work_area[:2], width, height), 'desktop', wname, hWnd
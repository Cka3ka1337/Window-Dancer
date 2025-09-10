def window_cursor(x, y, w, h, overlay) -> tuple:
    pos_x = int(x + w / 2 - overlay.width() / 2)
    pos_y = int(y - overlay.height())
    
    return pos_x, pos_y


def desktop(x, y, w, h, overlay) -> tuple:
    pos_x = int(x + w / 2 - overlay.width() / 2)
    pos_y = int(y + h - overlay.height())
    
    return pos_x, pos_y
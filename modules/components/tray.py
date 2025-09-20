from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon, QMenu


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon: str, parent):
        QSystemTrayIcon.__init__(self, QIcon(icon), parent)
        menu = QMenu(parent)
        
        
        hide_unhide = menu.addAction("Hide/Unhide")
        hide_unhide.triggered.connect(lambda e: (parent.show if parent.isHidden() else parent.hide)())
        
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(parent.close)
        
        self.setContextMenu(menu)
        self.setVisible(True)
        
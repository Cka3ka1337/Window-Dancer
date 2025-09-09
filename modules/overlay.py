from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QLabel, QWidget
)
from PySide6.QtCore import (
    Qt, QSize
)
from PySide6.QtGui import (
    QMovie, QPainter, QPaintEvent, QCloseEvent
)


class MainOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup window
        self.setWindowTitle('MainOverlay')
        # self.setGeometry(100, 100, 100, 100)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)# | Qt.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        
        # Init objects
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.movie = QMovie()
        self.movie.frameChanged.connect(self.update)
        self.label = QLabel() # Container for movie :/
        
        # addWidget`s or AddLayout`s
        # layout.addWidget(QLabel('This is MainOverlay'))
        layout.addWidget(self.label)

        # Margins
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Setting up the central widget and setting up the layout
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)
    
    
    def set_movie(self, path: str):
        self.movie.setFileName(path)
        self.movie.start()
    
    
    def set_scale(self, scale: float) -> None:
        frame_rect = self.movie.frameRect()
        
        size = QSize(
            int(frame_rect.width() * scale), 
            int(frame_rect.height() * scale)
        )
        
        self.movie.setScaledSize(size)
        self.setFixedSize(size)
    
    
    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        if self.movie.isValid():
            painter.drawPixmap(0, 0, self.movie.currentPixmap())
    
    
    def closeEvent(self, event: QCloseEvent) -> None:
        QApplication.instance().quit()
        super().closeEvent(event)
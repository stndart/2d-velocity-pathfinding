from PyQt5.QtWidgets import QMainWindow
from backend import Core

from .menubar import MyMenuBar
from .graphics import CarDisplay

import config

class MainWindow(QMainWindow):
    def __init__(self, core: Core):
        super().__init__()
        
        self.backend_core = core
        self.init_ui()
        
    def init_ui(self):
        self.setGeometry(*config.default_window_size)
        self.title = config.app_name
        
        self.menu = MyMenuBar(self)
        self.setMenuBar(self.menu)
        
        self.main_view = CarDisplay(self)
        self.setCentralWidget(self.main_view)
        
        self.show()
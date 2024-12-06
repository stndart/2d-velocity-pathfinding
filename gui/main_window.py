from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QCloseEvent
from backend import Core

import weakref
from threading import Thread, Lock, currentThread
from queue import Queue, Empty

import time

from .menubar import MyMenuBar
from .graphics import FieldDisplay
from backend import logger

import config

class MainWindow(QMainWindow):
    closed = pyqtSignal()
    
    def __init__(self, core: Core):
        super().__init__()
        
        self.backend_core = core
        self.init_ui()
        
        self.target_fps = 60
        
        self.thread = Thread(name='MainWindow::main_thread', target=MainWindow.main_thread, args=(weakref.proxy(self),))
        self.loop_active = True
        self.thread.daemon = True
        self.thread.start()
        
    def init_ui(self):
        self.setGeometry(*config.default_window_size)
        self.title = config.app_name
        
        self.menu = MyMenuBar(self)
        self.setMenuBar(self.menu)
        
        self.main_view = FieldDisplay(self, self.backend_core)
        self.setCentralWidget(self.main_view)
        
        self.show()
    
    def main_thread(self):
        self.timer = time.time()
        while self.loop_active:
            deltatime = time.time() - self.timer
            self.timer = time.time()
            
            self.backend_core.update(deltatime)
            self.main_view.update_frame(deltatime)
            
            desired_timeout = 1 / self.target_fps
            time.sleep(max(0, desired_timeout - deltatime))
    
    def closeEvent(self, event: QCloseEvent):
        logger.log("Close event caught")
        print('close!')
        
        self.loop_active = False
        self.thread.join()
        
        self.closed.emit()
        logger.save()
        
        event.accept()
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
        self.display_thread = Thread(name='MainWindow::display_thread', target=MainWindow.display_thread_fun, args=(weakref.proxy(self), self.target_fps))
        self.display_thread_active = True
        self.display_thread.daemon = True
        self.display_thread.start()

        self.target_phys_fps = 200
        self.physics_thread = Thread(name='MainWindow::physics_thread', target=MainWindow.physics_thread_fun, args=(weakref.proxy(self), self.target_phys_fps))
        self.physics_thread_active = True
        self.physics_thread.daemon = True
        self.physics_thread.start()
        
    def init_ui(self):
        self.setGeometry(*config.default_window_size)
        self.title = config.app_name
        
        self.menu = MyMenuBar(self)
        self.setMenuBar(self.menu)
        
        self.main_view = FieldDisplay(self, self.backend_core)
        self.setCentralWidget(self.main_view)
        
        self.show()
    
    def display_thread_fun(self, fps: float):
        timer = time.time()
        while self.display_thread_active:
            deltatime = time.time() - timer
            timer = time.time()
            
            self.main_view.update_frame(deltatime)
            
            desired_timeout = 1 / fps
            time.sleep(max(0, desired_timeout - deltatime))
    
    def physics_thread_fun(self, fps: float):
        timer = time.time()
        while self.physics_thread_active:
            deltatime = time.time() - timer
            timer = time.time()
            
            self.backend_core.update(deltatime)
            
            desired_timeout = 1 / fps
            time.sleep(max(0, desired_timeout - deltatime))
            
    
    def closeEvent(self, event: QCloseEvent):
        logger.log("Close event caught")
        
        self.physics_thread_active = False
        self.display_thread_active = False
        self.display_thread.join()
        self.physics_thread.join()
        
        self.closed.emit()
        logger.save()
        
        event.accept()
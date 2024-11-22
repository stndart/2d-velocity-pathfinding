import numpy as np
from math import ceil, floor

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import QPointF, QRectF

from PyQt5.QtCore import QTimer, pyqtSlot, Qt


import backend as bc
from .assets import assets
import config

class GridDisplay(QWidget):
    def __init__(self, parent: QWidget, ticksize: float = 1.0):
        super().__init__(parent)
        
        self.scene = QGraphicsScene(self)
        self.scene_rect = QRectF(-20., -15., 40., 30.)
        self.scene.setSceneRect(self.scene_rect)
        self.view = QGraphicsView(self.scene, self)
        self.view.scale(25, 25)
        self.registered_items = dict()
        
        pen2 = QPen(Qt.black, 0.02)
        pen2.setCapStyle(Qt.RoundCap)
        pen2.setJoinStyle(Qt.RoundJoin)
        
        pen1 = QPen(Qt.black, 0.06)
        pen1.setCapStyle(Qt.RoundCap)
        pen1.setJoinStyle(Qt.RoundJoin)
        
        pen0 = QPen(Qt.black, 0.15)
        pen0.setCapStyle(Qt.RoundCap)
        pen0.setJoinStyle(Qt.RoundJoin)
        
        self.line_pens = [pen0, pen1, pen2]
        
        self.init_grid(ticksize)
    
    @pyqtSlot()
    def init_grid(self, ticksize: float, majorticks: int = 5):
        left = ceil(self.scene_rect.left() / ticksize) * ticksize
        top = ceil(self.scene_rect.top() / ticksize) * ticksize
        right = floor(self.scene_rect.right() / ticksize) * ticksize
        bottom = floor(self.scene_rect.bottom() / ticksize) * ticksize
        
        i = left
        n = ceil(self.scene_rect.left() / ticksize)
        pen = lambda m: self.line_pens[0] if m == 0 else (self.line_pens[1] if m % majorticks == 0 else self.line_pens[2])
        while i < right:
            self.scene.addLine(i, top, i, bottom, pen=pen(n))
            i += ticksize
            n += 1
        
        i = top
        n = ceil(self.scene_rect.top() / ticksize)        
        while i < bottom:
            self.scene.addLine(left, i, right, i, pen=pen(n))
            i += ticksize
            n += 1
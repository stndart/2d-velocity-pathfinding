import numpy as np

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsItem

from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import QPointF

from PyQt5.QtCore import QTimer, pyqtSlot, Qt
from PyQt5.QtCore import QMetaObject
from PyQt5.Qt import Q_ARG

import backend as bc
from .assets import assets
from .grid_display import GridDisplay
import config

class FieldDisplay(GridDisplay):
    def __init__(self, parent: QWidget, core: bc.Core):
        super().__init__(parent)
        self.core = core
        
        self.registered_items: dict[[bc.Figure|bc.Agent], QGraphicsItem]= dict()

        self.pen = QPen(Qt.black, 0.06)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setJoinStyle(Qt.RoundJoin)
        self.brush = QBrush(Qt.red)
        self.brush2 = QBrush(Qt.green)
        
        self.update_items()
    
    @pyqtSlot()
    def update_items(self):
        for item in self.core.figures():
            if item not in self.registered_items:
                if isinstance(item, bc.Circle):
                    a, b = item.center.x - item.radius, -item.center.y + item.radius
                    c, d = 2 * item.radius, -2 * item.radius
                    self.registered_items[item] = self.scene.addEllipse(a, b, c, d, pen=self.pen, brush=self.brush)
                elif isinstance(item, (bc.Triangle, bc.Rectangle)):
                    self.registered_items[item] = self.scene.addPolygon(QPolygonF([QPointF(v.x, -v.y) for v in item.corners()]), pen=self.pen, brush=self.brush)
        
        for item in self.core.agents():
            if item not in self.registered_items:
                agent_poly = self.scene.addPolygon(QPolygonF([QPointF(p.x, p.y) for p in item.repr()]), pen=self.pen, brush=self.brush2)
                agent_poly.setPos(*item.coords())
                agent_poly.setVisible(True)
                agent_poly.setZValue(1)
                self.registered_items[item] = agent_poly
    
    @pyqtSlot(bc.Agent)
    def update_item_pos(self, agent: bc.Agent):
        npos = agent.coords()
        self.registered_items[agent].setPos(*npos)
    
    def update_frame(self, deltatime: float):
        for item in self.core.agents():
            QMetaObject.invokeMethod(self, 'update_item_pos', Qt.ConnectionType.QueuedConnection, Q_ARG(bc.Agent, item))
            
            
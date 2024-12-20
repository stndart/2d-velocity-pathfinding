import numpy as np
from typing import Optional
from math import degrees

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem

from PyQt5.QtGui import QPolygonF, QBrush, QPen, QPainter
from PyQt5.QtCore import QPointF, QRectF

from PyQt5.QtCore import QTimer, pyqtSlot, Qt
from PyQt5.QtCore import QMetaObject
from PyQt5.Qt import Q_ARG

import backend as bc
from .grid_display import GridDisplay
from .chain_graphics_item import RouteChain
from .fig_array_display import FigArrayItem

class FieldDisplay(GridDisplay):
    def __init__(self, parent: QWidget, core: bc.Core):
        super().__init__(parent)
        self.core = core
        
        self.registered_items: dict[[bc.Figure|bc.Agent], QGraphicsItem]= dict()

        self.pen = QPen(Qt.black, 0.06)
        self.pen.setCapStyle(Qt.RoundCap)
        self.pen.setJoinStyle(Qt.RoundJoin)

        self.pen2 = QPen(Qt.black, 0.05) # для рисования линий
        self.pen2.setCapStyle(Qt.RoundCap)
        self.pen2.setJoinStyle(Qt.RoundJoin)
        
        self.brush = QBrush(Qt.red)
        self.brush2 = QBrush(Qt.green)
        self.brush3 = QBrush(Qt.blue)
        
        self.update_items()
    
    @pyqtSlot()
    def update_items(self):
        for item in self.core.sprites():
            if item not in self.registered_items:
                mesh = item.mesh
                if isinstance(mesh, bc.Circle):
                    a, b = mesh.center.x - mesh.radius, -mesh.center.y + mesh.radius
                    c, d = 2 * mesh.radius, -2 * mesh.radius
                    self.registered_items[item] = self.scene.addEllipse(a, b, c, d, pen=self.pen, brush=self.brush)
                elif isinstance(mesh, (bc.Triangle, bc.Rectangle)):
                    self.registered_items[item] = self.scene.addPolygon(QPolygonF([QPointF(v.x, -v.y) for v in mesh.corners()]), pen=self.pen, brush=self.brush)
                elif isinstance(mesh, bc.Path):
                    titem = RouteChain(parent=self, path=mesh, pen=self.pen2, brush=self.brush3)
                    self.scene.addItem(titem)
                    titem.setZValue(10)
                    self.registered_items[item] = titem
                elif isinstance(mesh, bc.FigArray):
                    titem = FigArrayItem(parent=self, fig_array=mesh, pen=self.pen2, brush=self.brush)
                    self.scene.addItem(titem)
                    titem.setZValue(9)
                    self.registered_items[item] = titem
                else:
                    raise NotImplementedError(f"Can't draw {mesh.__class__.__name__}: unknown class")
        
        for item in self.core.agents():
            if item not in self.registered_items:
                sx, sy = item.pos().x, item.pos().y
                agent_poly = self.scene.addPolygon(QPolygonF([QPointF(p.x - sx, -p.y + sy) for p in item.repr()]), pen=self.pen, brush=self.brush2)
                agent_poly.setPos(QPointF(sx, -sy))
                agent_poly.setVisible(True)
                agent_poly.setZValue(1)
                self.registered_items[item] = agent_poly
    
    @pyqtSlot(bc.Agent)
    def update_item_pos(self, agent: bc.Agent):
        npos = agent.coords()
        nrot = -degrees(agent.direction)
        self.registered_items[agent].setPos(QPointF(npos[0], -npos[1]))
        self.registered_items[agent].setRotation(nrot)
    
    def update_frame(self, deltatime: float):
        for item in self.core.agents():
            QMetaObject.invokeMethod(self, 'update_item_pos', Qt.ConnectionType.QueuedConnection, Q_ARG(bc.Agent, item))
        
        for item, val in self.registered_items.items():
            if isinstance(item, bc.Path):
                val.update()
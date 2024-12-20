from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsItem, QAbstractGraphicsShapeItem

from PyQt5.QtGui import QPolygonF, QBrush, QPen, QPainter
from PyQt5.QtCore import QPointF, QRectF

from typing import Optional

from backend import FigArray
from backend.geometry import Point, Line

class FigArrayItem(QAbstractGraphicsShapeItem):
    def __init__(self, parent: QGraphicsScene, fig_array: FigArray = FigArray(), pen = QPen(), brush = QBrush(), pwidth: float = 0.1):
        super().__init__()
        
        self.fig_array = fig_array
        
        self.setPen(pen)
        self.setBrush(brush)
        
        self.pwidth = pwidth
        self.setPos(QPointF(0, 0))
    
    def update_path(self, new_fig_array: FigArray):
        self.fig_array = new_fig_array
    
    def boundingRect(self) -> QRectF:
        topLeft = None
        bottomRight = None
        for item in self.fig_array.elements:
            for p in item.vertexes():
                if topLeft is None:
                    topLeft = bottomRight = QPointF(p.x, p.y)
                if topLeft.x() < p.x:
                    topLeft = QPointF(p.x, topLeft.y())
                if topLeft.y() > p.y:
                    topLeft = QPointF(topLeft.x(), p.y)
                if bottomRight.x() > p.x:
                    bottomRight = QPointF(p.x, bottomRight.y())
                if bottomRight.y() < p.y:
                    bottomRight = QPointF(bottomRight.x(), p.y)
        
        #topLeft = QPointF(topLeft.x(), -topLeft.y())
        #bottomRight = QPointF(bottomRight.x(), -bottomRight.y())
        #return QRectF(topLeft, bottomRight) if topLeft is not None else QRectF()
        return QRectF() # bugs without it
    
    def paint(self, painter: QPainter, option: Optional[str] = None, widget: Optional[QWidget] = None):
        oldpen = painter.pen()
        oldbrush = painter.brush()
        
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        
        for item in self.fig_array.elements:
            if isinstance(item, Point):
                pass # for now
                painter.drawEllipse(QPointF(item.x, -item.y), self.pwidth, self.pwidth)
            elif isinstance(item, Line):
                p1, p2 = item.p1, item.p2
                painter.drawLine(QPointF(p1.x, -p1.y), QPointF(p2.x, -p2.y))
            else:
                raise NotImplementedError(f"FigArrayItem can't draw {item.__class__.__name__} yet")
        
        for item in self.fig_array.elements:
            if isinstance(item, Point):
                painter.drawEllipse(QPointF(item.x, -item.y), self.pwidth, self.pwidth)
        
        painter.setPen(oldpen)
        painter.setBrush(oldbrush)
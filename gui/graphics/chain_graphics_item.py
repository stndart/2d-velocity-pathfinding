from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsItem, QAbstractGraphicsShapeItem

from PyQt5.QtGui import QPolygonF, QBrush, QPen, QPainter
from PyQt5.QtCore import QPointF, QRectF

from typing import Optional

from backend import Path

class RouteChain(QAbstractGraphicsShapeItem):
    def __init__(self, parent: QGraphicsScene, path: Path = Path(), pen = QPen(), brush = QBrush(), pwidth: float = 0.2):
        super().__init__()
        
        self.path = path
        
        self.setPen(pen)
        self.setBrush(brush)
        
        self.pwidth = pwidth
        self.setPos(QPointF(0, 0))
    
    def boundingRect(self) -> QRectF:
        topLeft = None
        bottomRight = None
        for p in self.path.points():
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
        
        return QRectF(topLeft, bottomRight) if topLeft is not None else QRectF()
    
    def paint(self, painter: QPainter, option: Optional[str] = None, widget: Optional[QWidget] = None):
        print('paint')
        oldpen = painter.pen()
        oldbrush = painter.brush()
        
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        for p1, p2 in self.path.segments():
            painter.drawLine(p1.x, -p1.y, p2.x, -p2.y)
        for p in self.path.points():
            painter.drawEllipse(QPointF(p.x, -p.y), self.pwidth, self.pwidth)
        
        painter.setPen(oldpen)
        painter.setBrush(oldbrush)
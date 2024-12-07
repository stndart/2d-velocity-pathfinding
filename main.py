import sys
from time import sleep, time
from math import radians, degrees

from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from backend import Core, logger

from backend import SimpleCar, RoutingCar
from backend import Circle, Triangle, Point, Path
from backend import make_sprite, Sprite

from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import QPointF

def main(core: Core):
    app = QApplication(sys.argv)
    window = MainWindow(core)
    
    logger.log("App running")
    sys.exit(app.exec_())

if __name__ == '__main__':
    back = Core()

    route = Path([
        Point(-1, 1),
        Point(2, 0),
        Point(3, 6)
    ])    
    circ = make_sprite(Circle(4, 6, 2))
    tria = make_sprite(Triangle(
        Point(1, 5),
        Point(2, 1),
        Point(4, 3)
    ))
    
    back.add_sprite(circ)
    back.add_sprite(tria)
    back.add_sprite(Sprite(route, None))
    
    car = RoutingCar(route, turnspeed=0.8, maxspeed=2)
    #car = SimpleCar(Point(-1, 3))
    car.rotate(radians(90))
    
    back.add_agent(car)
    
    main(back)
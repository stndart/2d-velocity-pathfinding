import sys
from time import sleep, time
from math import radians, degrees

from PyQt5.QtWidgets import QApplication

from gui import MainWindow
from backend import Core, logger

from backend import SimpleCar, RoutingCar
from backend import Circle, Triangle, Point, Path

from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import QPointF

def main(core: Core):
    app = QApplication(sys.argv)
    window = MainWindow(core)
    
    logger.log("App running")
    sys.exit(app.exec_())

if __name__ == '__main__':
    back = Core()
    back.add_figure(Circle(4, 6, 2))
    back.add_figure(Triangle(
        Point(1, 5),
        Point(2, 1),
        Point(4, 3)
    ))
    route = Path(
        [Point(-1, 1),
         Point(2, 0),
         Point(3, 4)]
    )
    back.add_figure(route)
    
    car = RoutingCar(route)
    #car = SimpleCar(-1, 3)
    #car.direction = radians(10)
    #car.speed = 1
    
    back.add_agent(car)
    
    main(back)
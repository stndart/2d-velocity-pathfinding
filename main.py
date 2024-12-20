import sys
from time import sleep, time
from math import radians, degrees

from PyQt5.QtWidgets import QApplication

from PyQt5.QtGui import QPolygonF, QBrush, QPen
from PyQt5.QtCore import QPointF

from gui import MainWindow
from backend import Core, logger, SpriteGenerator

from backend import SimpleCar, RoutingCar
from backend import Circle, Triangle, Point, Path, Rectangle
from backend.geometry import Line
from backend import make_sprite, Sprite, GraphSprite
from backend import build_graph_on_quadtree, VertMode

def main(core: Core):
    app = QApplication(sys.argv)
    window = MainWindow(core)
    
    logger.log("App running")
    sys.exit(app.exec_())

if __name__ == '__main__':
    back = Core()
    
    GEN = False
    if not GEN:
        gen_n = 0
        if gen_n == 0:
            circ = make_sprite(Circle(3, 6.5, 1.2))
            tria = make_sprite(Triangle(
                Point(1, 4.9),
                Point(2, 1),
                Point(3.4, 3)
            ))
            c2 = make_sprite(Circle(1.5, 0.8, 0.5))
            
            back.add_sprite(circ)
            back.add_sprite(tria)
            back.add_sprite(c2)
        elif gen_n == 1:
            c1 = make_sprite(Circle(3.725, 4.118, 0.735))
            c2 = make_sprite(Circle(8.014, 4.526, 1.314))
            t1 = make_sprite(Triangle(Point(4.766, 5.924), Point(7.126, 4.912), Point(6.125, 4.160)))
            t2 = make_sprite(Triangle(Point(10.438, 6.877), Point(13.989, 6.716), Point(12.781, 9.415)))
            
            back.add_sprite(c1)
            back.add_sprite(c2)
            back.add_sprite(t1)
            back.add_sprite(t2)
        elif gen_n == 2:
            t1 = make_sprite(Triangle(Point(2.109, 8.794), Point(0.897, 9.259), Point(-0.915, 10.678)))
            back.add_sprite(t1)
    else:
        #sprites = SpriteGenerator(Rectangle(Point(-10, -15), Point(30, 15)), av_size=5).generate_sprites(5)
        sprites = SpriteGenerator(Rectangle(Point(0, 0), Point(15, 10)), av_size=5).generate_sprites(3)
        for s in sprites:
            back.add_sprite(s)
            print(s.mesh)
    
    route = Path([
        Point(-1, 1),
        Point(2, 0),
        Point(3, 6), 
        Point(6, 3), 
        Point(1, -2)
    ])
    #back.add_sprite(Sprite(route, None))
    
    car = RoutingCar(route, turnspeed=1.8, maxspeed=2)
    #car = SimpleCar(Point(-1, 1))
    #car.speed = 1
    
    car.rotate(radians(-20))
    #back.add_agent(car)
    
    print(back.quadtree.print_tree(), '\n', '-'*30, '\n'*2)
    #line = Line(Point(2.500, 2.500), Point(5.000, 5.000))
    #print(back.quadtree.get_collision_candidates(make_sprite(line)))
    
    G = build_graph_on_quadtree(back.quadtree, mode=VertMode.ALL)
    GS = GraphSprite(G)
    back.add_sprite(GS)
    
    main(back)
from math import radians

from backend import Core
from backend import SimpleCar, RoutingCar
from backend import Circle, Triangle, Point, Path, Rectangle
from backend.geometry import Line
from backend import make_sprite, Sprite, GraphSprite
from backend import build_graph_on_quadtree, VertMode
from backend import SpriteGenerator
from backend.pathfinding import QuadPathfinder

def generate_launch(back: Core, launch_configuration: int = 0, generate: bool = False, gen_configuration: int = 0) -> None:
    if not generate:
        if gen_configuration == 0:
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
        
        elif gen_configuration == 1:
            c1 = make_sprite(Circle(3.725, 4.118, 0.735))
            c2 = make_sprite(Circle(8.014, 4.526, 1.314))
            t1 = make_sprite(Triangle(Point(4.766, 5.924), Point(7.126, 4.912), Point(6.125, 4.160)))
            t2 = make_sprite(Triangle(Point(10.438, 6.877), Point(13.989, 6.716), Point(12.781, 9.415)))
            
            back.add_sprite(c1)
            back.add_sprite(c2)
            back.add_sprite(t1)
            back.add_sprite(t2)
        
        elif gen_configuration == 2:
            t1 = make_sprite(Triangle(Point(2.109, 8.794), Point(0.897, 9.259), Point(-0.915, 10.678)))
            back.add_sprite(t1)
        
        elif gen_configuration == 3:
            tria = make_sprite(Triangle(
                Point(1, 4.9),
                Point(2, 1),
                Point(3.4, 3)
            ))
            back.add_sprite(tria)
    else:
        if gen_configuration == 0:
            sprites = SpriteGenerator(Rectangle(Point(-10, -15), Point(30, 15)), av_size=5).generate_sprites(5)
        elif gen_configuration == 1:
            sprites = SpriteGenerator(Rectangle(Point(0, 0), Point(15, 10)), av_size=5).generate_sprites(3)
        else:
            sprites = SpriteGenerator(Rectangle(Point(0, 0), Point(1, 1)), av_size=1).generate_sprites(0)
        
        for s in sprites:
            back.add_sprite(s)
            print(s.mesh)
    
    if launch_configuration == 0:
        car = SimpleCar(Point(-1, 1))
        car.speed = 1
        car.rotate(radians(-20))

        back.add_agent(car)
    
    elif launch_configuration == 1:
        route = Path([
            Point(-1, 1),
            Point(2, 0),
            Point(3, 6), 
            Point(6, 3), 
            Point(1, -2)
        ])
        back.add_sprite(Sprite(route, None))
        
        car = RoutingCar(route, turnspeed=1.8, maxspeed=2)
        car.speed = 1
        
        car.rotate(radians(-20))
        back.add_agent(car)
    
    elif launch_configuration == 2:
        print(back.quadtree.print_tree(), '\n', '-'*30, '\n'*2)
        
        G = build_graph_on_quadtree(back.quadtree, mode=VertMode.ALL)
        GS = GraphSprite(G)
        back.add_sprite(GS)
    
    elif launch_configuration == 3:
        G = build_graph_on_quadtree(back.quadtree, mode=VertMode.ALL)
        GS = GraphSprite(G)
        back.add_sprite(GS)

        start, dest = Point(-1, 1), Point(5, 7)
        pathfinder = QuadPathfinder(back.quadtree)
        path = [start] + pathfinder.find_path(start, dest) + [dest]
        #path = [start, dest]
        print('path', path)
        back.add_sprite(Sprite(Path(path), None))
from time import time
from math import radians

from backend import Core
from backend import SimpleCar, RoutingCar
from backend import Circle, Triangle, Point, Path, Rectangle
from backend.geometry import Line
from backend import make_sprite, Sprite, GraphSprite
from backend import build_graph_on_quadtree, VertMode
from backend import SpriteGenerator
from backend.pathfinding import QuadPathfinder

def generate_sprites(back: Core, gen_configuration: int = 0) -> None:
    if gen_configuration == 0:
        sprites = SpriteGenerator(Rectangle(Point(-10, -15), Point(30, 15)), av_size=5).generate_sprites(5)
    elif gen_configuration == 1:
        sprites = SpriteGenerator(Rectangle(Point(0, 0), Point(15, 10)), avg_size=5).generate_sprites(3)
    else:
        sprites = SpriteGenerator(Rectangle(Point(0, 0), Point(15, 10)), avg_size=2, types = [Triangle]).generate_sprites(gen_configuration)
    
    for s in sprites:
        back.add_sprite(s)
        print(s.mesh)

def pregenerated_sprites(back: Core, gen_configuration: int = 0) -> None:
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
    
    elif gen_configuration == 4:
        tri2 = make_sprite(Triangle(
            Point(2.2, 7),
            Point(4, 6.5),
            Point(3, 5.3)
        ))
        tria = make_sprite(Triangle(
            Point(1, 4.9),
            Point(2, 1),
            Point(3.4, 3)
        ))
        #c2 = make_sprite(Circle(1.5, 0.8, 0.5))
        
        back.add_sprite(tri2)
        back.add_sprite(tria)
        #back.add_sprite(c2)
    
    elif gen_configuration == 5:
        # Triangle: [<13.820, 4.935>, <8.555, 4.226>, <10.510, 0.439>]
        # Triangle: [<13.247, 11.229>, <8.144, 11.560>, <6.682, 9.886>]

        t1 = make_sprite(Triangle(
            Point(13.820, 4.935),
            Point(8.555, 4.226),
            Point(10.510, 0.439)
        ))
        t2 = make_sprite(Triangle(
            Point(13.247, 11.229),
            Point(8.144, 11.560),
            Point(6.682, 9.886)
        ))

        back.add_sprite(t1)
        back.add_sprite(t2)
    

def generate_launch(back: Core, launch_configuration: int = 0, generate: bool = False, gen_configuration: int = 0,
                    pathfinder_algorithm: str = None) -> None:
    if not generate:
        pregenerated_sprites(back, gen_configuration)
    else:
        generate_sprites(back, gen_configuration)
    
    # simple car, rotated -20 degrees
    if launch_configuration == 0:
        car = SimpleCar(Point(-1, 1))
        car.speed = 1
        car.rotate(radians(-20))

        back.add_agent(car)
    # routing car, routing a sample route with constant speed
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
    # build a graph on the quadtree and display the graph
    elif launch_configuration == 2:
        print(back.quadtree.print_tree(), '\n', '-'*30, '\n'*2)
        
        G = build_graph_on_quadtree(back.quadtree, mode=VertMode.ALL)
        GS = GraphSprite(G)
        back.add_sprite(GS)
    # find a path from start to dest using the quadtree dijkstra pathfinder, also displays the graph
    elif launch_configuration == 3:
        start, dest = Point(-1, 0), Point(16, 11)
        if not pathfinder_algorithm:
            pathfinder_algorithm = 'dijkstra'
        back.pathfinder = QuadPathfinder(back.quadtree, algorithm=pathfinder_algorithm)
        
        ts = time()
        path = [start] + back.pathfinder.find_path(start, dest) + [dest]
        print(f"Searching path took {time() - ts: .2f}s")
        #print('path', path)
        back.add_sprite(Sprite(Path(path), None))
        
        gs = GraphSprite(back.pathfinder.graph.graph)
        back.add_sprite(gs)
    # find a path from start to dest using the quadtree dijkstra pathfinder
    elif launch_configuration == 4:
        start, dest = Point(-1, 0), Point(16, 11)
        if not pathfinder_algorithm:
            pathfinder_algorithm = 'dijkstra'
        back.pathfinder = QuadPathfinder(back.quadtree, algorithm=pathfinder_algorithm)
        
        ts = time()
        path = [start] + back.pathfinder.find_path(start, dest) + [dest]
        print(f"Searching path took {time() - ts: .2f}s")
        #print('path', path)
        back.add_sprite(Sprite(Path(path), None))
        
    elif launch_configuration == 5:
        start, dest = Point(-1, 0), Point(16, 11)
        if not pathfinder_algorithm:
            pathfinder_algorithm = 'dijkstra'
        
        
        ts = time()
        graph, vertex_dict = build_graph_on_quadtree(back.quadtree, mode=VertMode.ALL, return_vertex_dict=True)
        print(f'Building quadtree graph of {len(graph.vertexes)} vertices took {time() - ts: .2f}s')
        
        p1 = QuadPathfinder(back.quadtree, algorithm='Theta*', graph=graph, vertex_dict=vertex_dict)
        p2 = QuadPathfinder(back.quadtree, algorithm='A*', graph=graph, vertex_dict=vertex_dict)
        
        print(f"\n========   {pathfinder_algorithm}   ========")
        ts = time()
        path = [start] + p1.find_path(start, dest) + [dest]
        print(f"Searching path took {time() - ts: .2f}s for {pathfinder_algorithm}")
        print('path', path)
        back.add_sprite(Sprite(Path(path), None))
        
        print(f"\n========   A*   ========")
        ts = time()
        path = [start] + p2.find_path(start, dest) + [dest]
        print(f"Searching path took {time() - ts: .2f}s for A*")
        print('path', path)
        back.add_sprite(Sprite(Path(path), None))
        
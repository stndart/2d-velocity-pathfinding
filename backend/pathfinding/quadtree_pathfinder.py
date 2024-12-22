from .pathfinder import Dijkstra, Floyd
from .graph import Graph
from .quadtree import QuadTree
from .buildgraph import build_graph_on_quadtree, check_collisions, build_vertexes_from_rect
from .buildgraph import Waypoint as Vertex

from backend.geometry import Point, Line
from backend.sprites import make_sprite

from .graph import GraphEdge as Edge
from .buildgraph import VertMode

class QuadPathfinder(Dijkstra):
    def __init__(self, quadtree: QuadTree):
        self.quadtree = quadtree
        self.vertex_dict: dict[QuadTree, list[Vertex]]
        graph, self.vertex_dict = build_graph_on_quadtree(quadtree, mode=VertMode.ALL, return_vertex_dict=True)
        
        super().__init__(graph)
    
    def find_path_length(self, path: list[Vertex], start_v: Vertex, goal_v: Vertex) -> float:
        path_len = 0
        for i in range(len(path) - 1):
            path_len += path[i].coords.distance_to(path[i + 1].coords)
        path_len += path[-1].coords.distance_to(goal_v.coords)
        path_len += start_v.coords.distance_to(path[0].coords)
        return path_len

    def find_path(self, start: Point, goal: Point) -> list[Point]:
        # Implement the pathfinding logic using the quadtree
        
        if check_collisions(self.quadtree, start) or check_collisions(self.quadtree, goal):
            #print('start or goal inside an obstacle')
            return [] # either start or goal is inside an obstacle

        start_quad = self.quadtree.get_quad_tree(make_sprite(start))
        start_vertices: list[Vertex] = []
        for q in start_quad.dfs():
            for v in self.vertex_dict[q]:
                if not check_collisions(self.quadtree, Line(start, v.coords)):
                    start_vertices.append(v)

        end_quad = self.quadtree.get_quad_tree(make_sprite(goal))
        end_vertices: list[Vertex] = []
        for q in end_quad.dfs():
            for v in self.vertex_dict[q]:
                if not check_collisions(self.quadtree, Line(goal, v.coords)):
                    end_vertices.append(v)
        
        if not start_vertices or not end_vertices:
            #print('no adjacent vertices found')
            return [] # no adjacent vertices to start or goal found
        
        # Now we have to find the shortest path between start and goal vertices
        # using the Dijkstra algorithm

        #print("Start vertices:")
        #for v in start_vertices:
            #print(v)
        #print("End vertices:")
        #for v in end_vertices:
            #print(v)
        
        myv = None
        for v in start_vertices:
            if v.coords == Point(1, 4.9):
                myv = v
                break
        if myv:
            for q in self.vertex_dict:
                if myv in self.vertex_dict[q]:
                    print('q is', q)
            for e, cost in myv.edges.items():
                print(e, cost)
            print()

        shortest_path = []
        shortest_path_len = float('inf')
        for start_v in start_vertices:
            for end_v in end_vertices:
                path: list[Vertex] = super().find_path(start_v, end_v)
                new_path_len = self.find_path_length(path, Vertex(start), Vertex(goal)) if path else float('inf')
                if start_v.coords == Point(0, 6.25) and end_v.coords == Point(2.2, 7):
                    print("?", shortest_path_len, new_path_len)
                if new_path_len < shortest_path_len:
                    shortest_path = path
                    shortest_path_len = new_path_len
        
        print('shortest path length:', shortest_path_len)
        print("shortest path:", shortest_path)
        return [vert.coords for vert in shortest_path]

# class QuadPathfinderFloyd(Floyd):

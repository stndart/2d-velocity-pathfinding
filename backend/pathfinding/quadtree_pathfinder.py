from time import time
from typing import Optional

from .graph import Graph
from .quadtree import QuadTree
from .buildgraph import build_graph_on_quadtree, check_collisions, build_vertexes_from_rect
from .buildgraph import Waypoint as Vertex

from .pathfinder import Dijkstra, Floyd, Pathfinder
from .astar_pathfinder import AStar
from .thetastar_pathfinder import ThetaStar

from backend.geometry import Point, Line
from backend.sprites import make_sprite
from .graph import GraphEdge as Edge
from .buildgraph import VertMode

class QuadPathfinder:
    def __init__(self, quadtree: QuadTree, algorithm: str = 'dijkstra',
                 graph: Optional[Graph] = None, vertex_dict: Optional[dict[QuadTree, list[Vertex]]] = None):
        """_summary_

        Args:
            quadtree (QuadTree): _description_
            algorithm (str, optional): _description_. Defaults to 'dijkstra'.
            graph, vertex_dict: if given, will skip build_graph_on_quadte
        
        algorhitm:
            'dijkstra' - Dijkstra's algorithm
            'floyd' - Floyd-Warshall algorithm, with preprocessed paths
            'A*' - A* algorithm (not implemented)
            'Theta*' - Theta* algorithm, an A* improvement (not implemented)
        """

        self.quadtree = quadtree
        self.vertex_dict: dict[QuadTree, list[Vertex]]

        if not graph or not vertex_dict:
            ts = time()
            graph, vertex_dict = build_graph_on_quadtree(quadtree, mode=VertMode.ALL, return_vertex_dict=True)
            print(f'Building quadtree graph of {len(graph.vertexes)} vertices took {time() - ts: .2f}s')
        self.vertex_dict = vertex_dict

        self.graph: Pathfinder
        if algorithm == 'dijkstra':
            self.graph = Dijkstra(graph)
        elif algorithm == 'floyd':
            self.graph = Floyd(graph)
        elif algorithm == 'A*':
            self.graph = AStar(graph)
        elif algorithm == 'Theta*':
            self.graph = ThetaStar(graph, self.quadtree)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}\nAvailable algorithms are ['dijkstra', 'floyd', 'A*', 'Theta*']")
    
    def find_path_length(self, path: list[Vertex], start_v: Vertex, goal_v: Vertex) -> float:
        """
        Calculates the length of the path from start to goal vertices
        """

        path_len = 0
        if not path:
            path_len = float('inf')
        
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
        
        # print(f'approx is {len(start_vertices)}x{len(end_vertices)}={len(start_vertices) * len(end_vertices)}')

        # temporarily adding the start and goal vertices to the graph
        start_v = Vertex(start)
        goal_v = Vertex(goal)
        self.graph.graph.add_vertex(start_v)
        self.graph.graph.add_vertex(goal_v)

        for sv in start_vertices:
            self.graph.graph.add_edge(Edge(start_v, sv, start_v.coords.distance_to(sv.coords)))
        for ev in end_vertices:
            self.graph.graph.add_edge(Edge(ev, goal_v, goal_v.coords.distance_to(ev.coords)))
        
        self.graph.update_shortest_paths(start_v)
        self.graph.update_shortest_paths(goal_v)

        shortest_path = self.graph.find_path(start_v, goal_v)
        shortest_path_len = self.find_path_length(shortest_path, start_v, goal_v)

        # removing the start and goal vertices from the graph
        self.graph.graph.remove_vertex(start_v)
        self.graph.graph.remove_vertex(goal_v)
        # updating the shortest paths again
        self.graph.preprocess_paths()
        
        print('shortest path length:', shortest_path_len)
        print("shortest path:", shortest_path)
        return [vert.coords for vert in shortest_path]

# class QuadPathfinderFloyd(Floyd):

from .pathfinder import Pathfinder
from .graph import Graph
from .quadtree import QuadTree
from .buildgraph import Waypoint as Vertex, check_collisions
from backend.geometry import Point, Line
from backend.algo import PriorityQueue

class ThetaStar(Pathfinder):
    def __init__(self, g: Graph, quadtree: QuadTree):
        super().__init__(g)
        self.quadtree = quadtree
    
    def heuristic(self, end: Vertex):
        """
        Euristic distance from start to end
        Simple decart distance
        """
        return self.start.distance(end)

    def find_path(self, start: Vertex, end: Vertex) -> list[Vertex]:
        """
        Finds path from start to end using Theta* algorithm
        """
        self.start = start

        self.g_score: dict[Vertex, float] = {vertex: float('inf') for vertex in self.graph.vertexes}
        self.g_score[start] = 0
        self.f_score: dict[Vertex, float] = {vertex: float('inf') for vertex in self.graph.vertexes}
        self.f_score[start] = self.g_score[start] + self.heuristic(end)

        self.came_from: dict[Vertex, Vertex] = {}
        self.came_from[start] = start
        
        self.open_set: PriorityQueue[Vertex] = PriorityQueue()
        self.open_set.insert(start, self.f_score[start])
        self.closed_set: set[Vertex] = set()

        while self.open_set:
            current = self.open_set.extract_minimum()

            if current == end:
                return self.reconstruct_path(current)
            self.closed_set.add(current)

            for edge in current.edges:
                neighbor = edge.other(current)

                if neighbor not in self.closed_set:
                    if neighbor not in self.open_set:
                        # Initialize values of neighbor if it is
                        # Not already in the open set
                        self.g_score[neighbor] = float('inf')
                        self.came_from[neighbor] = None
                    self.update_vertex(current, neighbor)

        return []

    def update_vertex(self, current: Vertex, neighbor: Vertex) -> None:
        # This part of the algorithm is the main difference between A* and Theta*
        parent = self.came_from[current]
        s = current
        if self.line_of_sight(parent, neighbor):
            # If there is line-of-sight between parent(s) and neighbor
            # then ignore s and use the path from parent(s) to neighbor
            s = parent
        
        # If the length of the path from start to s and from s to 
        # neighbor is shorter than the shortest currently known distance
        # from start to neighbor, then update node with the new distance
        
        cost = s.distance(neighbor)
        if self.g_score[s] + cost < self.g_score[neighbor]:
            self.g_score[neighbor] = self.g_score[s] + cost
            self.came_from[neighbor] = s
            
            self.open_set.discard(neighbor)
            self.open_set.insert(neighbor, self.g_score[neighbor] + self.heuristic(neighbor))

    def line_of_sight(self, start: Vertex, end: Vertex):
        return not check_collisions(self.quadtree, Line(start.coords, end.coords))

    def reconstruct_path(self, current: Vertex) -> list[Vertex]:
        print('reconstructing...')
        path = [current]
        while current in self.came_from:
            if current == self.came_from[current]:
                break
            current = self.came_from[current]
            path.append(current)
        path.reverse()
        return path
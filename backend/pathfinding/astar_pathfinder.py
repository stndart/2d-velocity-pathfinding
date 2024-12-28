import heapq

from .pathfinder import Pathfinder
from .graph import Graph
from .buildgraph import Waypoint as Vertex

class AStar(Pathfinder):
    def __init__(self, g: Graph):
        super().__init__(g)
    
    def euristic(self, start: Vertex, end: Vertex):
        """
        Euristic distance from start to end
        Simple decart distance
        """
        return start.distance(end)

    def find_path(self, start: Vertex, end: Vertex) -> list[Vertex]:
        """
        Finds path from start to end using A* algorithm
        """

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from: dict[Vertex, Vertex] = {}
        g_score: dict[Vertex, float] = {vertex: float('inf') for vertex in self.graph.vertexes}
        g_score[start] = 0
        f_score: dict[Vertex, float] = {vertex: float('inf') for vertex in self.graph.vertexes}
        f_score[start] = self.euristic(start, end)

        while open_set:
            current: Vertex = heapq.heappop(open_set)[1]

            if current == end:
                return self.reconstruct_path(came_from, current)

            for edge in current.edges:
                neighbor = edge.other(current)
                tentative_g_score = g_score[current] + edge.cost

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.euristic(neighbor, end)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def reconstruct_path(self, came_from: dict[Vertex, Vertex], current: Vertex) -> list[Vertex]:
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path
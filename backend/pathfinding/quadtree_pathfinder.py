from .pathfinder import Dijkstra, Floyd
from .graph import Graph
from .quadtree import QuadTree
from .buildgraph import build_graph_on_quadtree, check_collisions, build_vertexes_from_rect
from .buildgraph import Waypoint as Vertex

from backend.geometry import Point, Line
from backend.sprites import make_sprite


class QuadPathfinder(Dijkstra):
    def __init__(self, quadtree: QuadTree):
        self.quadtree = quadtree
        graph, self.vertex_dict = build_graph_on_quadtree(quadtree, return_vertex_dict=True)
        
        super().__init__(graph)

    def find_path(self, start: Point, goal: Point):
        # Implement the pathfinding logic using the quadtree
        
        if check_collisions(self.quadtree, start) or check_collisions(self.quadtree, goal):
            return [] # either start or goal is inside an obstacle
        
        start_node = Vertex(start)
        goal_node = Vertex(goal)

        start_quad = self.quadtree.get_quad_tree(make_sprite(start))
        start_vertices = []
        for q in start_quad.dfs():
            for v in self.vertex_dict[q]:
                if not check_collisions(self.quadtree, make_sprite(Line(start, v.coords))):
                    start_vertices.append(v)

        end_quad = self.quadtree.get_quad_tree(make_sprite(goal))
        end_vertices = []
        for q in end_quad.dfs():
            for v in self.vertex_dict[q]:
                if not check_collisions(self.quadtree, make_sprite(Line(goal, v.coords))):
                    end_vertices.append(v)
        
        if not start_vertices or not end_vertices:
            return [] # no adjacent vertices to start or goal found
        
        # Now we have to find the shortest path between start and goal vertices
        # using the Dijkstra algorithm

        shortest_path = []
        for start_v in start_vertices:
            for end_v in end_vertices:
                path = super().find_path(start_v, end_v)
                if not shortest_path or len(path) < len(shortest_path):
                    shortest_path = path
        return shortest_path

# class QuadPathfinderFloyd(Floyd):

from enum import Enum
from itertools import combinations

from .graph import Graph
from .graph import GraphVertex as Vertex
from .quadtree import QuadTree

from backend.geometry import Rectangle, Point, Line
from backend.sprites import make_sprite

class VertMode(Enum):
    CENTER = 0
    CORNERS = 1
    EDGES = 2
    BOTH = 3
    ALL = 4

def build_vertexes_from_rect(rect: Rectangle, mode: VertMode = VertMode.CORNERS):
    res: list[Point] = []
    if mode in (VertMode.CENTER, VertMode.ALL):
        res += [(rect.bottom_left + rect.top_right) / 2]
    if mode in (VertMode.EDGES, VertMode.BOTH, VertMode.ALL):
        res += [(e.p1 + e.p2) / 2 for e in rect.edges()]
    if mode in (VertMode.CORNERS, VertMode.BOTH, VertMode.ALL):
        res += [v for v in rect.vertexes()]
    return res
    
class Waypoint(Vertex):
    def __init__(self, coords: Point):
        super().__init__()
        self.coords = coords
    
    def __hash__(self):
        return self.coords.x.__hash__() + self.coords.y.__hash__()
    
    def __eq__(self, other: 'Waypoint') -> bool:
        if not isinstance(other, Waypoint):
            return False
        return self.coords == other.coords
    
    def distance(self, other: 'Waypoint'):
        return abs(other.coords - self.coords)
    
    def __repr__(self):
        return self.coords.__repr__()

# returns True if p collides with anything in qtree
def check_collisions(qtree: QuadTree, p: Point|Line) -> bool:
    ts = make_sprite(p)  # Eeh, but ok
    for s in qtree.get_collision_candidates(ts):
        if ts.collision_shape.has_intersect(s.collision_shape):
            return True
    return False

def build_graph_on_quadtree(qtree: QuadTree, mode: VertMode = VertMode.CORNERS, return_vertex_dict: bool = False, quality=10) -> Graph:
    vertex_dict: dict[QuadTree, list[Waypoint]] = dict()
    for q in qtree.dfs():
        vertex_dict[q] = []
        wps: list[Waypoint] = []
        for p in build_vertexes_from_rect(q.rectangle, mode=mode):
            if not check_collisions(qtree, p):
                wps.append(Waypoint(p))
        vertex_dict[q] += wps
    
    for q in qtree.dfs():
        for fig in q.sprites:
            vs = fig.collision_shape.vertexes(quality=quality)
            for p in vs:
                q2 = qtree.get_quad_tree(make_sprite(p))
                wp = Waypoint(p)
                if wp not in vertex_dict[q2]:
                    vertex_dict[q2].append(Waypoint(p))

    sp = list(q.sprites)[0] if q.sprites else None
    cr = sp.collision_shape if sp else None
    
    G = Graph()
    for q in vertex_dict:
        vs = vertex_dict[q]
        #print(len(vs))
        # temp
        for v in vs:
            G.add_vertex(v)
        x = 1
        
        for v1, v2 in combinations(vs, 2):
            v1: Waypoint
            v2: Waypoint
            if not check_collisions(qtree, Line(v1.coords, v2.coords)):
                G.add_edge(v1, v2, cost=v1.distance(v2))
    
    return G if not return_vertex_dict else (G, vertex_dict)
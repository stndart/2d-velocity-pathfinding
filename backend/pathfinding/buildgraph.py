from enum import Enum
from itertools import chain, combinations
from typing import Iterable, TypeVar, Optional

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

def check_collisions(qtree: QuadTree, p: Point|Line) -> bool:
    """
    returns True if p collides with anything in qtree
    """
    ts = make_sprite(p)  # Eeh, but ok
    for s in qtree.get_collision_candidates(ts):
        if ts.collision_shape.has_intersect(s.collision_shape):
            return True
    return False

T = TypeVar('T')
def get_matching_item(container: Iterable[T], item: T) -> Optional[T]:
    return next((x for x in container if x == item), None)

def merge_vertexes(g: Graph, vertex_dict: dict[QuadTree, list[Waypoint]]):
    new_vertex_dict: dict[QuadTree, list[Waypoint]] = dict()

    for q in vertex_dict:
        for v in vertex_dict[q]:
            if v in g.vertexes:
                v_replace = get_matching_item(g.vertexes, v)
                v_replace = v_replace if v_replace else v
                if q in new_vertex_dict:
                    new_vertex_dict[q].append(v_replace)
                else:
                    new_vertex_dict[q] = [v_replace]
    return g, new_vertex_dict

def build_graph_on_quadtree(qtree: QuadTree, mode: VertMode = VertMode.CORNERS, return_vertex_dict: bool = False, quality=10) -> tuple[Graph, dict[QuadTree, list[Waypoint]]]:
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
    
    G = Graph()
    for q in vertex_dict:
        for v in vertex_dict[q]:
            G.add_vertex(v)
    # print(f"Before merging: {len(G.vertexes)}")
    G, vertex_dict = merge_vertexes(G, vertex_dict)
    # print(f"After merging: {len(G.vertexes)}")

    for q in vertex_dict:
        for v1 in vertex_dict[q]:
            for tq in chain([q], q.find_adjacent(direction='all'), q.recursive_parents()):
                for v2 in vertex_dict[tq]:
                    v2: Waypoint
                    if v1 == v2:
                        continue
                    if G.has_edge(v1, v2):
                        continue
                    if not check_collisions(qtree, Line(v1.coords, v2.coords)):
                        G.add_edge(v1, v2, cost=v1.distance(v2))
    
    # maybe redundant
    # G, vertex_dict = merge_vertexes(G, vertex_dict)
    return G if not return_vertex_dict else (G, vertex_dict)
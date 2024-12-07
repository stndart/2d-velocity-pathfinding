from .graph import Graph
from .graph import GraphVertex as Vertex
from .graph import GraphEdge as Edge

from backend.geometry import Point, Rectangle, Figure
from backend.sprites import Sprite

class QuadTree:
    def __init__(self, coords: Point, size: Point):
        assert size.x == size.y
        
        self.rectangle = Rectangle(coords, coords + size)
        self.sprites: list[Sprite] = []
        self.children = [None] * 4  # 4 since it is quadtree
    
    def add_sprites(self, sprites: list[Sprite]):
        pass
from .sprite import Sprite
from backend.pathfinding import Graph, Waypoint
from backend.geometry import Figure, Point, Line

class FigArray(Figure):
    def __init__(self, elements: set[Point|Line|Figure] = set()):
        self.elements = elements
    
    def add(self, element: Point|Line|Figure):
        self.elements.add(element)
    
    def __copy__(self):
        raise TypeError(f"Copying of {self.__class__.__name__} is not allowed")

    def __deepcopy__(self, memo):
        raise TypeError(f"Deep copying of {self.__class__.__name__} is not allowed")
    
    def has_intersect(self, other: 'Figure') -> bool:
        return any([e.has_intersect(other) for e in self.elements])
    
    def contains(self, other: Point) -> bool:
        return any([e.contains(other) for e in self.elements])
    
    def move(self, shift: Point):
        for e in self.elements:
            e.move(shift)
    
    def rotate(self, center: Point, angle: float):
        for e in self.elements:
            e.rotate(center, angle)

class GraphSprite(Sprite):
    def __init__(self, G: Graph):
        va = FigArray()
        for v in G.vertexes:
            if not isinstance(v, Waypoint):
                raise NotImplementedError("Can't create Sprite of an abstract Grpah. Graph must have Waypoint as vertices.")
            v: Waypoint
            
            va.add(v.coords)
            for e in v.edges:
                va.add(Line(e.v1.coords, e.v2.coords))
        
        super().__init__(mesh=va, collision_shape=None, static=True)
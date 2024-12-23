from .agents import Agent, Overseer
from .sprites import Sprite
from .pathfinding import QuadTree
from .geometry import Rectangle, Point

class Core(Overseer):
    def __init__(self, width: float = 100.0, height: float = 100.0):
        self.field_size = (width, height)
        self._sprites: list[Sprite] = []
        self._agents: list[Agent] = []
        
        self.quadtree = QuadTree(Rectangle(Point(-10, -10), Point(20, 20)))
        #self.quadtree = QuadTree(Rectangle(Point(0, 0), Point(20, 20)))
        self.pathfinder = None
    
    def add_sprite(self, f: Sprite):
        self._sprites.append(f)
        self.quadtree.add_sprites([f])
    
    def sprites(self) -> list[Sprite]:
        for f in self._sprites:
            yield f
    
    def add_agent(self, a: Agent):
        self._agents.append(a)
        self.quadtree.add_sprites([a.sprite])
    
    def agents(self) -> list[Agent]:
        for a in self._agents:
            yield a
    
    def update_object(self, obj: Agent):
        pass
    
    def update(self, deltatime: float):
        all_sprites = self._sprites + [a.sprite for a in self._agents]
        
        for a in self._agents:
            a.update(deltatime)
        
        for s in all_sprites:
            if s.static:
                continue
            s.update_collisions(self.quadtree.get_collision_candidates(s))
            
        for s in all_sprites:
            s.update(deltatime)
            
        self.quadtree.optimize_tree()
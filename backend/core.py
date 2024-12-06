from .agents import Agent, Overseer
from .sprites import Sprite

class Core(Overseer):
    def __init__(self, width: float = 100.0, height: float = 100.0):
        self.field_size = (width, height)
        self._sprites: list[Sprite] = []
        self._agents: list[Agent] = []
        self.pathfinder = None
    
    def add_sprite(self, f: Sprite):
        self._sprites.append(f)
    
    def sprites(self) -> list[Sprite]:
        for f in self._sprites:
            yield f
    
    def add_agent(self, a: Agent):
        self._agents.append(a)
    
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
            s.update_collisions(all_sprites)
            
        for s in all_sprites:
            s.update(deltatime)
from .geometry import Figure
from .agents import Agent, Overseer

class Core(Overseer):
    def __init__(self, width: float = 100.0, height: float = 100.0):
        self.field_size = (width, height)
        self._figures: list[Figure] = []
        self._agents: list[Agent] = []
        self.pathfinder = None
    
    def add_figure(self, f: Figure):
        self._figures.append(f)
    
    def figures(self) -> list[Figure]:
        for f in self._figures:
            yield f
    
    def add_agent(self, a: Agent):
        self._agents.append(a)
    
    def agents(self) -> list[Agent]:
        for a in self._agents:
            yield a
    
    def update_object(self, obj: Agent):
        pass
    
    def update(self, deltatime: float):
        for a in self.agents():
            a.update(deltatime)
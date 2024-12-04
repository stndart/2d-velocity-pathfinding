from .geometry import Point

class Agent:
    pass

class Overseer:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def update_object(self, obj: Agent):
        pass

class Agent:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.direction = 0
        
        self.overseer: Overseer = None

    def register_overseer(self, overseer: Overseer):
        self.overseer = overseer
    
    def update(self, deltatime: float):
        if self.overseer:
            self.overseer.update_object(self)
    
    def pos(self) -> Point:
        return Point(self.x, self.y)
    
    def coords(self) -> tuple[float]:
        return self.x, self.y
    
    def repr(self) -> list[Point]:
        return [Point(self.x, self.y)]
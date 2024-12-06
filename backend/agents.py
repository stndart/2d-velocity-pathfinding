from math import sin, cos, pi

from .geometry import Point
from .sprites import Sprite

class Agent:
    pass

class Overseer:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def update_object(self, obj: Agent):
        pass

class Agent:
    def __init__(self, c: Point, s: Sprite):
        self.sprite = s
        
        self.center = c
        self.direction = 0
        
        self.overseer: Overseer = None
    
    def dir_vec(self):
        return Point(cos(self.direction), sin(self.direction))

    def register_overseer(self, overseer: Overseer):
        self.overseer = overseer
        
    def move(self, mov: Point):
        self.sprite.movement += mov
    
    def rotate(self, angle: float):
        self.sprite.rotation += angle
    
    def update_sprite(self, deltatime: float):
        rot, mov = self.sprite.update(deltatime)
        self.center += mov
        self.direction += rot
    
    def update(self, deltatime: float):
        self.update_sprite(deltatime)
        if self.overseer:
            self.overseer.update_object(self)
    
    def pos(self) -> Point:
        return self.center
    
    def coords(self) -> tuple[float]:
        return self.center.coords()
    
    def repr(self) -> list[Point]:
        return [self.sprite.mass_center]
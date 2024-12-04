from math import sin, cos, pi

from backend.agents import Agent
from backend.geometry import Figure, Triangle, Point

class SimpleCar(Agent):
    def __init__(self, x: float = 0.0, y: float = 0.0):
        super().__init__(x, y)
        
        self.direction = 0
        self.speed = 0
    
    def dir_vec(self):
        return Point(cos(self.direction), sin(self.direction))
    
    def speed_vec(self):
        return self.dir_vec() * self.speed
    
    def turn(self, angle: float):
        self.direction += angle
    
    def accelerate(self, speed: float):
        self.speed += speed
    
    def update(self, deltatime: float):
        self.x += self.speed * cos(self.direction) * deltatime
        self.y += self.speed * sin(self.direction) * deltatime
        
        super().update(deltatime)
    
    def repr(self) -> list[Point]:
        width = 0.6
        pos = Point(self.x, self.y)
        
        w_vec = Point(cos(self.direction + pi / 2), sin(self.direction + pi / 2))
        
        return Triangle(
            pos + self.dir_vec() * width * 1.4,
            pos + w_vec * width - self.dir_vec() * width * 0.6,
            pos - w_vec * width - self.dir_vec() * width * 0.6,
        ).corners()
from math import sin, cos, pi

from backend.agents import Agent
from backend.geometry import Triangle, Point
from backend.sprites import make_sprite

class SimpleCar(Agent):
    def __init__(self, c: Point):
        width = 0.6
        
        dir_vec = Point(1, 0)
        w_vec = Point(0, 1)
        
        fig = Triangle(
            c + dir_vec * width * 1.4,
            c + w_vec * width - dir_vec * width * 0.6,
            c - w_vec * width - dir_vec * width * 0.6,
        )
        
        super().__init__(c, make_sprite(fig))
        
        self.speed = 0
    
    def speed_vec(self):
        return self.dir_vec() * self.speed
    
    def accelerate(self, speed: float):
        self.speed += speed
    
    def update(self, deltatime: float):
        self.move(self.speed_vec() * deltatime)
        super().update(deltatime)
    
    def repr(self) -> list[Point]:
        return self.sprite.mesh.vertexes()
from .sprite import make_sprite, Sprite
from backend.geometry import Figure, Rectangle, Triangle, Circle, Point
from random import choice, random
from math import pi, cos, sin

def randrange(a: float, b: float) -> float:
    return random() * (b - a) + a

def random_not_small(m: float):
    return (random() * 0.95 + 0.05) * m

class SpriteGenerator:
    def __init__(self, field: Rectangle, types: list[type] = [Triangle, Circle], av_size: float = 3, precision: float = 0.1):
        self.field = field
        self.types = types
        self.av_size = av_size
        self.precision = precision
    
    def gen_point_around(self, center: Point) -> Point:
        angle = random() * pi * 2
        dist = random_not_small(self.av_size / 2)
        return center + Point(dist * cos(angle), dist * sin(angle))
    
    def gen_figure(self) -> Figure:
        t = choice(self.types)
        if t is Triangle:
            center = Point(
                randrange(self.field.bottom_left.x, self.field.top_right.x),
                randrange(self.field.bottom_left.y, self.field.top_right.y),
            )
            return Triangle(*[self.gen_point_around(center) for i in range(3)])
        elif t is Circle:
            radius = random_not_small(self.av_size / 2)
            center = Point(
                randrange(self.field.bottom_left.x + radius, self.field.top_right.y - radius),
                randrange(self.field.bottom_left.y + radius, self.field.top_right.y - radius),
            )
            return Circle(center.x, center.y, radius)
        else:
            raise NotImplemented(f"Generation of {t} is not yet implemented.")
    
    def generate_sprites(self, n: int) -> list[Sprite]:
        return [make_sprite(self.gen_figure()) for i in range(n)]
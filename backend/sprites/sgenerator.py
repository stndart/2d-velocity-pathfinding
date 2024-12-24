from typing import Optional
from random import choice, random, gauss
from math import pi, cos, sin, atan2

from .sprite import make_sprite, Sprite
from backend.geometry import Figure, Rectangle, Triangle, Circle, Point
from .noisegen import fill_dots, mean_min_distance

def random_not_small(m: float):
    return (random() * 0.95 + 0.05) * m

def random_normal(mean: float, sigma: float) -> float:
    return gauss(mean, sigma)

def random_normal_pos(mean: float, sigma: float) -> float:
    return abs(random_normal(mean, sigma))

def random_uniform(a: float, b: float) -> float:
    return random() * (b - a) + a

class SpriteGenerator:
    def __init__(self, field: Rectangle, types: list[type] = [Triangle, Circle], avg_size: float = 3, precision: float = 0.1):
        self.field = field
        self.types = types
        self.avg_size = avg_size
        self.precision = precision
        
        # Triangle generation mode
        # 'simple' - generate triangles with random points around the center
        # 'normal' - generate triangles with normal distribution of area of the triangle
        self.triangle_mode = 'normal'
        # Figure distribution
        # 'random' - random distribution of triangles
        # 'uniform' - uniform distribution of triangles by Perlin noise height map thresholding
        self.distribution = 'uniform'
    
    def gen_point_around(self, center: Point, avg_size: float) -> Point:
        angle = random() * pi * 2
        dist = random_not_small(avg_size / 2)
        return center + Point(dist * cos(angle), dist * sin(angle))

    def gen_triangle(self, center: Point, avg_size: float, mode: str = 'normal') -> Triangle:
        if mode == 'simple':
            return self.gen_triangle_simple(center, avg_size)
        elif mode == 'normal':
            return self.gen_triangle_normal(center, avg_size)
    
    def gen_triangle_simple(self, center: Point, avg_size: float) -> Triangle:
        return Triangle(*[self.gen_point_around(center, avg_size) for i in range(3)])

    def gen_triangle_normal(self, center: Point, avg_size: float) -> Triangle:
        # Generate a random angle for the first vertex
        angle1 = random() * pi * 2
        angle1 = pi / 4
        # Generate a random radius with normal distribution for the first vertex
        radius1 = avg_size * random_normal_pos(1, 0.2)  # Adjust 0.1 for tighter spread
        p1 = center + Point(radius1 * cos(angle1), radius1 * sin(angle1))

        # Generate a second angle offset from the first to ensure non-collinearity
        angle2 = angle1 + random_uniform(pi * 0.2, pi * 0.8)
        radius2 = avg_size * random_normal_pos(1, 0.2)

        p2 = center + Point(radius2 * cos(angle2), radius2 * sin(angle2))

        # Area is spread normally around 0.5*avg_size^2
        area_factor = random_normal_pos(1, 0.2)
        area_factor *= 0.5 * avg_size ** 2
        height = 2 * area_factor / abs(p1 - p2)

        a21 = atan2(p1.y - p2.y, p1.x - p2.x)

        min_direction = pi / 4
        max_direction = 3 * pi / 4
        direction = -random_uniform(min_direction, max_direction)
        rad = -height / sin(direction)

        p3 = p2 + Point(rad * cos(a21 + direction), rad * sin(a21 + direction))

        return Triangle(p1, p2, p3)
    
    def gen_circle(self, center: Point, avg_size: float) -> Circle:
        radius = random_not_small(avg_size / 2)
        return Circle(center.x, center.y, radius)
    
    def gen_figure(self, center: Optional[Point] = None) -> Figure:
        t = choice(self.types)
        if not center:
            center = Point(
                random_uniform(self.field.bottom_left.x, self.field.top_right.x),
                random_uniform(self.field.bottom_left.y, self.field.top_right.y),
            )
        if t is Triangle:
            return self.gen_triangle(center, self.avg_size, self.triangle_mode)
        elif t is Circle:
            return self.gen_circle(center, self.avg_size)
        else:
            raise NotImplemented(f"Generation of {t} is not yet implemented.")
    
    def generate_sprites(self, n: int) -> list[Sprite]:
        if self.distribution == 'random':
            return [make_sprite(self.gen_figure()) for i in range(n)]
        else:
            centers = fill_dots(self.field, n)
            self.avg_size = mean_min_distance(centers) * 0.7
            return [make_sprite(self.gen_figure(center)) for center in centers]
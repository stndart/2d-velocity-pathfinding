from math import sqrt

EPS = 1e-5

def is_close(a, b, eps=EPS):
    return abs(a - b) < eps

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def has_intersect(self, other):
        if isinstance(other, Point):
            return is_close(self.x, other.x) and is_close(self.y, other.y)
        elif isinstance(other, Circle):
            return sqrt((self.x - other.x)**2 + (self.y - other.y)**2) <= other.radius + EPS
        elif isinstance(other, Rectangle):
            return (other.x1 - EPS <= self.x <= other.x2 + EPS and
                    other.y1 - EPS <= self.y <= other.y2 + EPS)
        elif isinstance(other, Triangle):
            return other.contains(self)
        return False


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def has_intersect(self, other):
        if isinstance(other, Point):
            return other.has_intersect(self)
        elif isinstance(other, Circle):
            dist = sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
            return dist <= self.radius + other.radius + EPS
        elif isinstance(other, Rectangle):
            closest_x = max(other.x1, min(self.x, other.x2))
            closest_y = max(other.y1, min(self.y, other.y2))
            dist = sqrt((self.x - closest_x)**2 + (self.y - closest_y)**2)
            return dist <= self.radius + EPS
        elif isinstance(other, Triangle):
            return any(self.has_intersect(Point(v[0], v[1])) for v in other.vertices) or other.intersects_circle(self)
        return False


class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = min(x1, x2), min(y1, y2)
        self.x2, self.y2 = max(x1, x2), max(y1, y2)

    def has_intersect(self, other):
        if isinstance(other, Point):
            return other.has_intersect(self)
        elif isinstance(other, Circle):
            return other.has_intersect(self)
        elif isinstance(other, Rectangle):
            return not (self.x2 + EPS < other.x1 or self.x1 > other.x2 + EPS or
                        self.y2 + EPS < other.y1 or self.y1 > other.y2 + EPS)
        elif isinstance(other, Triangle):
            return any(other.contains(Point(self.x1, self.y1)) or 
                       other.contains(Point(self.x2, self.y2)) or 
                       other.contains(Point(self.x1, self.y2)) or 
                       other.contains(Point(self.x2, self.y1)))
        return False


class Triangle:
    def __init__(self, v1, v2, v3):
        self.vertices = [v1, v2, v3]

    def area(self, a, b, c):
        return abs((a[0] * (b[1] - c[1]) + 
                    b[0] * (c[1] - a[1]) + 
                    c[0] * (a[1] - b[1])) / 2.0)

    def contains(self, point):
        a, b, c = self.vertices
        p = (point.x, point.y)
        area_orig = self.area(a, b, c)
        area1 = self.area(p, b, c)
        area2 = self.area(a, p, c)
        area3 = self.area(a, b, p)
        return is_close(area_orig, area1 + area2 + area3)

    def intersects_circle(self, circle):
        for v in self.vertices:
            if circle.has_intersect(Point(v[0], v[1])):
                return True
        return False

    def has_intersect(self, other):
        if isinstance(other, Point):
            return other.has_intersect(self)
        elif isinstance(other, Circle):
            return other.has_intersect(self)
        elif isinstance(other, Rectangle):
            return any(self.contains(Point(other.x1, other.y1)) or 
                       self.contains(Point(other.x2, other.y2)) or 
                       self.contains(Point(other.x1, other.y2)) or 
                       self.contains(Point(other.x2, other.y1)))
        elif isinstance(other, Triangle):
            return any(self.contains(Point(v[0], v[1])) or 
                       other.contains(Point(v2[0], v2[1])) for v in self.vertices)
        return False

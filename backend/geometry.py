import numpy as np
from typing import Generator
from itertools import pairwise

from math import sqrt, atan2

EPS = 1e-5

def is_close(a: float, b: float, eps: float = EPS):
    return abs(a - b) < eps

def sign(a: float):
    if a > EPS:
        return +1
    elif a < -EPS:
        return -1
    return 0

def rotation_matrix(angle: float) -> np.ndarray[float]:
    return np.array([
        [np.cos(angle), np.sin(angle)],
        [-np.sin(angle), np.cos(angle)]
    ])

class Point:
    pass

class Figure:
    def __init__(self):
        pass
    
    def copy(self):
        return Figure()
    
    def has_intersect(self, other: 'Figure') -> bool:
        return False
    
    def contains(self, other: Point) -> bool:
        return False

    def vertexes(self, quality: int = 0) -> list[Point]:
        return []
    
    def set_vertexes(self, vs: list[Point]):
        pass

    def mass_center(self):
        return Point(0, 0)
    
    def __repr__(self):
        if self.vertexes() == []:
            return f'{self.__class__.__name__}: []'

        arr = ''
        for i in self.vertexes()[:-1]:
            arr += f'{i}, '
        arr += self.vertexes()[-1].__repr__()
        
        return f'{self.__class__.__name__}: [{arr}]'
    
    def move(self, shift: Point):
        self.set_vertexes([v + shift for v in self.vertexes()])
    
    def rotate(self, center: Point, angle: float):
        rotmat = rotation_matrix(angle)
        vecs = np.array([[(v - center).x, (v - center).y] for v in self.vertexes()])
        nvecs = vecs.dot(rotmat)
        self.set_vertexes([Point(*c) + center for c in nvecs])

from functools import reduce
def sum_points(points: list[Point]):
    return reduce(lambda x, y: x + y, points)
def mean_points(points: list[Point]):
    return sum_points(points) / len(points)

# объявления классов для корректной типизации методов
class Circle(Figure):
    pass
class Triangle(Figure):
    pass
class Rectangle(Figure):
    pass
class Line:
    pass

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
    def copy(self):
        return Point(self.x, self.y)
    
    def vertexes(self, quality: int = 0) -> list[Point]:
        return [self]

    def mass_center(self):
        return self.copy()
    
    def move(self, shift: Point):
        self.x += shift.x
        self.y += shift.y
    
    def rotate(self, center: Point, angle: float):
        rotmat = rotation_matrix(angle)
        vecs = np.array([[(self - center).x, (self - center).y]])
        nvecs = vecs.dot(rotmat)
        c = Point(*nvecs[0]) + center
        self.x = c.x
        self.y = c.y

    def has_intersect(self, other: Point|Figure) -> bool:
        if isinstance(other, Point):
            return is_close(self.x, other.x) and is_close(self.y, other.y)
        elif isinstance(other, Figure):
            return other.contains(self)
        return False
    
    def distance_to(self, other: Point|Figure|Line) -> float:
        if isinstance(other, Point):
            return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        elif isinstance(other, Circle):
            return max(0, self.distance_to(other.center) - other.radius)
        elif isinstance(other, (Rectangle, Triangle)):
            if other.has_intersect(self):
                return 0
            return min([self.distance_to(e) for e in other.edges()])
        elif isinstance(other, Line):
            v1 = other.p2 - other.p1
            v2 = self - other.p1
            t = (v1 * v2) / abs(v1) ** 2
            if t < 0:
                return self.distance_to(other.p1)
            elif t > 1:
                return self.distance_to(other.p2)
            else:
                return abs(other.distance(self))
    
    def coords(self) -> tuple[float]:
        return self.x, self.y

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def __mul__(self, other: int|float|Point) -> Point | float:
        if isinstance(other, (float, int)):
            return Point(self.x * other, self.y * other)
        elif isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        else:
            raise NotImplementedError(f"__mul__ for args Point and {other.__class__} is not implemented")
    
    def dot(self, other: Point) -> float:
        # returns cross-product of two vectors
        return self.x * other.y - self.y * other.x
    
    def __truediv__(self, other: float) -> Point:
        return Point(self.x / other, self.y / other)
    
    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
    def __repr__(self):
        return f'<{self.x:.3f}, {self.y:.3f}>'
    
    def __hash__(self):
        return self.x.__hash__() + self.y.__hash__()
    
    def __eq__(self, other: Point) -> bool:
        if not isinstance(other, Point):
            return False
        return is_close(abs(self - other), 0)

    def angle_to(v1, v2):
        return atan2(v1.x * v2.y - v1.y * v2.x, v1.x * v2.x + v1.y * v2.y)

class Line:
    def __init__(self, p1: Point, p2: Point):
        if is_close(abs(p1 - p2), 0):
            raise ValueError("Отрезок не может быть задан двумя одинаковыми точками.")
        self.p1 = p1
        self.p2 = p2
        
    def copy(self):
        return Line(self.p1.copy(), self.p2.copy())

    def mass_center(self):
        return (self.p1 + self.p2) / 2
    
    def __repr__(self):
        return f'{self.__class__.__name__}: A={self.p1}, B={self.p2}'
    
    def print_eq(self):
        A = self.p2.y - self.p1.y
        B = self.p1.x - self.p2.x
        C = self.p2.x * self.p1.y - self.p1.x * self.p2.y
        return A, B, C
    
    def vertexes(self, quality: int = 0) -> list[Point]:
        return [self.p1, self.p2]
    
    def set_vertexes(self, vs: list[Point]):
        self.p1 = vs[0]
        self.p2 = vs[1]
    
    def __hash__(self):
        return self.p1.__hash__() + self.p2.__hash__()
    
    def __eq__(self, other: 'Line') -> bool:
        if not isinstance(other, Line):
            return False
        
        if self.p1 == other.p1:
            return self.p2 == other.p2
        elif self.p1 == other.p2:
            return self.p2 == other.p1
        return False
    
    def move(self, shift: Point):
        self.set_vertexes([v + shift for v in self.vertexes()])
    
    def rotate(self, center: Point, angle: float):
        rotmat = rotation_matrix(angle)
        vecs = np.array([[(v - center).x, (v - center).y] for v in self.vertexes()])
        nvecs = vecs.dot(rotmat)
        self.set_vertexes([Point(*c) for c in nvecs])

    def distance(self, p: Point) -> float:
        """
        Возвращает знаковое расстояние от точки до прямой.
        Если расстояние меньше нуля, то точка справа от прямой, если больше, то слева.
        (сторона выбирается при обходе прямой от p1 к p2)
        """
        # Векторное представление
        line_vec = self.p2 - self.p1  # Вектор направления прямой
        point_vec = p - self.p1       # Вектор от точки `p1` до `p`
        
        # Векторное произведение для нахождения площади параллелограмма
        # cross_product = line_vec.dot(point_vec)
        cross_product = line_vec.x * point_vec.y - line_vec.y * point_vec.x
        line_length = abs(line_vec)  # Длина вектора прямой

        # Расстояние = площадь / длина прямой
        return cross_product / line_length if line_length > EPS else 0.0

    def has_intersect(self, other: Point|Line|Figure) -> bool:
        if isinstance(other, Point):
            return other.distance_to(self) < EPS
        elif isinstance(other, Line):
            return self._intersects_line(other)
        elif isinstance(other, Figure):
            return other.has_intersect(self)
        return False

    def _intersects_line(self, other: Line) -> bool:
        """
        Проверяет, пересекаются ли два отрезка исключая концы отрезков
        """
        
        d1 = self.distance(other.p1)
        d2 = self.distance(other.p2)
        
        # Если отрезки коллинеарны, проверить не лежат ли вершины одного внутри другого
        if abs(d1) + abs(d2) < 2 * EPS:
            prod1 = (self.p1 - other.p1) * (self.p2 - other.p2)
            prod2 = (self.p1 - other.p2) * (self.p2 - other.p1)
            return any([prod1 < 0, prod2 < 0])
        
        # Проверка на то, что обе точки второго отрезка лежат с одной стороны от первого отрезка
        # if (self.p2 - self.p1).dot(other.p1 - self.p1) * (self.p2 - self.p1).dot(other.p2 - self.p1) > 0:
        if sign(d1) * sign(d2) > 0:
            return False
        
        intersection = (other.p1 * abs(d2) + other.p2 * abs(d1)) / (abs(d1) + abs(d2))
        return (self.p1 - intersection) * (self.p2 - intersection) < -EPS

class Circle(Figure):
    def __init__(self, x: float, y: float, radius: float):
        self.center = Point(x, y)
        self.radius = max(radius, 0)  # Убедимся, что радиус не отрицательный
        
    def copy(self):
        return Circle(self.center.x, self.center.y, self.radius)
    
    def __repr__(self):
        return f'{self.__class__.__name__}: C={self.center}, R={self.radius:.3f}'
    
    def _vertexes(self, quality: int = 0):
        """
        Returns N=quality vertices positioned on the circle
        """
        angles = np.linspace(0, np.pi * 2, quality + 1)[:-1]
        px = self.center.x + np.cos(angles) * self.radius
        py = self.center.y + np.sin(angles) * self.radius
        return [Point(x, y) for x, y in zip(px, py)]

    def vertexes(self, quality: int = 10):
        """
        Returns N=quality vertices, positioned outside the circle:
        Lines, connecting nearby points barely touch the circle
        quality should be >=3
        """
        if quality < 3:
            return self._vertexes()
        
        angles = np.linspace(0, np.pi * 2, quality + 1)[:-1]
        beta = np.pi / quality
        newrad = self.radius / np.cos(beta)
        px = self.center.x + np.cos(angles) * newrad
        py = self.center.y + np.sin(angles) * newrad
        return [Point(x, y) for x, y in zip(px, py)]

    def mass_center(self):
        return self.center.copy()

    def set_vertexes(self, vs: list[Point]):
        raise NotImplementedError("Circle can't be set with vertexes")
    
    def move(self, shift: Point):
        self.center += shift
    
    def rotate(self, center: Point, angle: float):
        rotmat = rotation_matrix(angle)
        vec = np.array((self.center - center).coords())
        self.center = Point(*(vec.dot(rotmat))) + center
    
    def _intersects_line(self, line: Line) -> bool:
        """
        Checks if the segment has any point inside the circle
        """
        # if line is away from center of the circle
        if abs(line.distance(self.center)) > self.radius - EPS:
            return False
        line_vec = line.p2 - line.p1
        p1_vec = line.p1 - self.center
        p2_vec = line.p2 - self.center
        # segment points are on different sides of the circle
        if (line_vec * p1_vec) * (line_vec * p2_vec) < 0:
            return True
        # segment points are on the same side of the circle
        if min(abs(line.p1 - self.center), abs(line.p2 - self.center)) < self.radius - EPS:
            return True
        return False
    
    def contains(self, other: Point|Figure|Line):
        """
        Checks if other figure is completely inside
        """
        if isinstance(other, Point):
            return self.has_intersect(other)
        elif isinstance(other, Circle):
            return abs(self.center - other.center) < self.radius - other.radius + EPS
        elif isinstance(other, (Figure, Line)):
            if any([not self.has_intersect(p) for p in other.vertexes()]):
                return False
            return True
        
        return False

    def has_intersect(self, other: Point|Line|Figure) -> bool:
        """
        Checks if intersection of two figures is not empty
        """
        if self.radius < EPS:  # Если радиус 0, окружность превращается в точку
            return self.center.has_intersect(other)
        elif isinstance(other, Point):
            return abs(self.center - other) < self.radius + EPS
        elif isinstance(other, Line):
            return self._intersects_line(other)
        elif isinstance(other, Circle):
            return abs(self.center - other.center) < self.radius + other.radius + EPS
        elif isinstance(other, Rectangle):
            return other.has_intersect(self)
        elif isinstance(other, Triangle):
            return other.has_intersect(self)
        return False

class Triangle(Figure):
    def __init__(self, v1: Point, v2: Point, v3: Point):
        self.vertices: list[Point] = [v1, v2, v3]
        
    def copy(self) -> Triangle:
        return Triangle(*[v.copy() for v in self.vertices])
    
    def vertexes(self, quality: int = 0) -> list[Point]:
        return self.vertices

    def mass_center(self):
        return mean_points(self.vertexes())
    
    def set_vertexes(self, vs: list[Point]):
        self.vertices = vs.copy()

    def area(self, a: Point, b: Point, c: Point) -> float:
        return abs((a.x * (b.y - c.y) + 
                    b.x * (c.y - a.y) + 
                    c.x * (a.y - b.y)) / 2.0)

    def is_degenerate(self) -> bool:
        return is_close(self.area(*self.vertices), 0)
    
    def corners(self) -> list[Point]:
        return self.vertices
    
    def edges(self) -> list[Line]:
        a, b, c = self.vertices
        return [Line(a, b), Line(b, c), Line(c, a)]

    def contains(self, other: Point|Figure|Line) -> bool:
        """
        Checks if other figure is completely inside
        """
        if isinstance(other, Point):
            return self.has_intersect(other)
        elif isinstance(other, Circle):
            if self.has_intersect(other.center):  # Center of the circle is inside, so we should check intersections with edges
                if any([other.center.distance_to(e) - other.radius < -EPS for e in self.edges()]):
                    return False
                return True
            else:
                return False
        elif isinstance(other, (Figure, Line)):
            if any([not self.contains(p) for p in other.vertexes()]):
                return False
            return True
        
        return False
    
    def has_intersect(self, other: Point|Line|Figure) -> bool:
        """
        Checks if intersection of two figures is not empty
        """
        if isinstance(other, Point):
            dists = [side.distance(other) for side in self.edges()]
            return all([d > EPS for d in dists]) or all([d < -EPS for d in dists])
        elif isinstance(other, Line):
            for e in self.edges():
                if e.has_intersect(other):
                    if e.distance(other.p1) < EPS and e.distance(other.p2) < EPS:
                        # coinsiding lines don't count
                        continue
                    else:
                        return True
            return False
        elif isinstance(other, Circle):
            return self._intersects_circle(other)
        elif isinstance(other, Triangle):
            return self._intersects_triangle(other)
        elif isinstance(other, Rectangle):
            return other.has_intersect(self)
        return False

    def _intersects_circle(self, circle: Circle) -> bool:
        a, b, c = self.vertices
        d1 = Line(a, b).distance(circle.center)
        d2 = Line(b, c).distance(circle.center)
        d3 = Line(c, a).distance(circle.center)
        
        if sign(d1) < 0 and sign(d2) < 0 and sign(d3) < 0: # Если центр окружности внутри треугольника
            return True
        elif sign(d1) > 0 and sign(d2) > 0 and sign(d3) > 0: # Если центр окружности внутри треугольника
            return True
        elif circle.contains(a) or circle.contains(b) or circle.contains(c): # Если хотя бы одна из вершин треугольника внутри окружности
            return True
        elif any([circle.has_intersect(edge) for edge in self.edges()]):
            return True # Если окружность пересекает хотя бы одну сторону треугольника
        return False
    
    def _intersects_triangle(self, other: Triangle) -> bool:
        e1s = self.edges()
        e2s = other.edges()
        
        for e1 in e1s:
            if any([e1.has_intersect(e2) for e2 in e2s]):
                return True
        if any([self.contains(p) for p in other.corners()]):
            return True
        if any([other.contains(p) for p in self.corners()]):
            return True
        return False

class Rectangle(Figure):
    def __init__(self, bottom_left: Point, top_right: Point):
        self.bottom_left = Point(min(bottom_left.x, top_right.x), min(bottom_left.y, top_right.y))
        self.top_right = Point(max(bottom_left.x, top_right.x), max(bottom_left.y, top_right.y))
        
    def copy(self) -> Rectangle:
        return Rectangle(self.bottom_left.copy(), self.top_right.copy())
    
    def size(self) -> Point:
        return self.top_right - self.bottom_left
    
    def width(self) -> float:
        return self.top_right.x - self.bottom_left.x
    
    def height(self) -> float:
        return self.top_right.y - self.bottom_left.y
    
    def vertexes(self, quality: int = 0) -> list[Point]:
        return self.corners()

    def mass_center(self):
        return mean_points(self.vertexes())
    
    def set_vertexes(self, vs: list[Point]):
        raise NotImplementedError("Rectangle can't be set with vertexes")
    
    def rotate(self, center: Point, angle: float):
        raise NotImplementedError("Rectangle can't be rotated")
    
    def corners(self) -> list[Point]:
        """
        Returns corners in the following order:
        bottom_left, top_left, top_right, bottom_right
        """
        p1, p3 = self.bottom_left, self.top_right
        p2 = Point(p1.x, p3.y)
        p4 = Point(p3.x, p1.y)
        return [p1, p2, p3, p4]
    
    def edges(self) -> list[Line]:
        """
        Returns edges in the following order:
        left, top, right, bottom
        """
        p1, p2, p3, p4 = self.corners()
        return [Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p1)]
    
    def contains(self, other: Point|Figure|Line) -> bool:
        """
        Checks if other figure is completely inside
        """
        if isinstance(other, Point):
            return self.has_intersect(other)
        elif isinstance(other, Circle):
            if self.has_intersect(other.center):  # Center of the circle is inside, so we should check intersections with edges
                if any([other.center.distance_to(e) - other.radius < -EPS for e in self.edges()]):
                    return False
                return True
            else:
                return False
        elif isinstance(other, (Figure, Line)):
            if any([not self.has_intersect(p) for p in other.vertexes()]):
                return False
            return True
        
        return False
    

    def has_intersect(self, other: Point|Line|Figure) -> bool:
        """
        Checks if intersection of two figures is not empty
        """
        if isinstance(other, Point):
            return (self.bottom_left.x + EPS <= other.x <= self.top_right.x - EPS and
                    self.bottom_left.y + EPS <= other.y <= self.top_right.y - EPS)
        elif isinstance(other, Line):
            return self.contains((other.p1 + other.p2) / 2) or\
                   any([other.has_intersect(e) for e in self.edges()]) or\
                   any([self.contains(v) for v in other.vertexes()])
        elif isinstance(other, Circle):
            return self._intersects_circle(other)
        elif isinstance(other, (Triangle, Rectangle)):
            return self._intersects_rectangle(other)

        return False

    def _intersects_circle(self, circle: Circle) -> bool:
        """
        Проверяет пересечение прямоугольника и окружности.
        """
        p1, p2, p3, p4 = self.corners()
        
        t1, t2 = Triangle(p1, p2, p3), Triangle(p1, p4, p3)
        return t1.has_intersect(circle) or t2.has_intersect(circle)

    def _intersects_rectangle(self, other: Rectangle|Triangle) -> bool:
        e1s = self.edges()
        e2s = other.edges()
        
        for e1 in e1s:
            if any([e1.has_intersect(e2) for e2 in e2s]):
                return True
        if any([self.contains(p) for p in other.corners()]):
            return True
        if any([other.contains(p) for p in self.corners()]):
            return True
        return False

class Path(Figure):
    def __init__(self, path: list[Point] = []):
        self.path = path
    
    def vertexes(self, quality: int = 0):
        return list(self.points())

    def mass_center(self):
        return mean_points(self.vertexes())

    def points(self) -> Generator[Point, None, None]:
        for p in self.path:
            yield p
    
    def segments(self) -> Generator[tuple[Point], None, None]:
        for p1, p2 in pairwise(self.path):
            yield p1, p2
    
    def add_point(self, point: Point, i: int = None):
        if i is None:
            i = len(self.path)
        assert i <= len(self.path) and i >= 0
        self.path = self.path[:i] + [point] + self.path[i:]
    
    def remove_point(self, i: int):
        assert i < len(self.path) and i >= 0
        self.path.pop(i)
    
    def update_point(self, i: int, np: Point):
        assert i < len(self.path) and i >= 0
        self.path[i] = np

    def has_intersect(self, other: Figure | Point | Line):
        for p in self.points():
            if other.has_intersect(p):
                return True
        for p1, p2 in self.segments():
            if other.has_intersect(Line(p1, p2)):
                return True
        return False
    
    def contains(self, other: Point):
        return self.has_intersect(other)
    
    def start_point(self):
        if len(self.path) < 1:
            return None
        return self.path[0]
    
    def current_point(self):
        if len(self.path) < 2:
            return None
        return self.path[1]
    
    def next_point(self):
        if len(self.path) >= 2:
            self.remove_point(0)
        return self.current_point()

def fig_distance(f1: Figure, f2: Figure):
    if isinstance(f1, Circle):
        if isinstance(f2, Circle):
            return max(0, abs(f1.center - f2.center) - f1.radius - f2.radius)
        else:
            return max(0, f1.center.distance_to(f2) - f1.radius)
    else:
        if isinstance(f2, Circle):
            return fig_distance(f2, f1)
        else:
            if f1.has_intersect(f2):
                return 0
            return min([v.distance_to(f2) for v in f1.vertexes()])

if __name__ == '__main__':
    c = Circle(1, 0, 1)
    l = Line(Point(0, 0), Point(1, 2))
    s = Triangle(Point(0, 0), Point(3, 3), Point(2, 1))
    
    test_n = 6
    if test_n == 0:
        print(c)
        c.rotate(c.center, np.deg2rad(45))
        print(c)
        c.rotate(Point(0, 0), np.deg2rad(45))
        print(c)
    
        print(l)
        l.rotate(Point(0, 0), np.deg2rad(45))
        print(l)
        l.rotate(Point(1, 2), np.deg2rad(-45))
        print(l)
    
        print(s)
        s.rotate(Point(0, 0), np.deg2rad(45))
        print(s)
        s.rotate(Point(1, 2), np.deg2rad(-45))
        print(s)
    
    elif test_n == 1:
        c1 = Circle(4, 6, 2)
        t1 = Triangle(Point(-0.160, 3.000), Point(-1.360, 3.600), Point(-1.360, 2.400))
        print(c1.has_intersect(t1))
        print(t1.has_intersect(c1))
    elif test_n == 2:
        t1 = Triangle(Point(2.290, 0.427), Point(1.212, 1.226), Point(1.004, 0.044))
        c1 = Circle(1.5, 0.5, 0.28)
        print(t1.has_intersect(c1))
        print(c1.has_intersect(t1))
        print(t1.contains(c1))
        print(c1.contains(t1))
    elif test_n == 3:
        t1 = Triangle(Point(2.070, -0.103), Point(1.147, 0.872), Point(0.737, -0.256))
        c1 = Circle(1.5, 0.5, 0.3)
        print(t1.has_intersect(c1))
        print(c1.has_intersect(t1))
        print(t1.contains(c1))
        print(c1.contains(t1))
        
        a, b, c = t1.vertices
        d1 = Line(a, b).distance(c1.center)
        d2 = Line(b, c).distance(c1.center)
        d3 = Line(c, a).distance(c1.center)
        
        print(d1, d2, d3)
        
        es = [e for e in t1.edges()]
        print(es[0], c1)
        print(c1.has_intersect(es[0]))
        
        es[0].print_eq()
    
    elif test_n == 4:
        t1 = Triangle(Point(0.044, 0.634), Point(-0.878, 1.609), Point(-1.288, 0.481))
        c1 = Circle(1.5, 0.5, 0.3)
        print(t1.has_intersect(c1))
        print(c1.has_intersect(t1))
        print(t1.contains(c1))
        print(c1.contains(t1))
        
        a, b, c = t1.vertices
        d1 = Line(a, b).distance(c1.center)
        d2 = Line(b, c).distance(c1.center)
        d3 = Line(c, a).distance(c1.center)
        
        print(d1, d2, d3)
        
        es = [e for e in t1.edges()]
        print(es[0], c1)
        print(c1.has_intersect(es[0]))
        print(es[1], c1)
        print(c1.has_intersect(es[1]))
        print(es[2], c1)
        print(c1.has_intersect(es[2]))
    
    elif test_n == 5:
        tria = Triangle(
            Point(1, 4.9),
            Point(2, 1),
            Point(3.4, 3)
        )
        L1 = Line(
            Point(0, 3.125),
            Point(6.25, 3.125)
        )
        L2 = Line(
            Point(3.125, 0),
            Point(3.125, 6.25)
        )
        e1, e2, e3 = tria.edges()
        
        assert e1.has_intersect(L1)
        assert not e1.has_intersect(L2)
        
        assert e3.has_intersect(L1)
        assert e3.has_intersect(L2)
        
        assert tria.has_intersect(L1)
        assert tria.has_intersect(L2)
        
        print("Test #5 is successfull")
        
    elif test_n == 6:
        L1 = Line(Point(0, 0), Point(10, 10))
        L2 = Line(Point(0, 0), Point(50, 50))
        L3 = Line(Point(0, 0), Point(60, 60))
        R = Rectangle(Point(0, 0), Point(50, 50))
        
        assert R.has_intersect(L1)
        assert R.has_intersect(L2)
        assert R.has_intersect(L3)
        
        print("Test #6 is successfull")
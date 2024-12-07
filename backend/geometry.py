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

class Line:
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
    
    def __repr__(self):
        arr = ''
        for i in self.vertexes()[:-1]:
            arr += f'{i}, '
        arr += self.vertexes()[-1].__repr__()
        
        return f'{self.__class__}: [{arr}]'
    
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

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        
    def copy(self):
        return Point(self.x, self.y)

    def has_intersect(self, other: Point|Figure) -> bool:
        if isinstance(other, Point):
            return is_close(self.x, other.x) and is_close(self.y, other.y)
        elif isinstance(other, Figure):
            return other.contains(self)
        return False
    
    def coords(self) -> tuple[float]:
        return self.x, self.y

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)
    
    def __mul__(self, other: float) -> Point:
        return Point(self.x * other, self.y * other)
    
    def __truediv__(self, other: float) -> Point:
        return Point(self.x / other, self.y / other)
    
    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
    def __repr__(self):
        return f'<{self.x:.3f}, {self.y:.3f}>'

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
    
    def __repr__(self):
        return f'{self.__class__}: A={self.p1}, B={self.p2}'
    
    def vertexes(self, quality: int = 0) -> list[Point]:
        return [self.p1, self.p2]
    
    def set_vertexes(self, vs: list[Point]):
        self.p1 = vs[0]
        self.p2 = vs[1]
    
    def move(self, shift: Point):
        self.set_vertexes([v + shift for v in self.vertexes()])
    
    def rotate(self, center: Point, angle: float):
        rotmat = rotation_matrix(angle)
        vecs = np.array([[(v - center).x, (v - center).y] for v in self.vertexes()])
        nvecs = vecs.dot(rotmat)
        self.set_vertexes([Point(*c) for c in nvecs])

    def distance(self, p: Point) -> float:
        '''
        Возвращает знаковое расстояние от точки до прямой.
        Если расстояние меньше нуля, то точка справа от прямой, если больше, то слева.
        (сторона выбирается при обходе прямой от p1 к p2)
        '''
        # Векторное представление
        line_vec = self.p2 - self.p1  # Вектор направления прямой
        point_vec = p - self.p1       # Вектор от точки `p1` до `p`
        
        # Векторное произведение для нахождения площади параллелограмма
        cross_product = line_vec.x * point_vec.y - line_vec.y * point_vec.x
        line_length = abs(line_vec)  # Длина вектора прямой

        # Расстояние = площадь / длина прямой
        return cross_product / line_length if line_length > EPS else 0.0

    def has_intersect(self, other: Line) -> bool:
        """
        Проверяет, пересекаются ли два отрезка.
        """
        def orientation(p: Point, q: Point, r: Point) -> int:
            """
            Вычисляет ориентацию трёх точек:
            0 -> коллинеарны,
            1 -> по часовой стрелке,
            2 -> против часовой стрелки.
            """
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if is_close(val, 0):
                return 0
            return 1 if val > 0 else 2

        def on_segment(p: Point, q: Point, r: Point) -> bool:
            """
            Проверяет, лежит ли точка q на отрезке pr.
            """
            return (min(p.x, r.x) - EPS <= q.x <= max(p.x, r.x) + EPS and
                    min(p.y, r.y) - EPS <= q.y <= max(p.y, r.y) + EPS)

        # Концы текущего и другого отрезка
        p1, q1 = self.p1, self.p2
        p2, q2 = other.p1, other.p2

        # Определяем ориентации
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # Основной случай: разные ориентации
        if o1 != o2 and o3 != o4:
            return True

        # Специальные случаи: проверка на коллинеарность
        if o1 == 0 and on_segment(p1, p2, q1):
            return True
        if o2 == 0 and on_segment(p1, q2, q1):
            return True
        if o3 == 0 and on_segment(p2, p1, q2):
            return True
        if o4 == 0 and on_segment(p2, q1, q2):
            return True

        return False

class Circle(Figure):
    def __init__(self, x: float, y: float, radius: float):
        self.center = Point(x, y)
        self.radius = max(radius, 0)  # Убедимся, что радиус не отрицательный
        
    def copy(self):
        return Circle(self.center.x, self.center.y, self.radius)
    
    def __repr__(self):
        return f'{self.__class__}: C={self.center}, R={self.radius:.3f}'
    
    def vertexes(self, quality: int = 0):
        angles = np.linspace(0, np.pi * 2, quality)
        px = self.center.x + np.cos(angles)
        py = self.center.y + np.sin(angles)
        return [Point(x, y) for x, y in zip(px, py)]

    def set_vertexes(self, vs: list[Point]):
        raise NotImplementedError("Circle can't be set with vertexes")
    
    def move(self, shift: Point):
        self.center += shift
    
    def rotate(self, center: Point, angle: float):
        rotmat = rotation_matrix(angle)
        vec = np.array((self.center - center).coords())
        self.center = Point(*(vec.dot(rotmat))) + center
    
    def _intersects_line(self, line: Line) -> bool:
        x0 = line.p1.x
        y0 = line.p1.y
        x1 = (line.p2 - line.p1).x
        y1 = (line.p2 - line.p1).y
        
        A = x1 ** 2 + y1 ** 2
        B = 2 * x1 * (x0 - self.center.x) +  2 * y1 * (y0 - self.center.y)
        C = (x0 - self.center.x) ** 2 + (y0 - self.center.y) ** 2
        
        D = B ** 2 - 4 * A * C
        if D < 0:
            return False
        t1 = (-B - sqrt(D)) / (4 * A * C)
        t2 = (-B + sqrt(D)) / (4 * A * C)
        
        if 0 <= t1 <= 1:
            return True
        if 0 <= t2 <= 1:
            return True
        return False
    
    def contains(self, other: Point) -> bool:
        return abs(self.center - other) < self.radius + EPS

    def has_intersect(self, other: Figure | Line) -> bool:
        if self.radius < EPS:  # Если радиус 0, окружность превращается в точку
            return other.contains(self.center)
        elif isinstance(other, Line):
            return self._intersects_line(other)
        elif isinstance(other, Circle):
            dist = abs(self.center - other.center)
            return is_close(dist, self.radius + other.radius)
        elif isinstance(other, Rectangle):
            return other.has_intersect(self)
        elif isinstance(other, Triangle):
            return other.has_intersect(self)
        return False

class Triangle(Figure):
    def __init__(self, v1: Point, v2: Point, v3: Point):
        self.vertices: list[Point] = [v1, v2, v3]
        
    def copy(self):
        return Triangle(*[v.copy() for v in self.vertices])
    
    def vertexes(self, quality: int = 0):
        return self.vertices
    
    def set_vertexes(self, vs: list[Point]):
        self.vertices = vs.copy()

    def area(self, a: Point, b: Point, c: Point) -> bool:
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

    def contains(self, p: Point) -> bool:
        a, b, c = self.vertices
        area_orig = self.area(a, b, c)
        area1 = self.area(p, b, c)
        area2 = self.area(a, p, c)
        area3 = self.area(a, b, p)
        return is_close(area_orig, area1 + area2 + area3)

    def _intersects_circle(self, circle: Circle) -> bool:
        a, b, c = self.vertices
        d1 = Line(a, b).distance(circle.center)
        d2 = Line(b, c).distance(circle.center)
        d3 = Line(c, a).distance(circle.center)
        
        if sign(d1) < 0 and sign(d2) < 0 and sign(d3) < 0: # Если центр окружности внутри треугольника
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

    def has_intersect(self, other: Figure | Line) -> bool:
        if isinstance(other, Line):
            return any([other.has_intersect(e) for e in self.edges()])
        elif isinstance(other, Circle):
            return self._intersects_circle(other)
        elif isinstance(other, Triangle):
            return self._intersects_triangle(other)
        elif isinstance(other, Rectangle):
            return other.has_intersect(self)
        return False

class Rectangle(Figure):
    def __init__(self, bottom_left: Point, top_right: Point):
        self.bottom_left = Point(min(bottom_left.x, top_right.x), min(bottom_left.y, top_right.y))
        self.top_right = Point(max(bottom_left.x, top_right.x), max(bottom_left.y, top_right.y))
        
    def copy(self):
        return Rectangle(self.bottom_left.copy(), self.top_right.copy())
    
    def vertexes(self, quality: int = 0):
        return self.corners()
    
    def set_vertexes(self, vs: list[Point]):
        raise NotImplementedError("Rectangle can't be set with vertexes")
    
    def rotate(self, center: Point, angle: float):
        raise NotImplementedError("Rectangle can't be rotated")
    
    def corners(self) -> list[Point]:
        p1, p3 = self.bottom_left, self.top_right
        p2 = Point(p1.x, p3.y)
        p4 = Point(p3.x, p1.y)
        return [p1, p2, p3, p4]
    
    def edges(self) -> list[Line]:
        p1, p2, p3, p4 = self.corners()
        return [Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p1)]

    def contains(self, p: Point) -> bool:
        """
        Проверяет, находится ли точка внутри прямоугольника (включая границы).
        """
        return (self.bottom_left.x - EPS <= p.x <= self.top_right.x + EPS and
                self.bottom_left.y - EPS <= p.y <= self.top_right.y + EPS)

    def has_intersect(self, other: Figure | Line) -> bool:
        """
        Проверяет пересечение прямоугольника с другими фигурами.
        """
        if isinstance(other, Line):
            return any([other.has_intersect(e) for e in self.edges()])
        elif isinstance(other, Circle):
            return self._intersects_circle(other)
        if isinstance(other, (Triangle, Rectangle)):
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


if __name__ == '__main__':
    c = Circle(1, 0, 1)
    l = Line(Point(0, 0), Point(1, 2))
    s = Triangle(Point(0, 0), Point(3, 3), Point(2, 1))
    
    #print(c)
    #c.rotate(c.center, np.deg2rad(45))
    #print(c)
    #c.rotate(Point(0, 0), np.deg2rad(45))
    #print(c)

    #print(l)
    #l.rotate(Point(0, 0), np.deg2rad(45))
    #print(l)
    #l.rotate(Point(1, 2), np.deg2rad(-45))
    #print(l)

    #print(s)
    #s.rotate(Point(0, 0), np.deg2rad(45))
    #print(s)
    #s.rotate(Point(1, 2), np.deg2rad(-45))
    #print(s)
    
    c1 = Circle(4, 6, 2)
    t1 = Triangle(Point(-0.160, 3.000), Point(-1.360, 3.600), Point(-1.360, 2.400))
    print(c1.has_intersect(t1))
    print(t1.has_intersect(c1))
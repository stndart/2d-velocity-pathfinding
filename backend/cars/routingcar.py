from math import degrees

from .simplecar import SimpleCar
from backend.geometry import Path, Point, sign

class RoutingCar(SimpleCar):
    def __init__(self, path: Path, turnspeed: float = 0.3, maxspeed: float = 1):
        super().__init__(*path.start_point().coords())

        self.path = path        
        self.next_point = path.current_point()
        assert self.next_point is not None
        
        self.turnspeed = turnspeed
        self.maxspeed = maxspeed
    
    def update(self, deltatime: float):
        self.path.update_point(0, self.pos())
        
        if self.next_point is None:
            return
        
        if self.pos().has_intersect(self.next_point):
            self.speed = 0
            self.next_point = self.path.next_point()
            return
        
        direction_vec = self.next_point - self.pos()
        direction_vec /= abs(direction_vec)
        if self.dir_vec().has_intersect(direction_vec):
            distance_to_travel = abs(self.pos() - self.next_point)
            self.speed = self.maxspeed if distance_to_travel > self.speed * deltatime else distance_to_travel / deltatime
        else:
            self.speed = 0
            angle_to_turn = self.dir_vec().angle_to(direction_vec)
            angle_to_turn_abs = min(self.turnspeed * deltatime, abs(angle_to_turn))
            self.turn(angle_to_turn_abs * sign(angle_to_turn))
        
        super().update(deltatime)
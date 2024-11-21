from math import sin, cos

class Overseer:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def update_object(self, obj):
        pass

class SimpleCar:
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
        
        self.direction = 0
        self.speed = 0
        
        self.overseer = None
    
    def turn(self, angle: float):
        self.direction += angle
    
    def accelerate(self, speed: float):
        self.speed += speed
        
    def register_overseer(self, overseer: Overseer):
        self.overseer = overseer
    
    def update(self, deltatime: float):
        self.x += self.speed * cos(self.direction) * deltatime
        self.y += self.speed * sin(self.direction) * deltatime
        
        if self.overseer:
            self.overseer.update_object(self)
    
    def coords(self):
        return self.x, self.y
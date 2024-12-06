from backend.geometry import Figure, Point, mean_points

class Sprite:
    def __init__(self, mesh: Figure, collision_shape: Figure):
        self.mesh: Figure = mesh
        self.collision_shape: Figure = collision_shape
        if self.collision_shape is not None:
            self.mass_center: Point = mean_points(self.collision_shape.vertexes(quality=4))
        else:
            self.mass_center = Point(0, 0)
        
        self.blocked = False
        self.movement = Point(0, 0)
        self.rotation = 0.0
    
    def check_collisions(self, others: list['Sprite']) -> list[int]:
        collides = []
        for i, sprite in enumerate(others):
            if sprite is self:
                continue
            if self.collision_shape.has_intersect(sprite.collision_shape):
                collides.append(i)
        return collides

    def update_collisions(self, others: list['Sprite']):
        if len(self.check_collisions(others)) > 0:
            #self.blocked = True
        #else:
            self.blocked = False
    
    def update(self, deltatime: float):
        rot, mov = 0, 0
        
        if not self.blocked:
            rot = self.rotation
            mov = self.movement
            
            self.collision_shape.rotate(self.mass_center, self.rotation)
            self.mesh.rotate(self.mass_center, self.rotation)
            self.collision_shape.move(self.movement)
            self.mesh.move(self.movement)
            
            self.rotation = 0.0
            self.movement = Point(0, 0)
        
        return rot, mov

def make_sprite(f: Figure):
    return Sprite(f, f)
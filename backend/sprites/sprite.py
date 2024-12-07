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
        if self.collision_shape is None:
            return []
        
        collides = []
        for i, sprite in enumerate(others):
            if sprite is self:
                continue
            if sprite.collision_shape is None:
                continue
            if self.collision_shape.has_intersect(sprite.collision_shape):
                collides.append(i)
        return collides

    def update_collisions(self, others: list['Sprite']):
        if len(self.check_collisions(others)) > 0:
            self.blocked = True
        else:
            self.blocked = False
    
    def update(self, deltatime: float):
        rot, mov = 0, Point(0, 0)
        
        if not self.blocked:
            rot = self.rotation
            mov = self.movement
            
            if self.collision_shape is not None:
                self.collision_shape.rotate(self.mass_center, rot)
                self.collision_shape.move(mov)
            if self.mesh is not None:
                self.mesh.rotate(self.mass_center, rot)
                self.mesh.move(mov)
            self.mass_center += mov
            
            self.rotation = 0.0
            self.movement = Point(0, 0)
        
        return rot, mov
    
    def __hash__(self):
        return id(self)

def make_sprite(f: Figure):
    return Sprite(f.copy(), f.copy())
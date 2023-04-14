import arcade
import math
import pymunk
from conf import SCREEN_HEIGHT, SCREEN_WIDTH

class Object(arcade.Sprite):
    def __init__(self, image, scale, angle, center_x, center_y, fixed = False, destructible=True, destroyed=False, shape=None):
        super().__init__(image, scale, angle=angle, center_x=center_x, center_y=center_y)
        self.shape = shape
        self.fixed = fixed
        self.destroyed = destroyed
        self.destructible = destructible
    
    def make_shape_box(self, mass, size, static=False, elasticity=0, friction=0):
        if static : body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else : body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        body.position = pymunk.Vec2d(self.center_x, self.center_y)
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elasticity
        shape.friction = friction
        self.shape = shape

    def make_shape_circle(self, mass, radius, static=False, elasticity=0, friction=0):
        if static : body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else : body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        body.position = pymunk.Vec2d(self.center_x, self.center_y)
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        self.shape = shape

    def update(self):
        if not self.destroyed and not self.fixed:
            self.shape.body.position += self.velocity
            self.angle = math.degrees(self.shape.body.angle)
            self.center_x = self.shape.body.position.x
            self.center_y = self.shape.body.position.y
    
    def kill(self):
        if self.destructible :
            self.destroyed = True
            self.texture = arcade.load_texture("img/tank_dead.png")

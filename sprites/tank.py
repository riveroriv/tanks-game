import arcade
import math
import pymunk
from .bullet import Bullet

class Tank(arcade.Sprite):
    def __init__(self, image, scale, center_x, center_y, shape=None, refill_seconds=4):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        self.shape = shape
        self.alive = True
        self.bullets = 5
        self.speed = 0
        self.direction = 1
        self.rotate_speed = 90
        self.angular_velocity = self.rotate_speed
        self.munition = dict()
        self.refill_delta = refill_seconds * 60
        self.refill_time = 0
    
    def make_shape(self, mass, size, elasticity=1, friction=1):
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        body.position = pymunk.Vec2d(self.center_x, self.center_y)
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elasticity
        shape.friction = friction
        self.shape = shape
        return (shape, body)


    def update(self):
        self.shape.body.angular_velocity = math.radians(self.angular_velocity)
        self.angle = math.degrees(self.shape.body.angle)
        self.center_x = self.shape.body.position.x - self.speed * math.sin(math.radians(self.angle))
        self.center_y = self.shape.body.position.y + self.speed * math.cos(math.radians(self.angle))
        self.shape.body.position = pymunk.Vec2d(self.center_x, self.center_y)

        if self.bullets < 5:
            self.refill_time+=1
        if self.refill_time >= self.refill_delta and self.bullets < 5:
            self.refill_time = 0
            self.munition[self.bullets].fill()
            self.bullets+=1
    
    def avanzar(self):
        if self.alive :
            self.angular_velocity = 0
            self.speed = 2
            self.direction *= -1
    
    def detener(self):
        if self.alive :
            self.angular_velocity = self.rotate_speed * self.direction
            self.speed = 0
    
    def die(self):
        self.alive = False
        self.angular_velocity = 0
        self.speed = 0
        self.texture = arcade.load_texture("img/tank_dead_s.png")
        for m in self.munition.values():
            m.remove_from_sprite_lists()
    
    def shoot(self):
        if self.alive and self.bullets>0 :
            bullet = Bullet('img/bullet.png', 1, self.angle , self.center_x, self.center_y)
            bullet.make_shape(1, 5)
            bullet.velocity = (
                    15 * math.cos(math.radians(self.angle + 90)),
                    15 * math.sin(math.radians(self.angle + 90))
            )
            self.bullets-=1
            self.munition[self.bullets].use()
            return bullet
        return None
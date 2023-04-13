import arcade
import math
import pymunk

class Tank(arcade.Sprite):
    def __init__(self, image, scale, center_x, center_y, shape=None):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        self.shape = shape
        self.speed = 0
        self.direction = 1
        self.rotate_speed = 90
        self.angular_velocity = self.rotate_speed
    
    def update(self):
        self.shape.body.angular_velocity = math.radians(self.angular_velocity)
        self.angle = math.degrees(self.shape.body.angle)
        self.center_x = self.shape.body.position.x - self.speed * math.sin(math.radians(self.angle))
        self.center_y = self.shape.body.position.y + self.speed * math.cos(math.radians(self.angle))
        self.shape.body.position = pymunk.Vec2d(self.center_x, self.center_y)
    
    def avanzar(self):
        self.angular_velocity = 0
        self.speed = 2
        self.direction *= -1
    
    def detener(self):
        self.angular_velocity = self.rotate_speed * self.direction
        self.speed = 0
import arcade
import math

class Tank(arcade.Sprite):
    def __init__(self, image, scale, center_x, center_y):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        
        self.speed = 0
        self.direction = 1
        self.rotate_speed = 2

        #self.shape = shape
    
    def update(self):
        self.angle += self.rotate_speed
        self.center_x += -self.speed * math.sin(math.radians(self.angle))
        self.center_y += self.speed * math.cos(math.radians(self.angle))
    
    def avanzar(self):
        self.speed = 2
        self.rotate_speed = 0
        self.direction *= -1
    
    def detener(self):
        self.speed = 0
        self.rotate_speed = 2*self.direction
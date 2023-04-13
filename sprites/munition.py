import arcade
import math
import pymunk
from conf import SCREEN_HEIGHT, SCREEN_WIDTH

class Munition(arcade.Sprite):
    def __init__(self, index, owner, angle, center_x, center_y, image='img/bullet.png', scale=1):
        super().__init__(image, scale, angle=angle, center_x=center_x, center_y=center_y)
        self.index = index
        self.owner = owner
        self.used = False

    def use(self):
        self.texture = arcade.load_texture("img/bullet_no.png")
    
    def fill(self):
        self.texture = arcade.load_texture("img/bullet.png")
    #def update(self):
        
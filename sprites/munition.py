import arcade
import math
import pymunk
from conf import SCREEN_HEIGHT, SCREEN_WIDTH

class Munition(arcade.Sprite):
    '''
    Clase para los sprites de munición en los paneles de munición
    '''
    def __init__(self, index, owner, angle, center_x, center_y, image='img/bullet.png', scale=1):
        super().__init__(image, scale, angle=angle, center_x=center_x, center_y=center_y)
        self.index = index
        '''índice en el panel de municion'''
        self.owner = owner
        '''índice del jugador al que pertenece el panel'''
        self.used = False
        '''munición ha sido usada?'''

    def use(self):
        '''cambia la textura del sprite a no bala'''
        self.texture = arcade.load_texture("img/bullet_no.png")
    
    def fill(self):
        '''cambia la textura del sprite a bala'''
        self.texture = arcade.load_texture("img/bullet.png")
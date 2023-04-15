import arcade
import math
import pymunk
from conf import SCREEN_HEIGHT, SCREEN_WIDTH

class Bullet(arcade.Sprite):
    '''
    Clase que contiene la lógica de la bala
    '''
    def __init__(self, image, scale, angle, center_x, center_y, owner, shape=None, speed=200):
        super().__init__(image, scale, angle=angle, center_x=center_x, center_y=center_y)
        self.owner = owner
        '''índice del tank que la creó'''
        self.shape = shape
        '''shape de la bala'''
        self.speed = speed
        '''rapidez de la bala, 200 por defecto'''
        if shape != None: self.collision_info()
        self.velocity = pymunk.Vec2d(1, 0).rotated(math.radians(self.angle)) * self.speed / 60
        '''vector velocidad de la vala'''
    
    def make_shape(self, mass, radius, elasticity=0, friction=0):
        '''
        Crea la forma y cuerpo de la bala para que interactue con otros objetos
        
        Atributos:
            mass - masa del cuerpo
            radius - radio del círculo
            elasticity - opcional
            friction - opcional
        '''
        body = pymunk.Body(mass, pymunk.moment_for_circle(mass,0, radius))
        body.position = pymunk.Vec2d(self.center_x, self.center_y)
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        self.shape = shape
        self.collision_info()

    def update(self):
        '''
        Actualiza la posición de la bala según el vector velocidad
        elimina las balas si salen de la pantalla
        '''
        self.shape.body.position += self.velocity
        self.center_x = self.shape.body.position.x
        self.center_y = self.shape.body.position.y
        if self.top > SCREEN_HEIGHT or self.bottom < 0 or self.right > SCREEN_WIDTH or self.left < 0:
            self.shape.collision_type = 0 # para que su shape no afecte en las coliciones
            self.remove_from_sprite_lists()
            self.kill()
    
    def collision_info(self):
        '''añaden información una autoreferencia al body y el tipo de colision'''
        self.shape.body.data = self
        self.shape.collision_type = 1
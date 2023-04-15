import arcade
import math
import pymunk
from conf import SCREEN_HEIGHT, SCREEN_WIDTH

class Object(arcade.Sprite):
    '''
    Clase para crear objetos con diferentes interacciones en el mapa
    como ser cajas, rocas o arbustos
    '''
    def __init__(self, image, scale, angle, center_x, center_y, destructible=True, destroyed=False, destroyed_image=None, shape=None):
        super().__init__(image, scale, angle=angle, center_x=center_x, center_y=center_y)
        self.shape = shape
        '''shape del objeto'''
        if shape != None: self.collision_info()
        self.destroyed_image = destroyed_image
        '''imagen de objeto destruido'''
        self.destroyed = destroyed
        '''el objeto está destruido?'''
        self.destructible = destructible
        '''el objeto se puede destruir?'''
    
    def make_shape_box(self, mass, size, static=False, elasticity=0, friction=0):
        '''
        crea un body y shape para un objeto con forma de caja
        Atributos:
            mass - masa
            size - tamaño en tupla (x,y)
            static - es inamovible (bool)
            elasticity - opcional
            friction - opcional
        '''
        if static : body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else : body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        body.position = pymunk.Vec2d(self.center_x, self.center_y)
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elasticity
        shape.friction = friction
        self.shape = shape
        self.collision_info()

    def make_shape_circle(self, mass, radius, static=False, elasticity=0, friction=0):
        '''
        crea un body y shape para un objeto con forma circular
        Atributos:
            mass - masa
            radius - radio
            static - es inamovible (bool)
            elasticity - opcional
            friction - opcional
        '''
        if static : body = pymunk.Body(body_type=pymunk.Body.STATIC)
        else : body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        body.position = pymunk.Vec2d(self.center_x, self.center_y)
        shape = pymunk.Circle(body, radius)
        shape.elasticity = elasticity
        shape.friction = friction
        self.shape = shape
        self.collision_info()

    def update(self):
        '''
        actualiza la información del objeto a menos que esté destruido
        '''
        if not self.destroyed :
            self.shape.body.position += self.velocity
            self.angle = math.degrees(self.shape.body.angle)
            self.center_x = self.shape.body.position.x
            self.center_y = self.shape.body.position.y
    
    def destroy(self):
        '''
        cambia la textura a imagen de objeto destruido
        y si es destruible lo destruye.
        
        Esto da lugar a que también haya objetos
        con imagen de destruido o desgastado y que se puedan mover.
        '''
        if self.destroyed_image != None :
            self.texture = arcade.load_texture(self.destroyed_image)
        if self.destructible :
            self.destroyed = True
    
    def collision_info(self):
        '''añaden información una autoreferencia al body y el tipo de colision'''
        self.shape.body.data = self
        self.shape.collision_type = 3

import arcade
import math
import pymunk
from .bullet import Bullet

class Tank(arcade.Sprite):
    def __init__(self, image, scale, center_x, center_y, player=0, shape=None, refill_seconds=4):
        super().__init__(image, scale, center_x=center_x, center_y=center_y)
        self.player = player
        '''índice del jugador'''
        self.shape = shape
        '''forma del tank'''
        if shape != None : self.collision_info()
        self.alive = True
        '''boolean sie está vivo'''
        self.bullets = 5
        '''cantidad de balas disponibles'''
        self.speed = 0
        '''rapidez del tanke'''
        self.direction = 1
        '''
        sentido de rotación
            1   contra reloj
            -1  reloj
        '''
        self.rotate_speed = 90
        '''rapidez angular'''
        self.angular_velocity = self.rotate_speed
        '''velocidad angular, toma en cuenta la dirección de rotación'''
        self.munition = dict()
        '''sprites de munición del  panel de munición'''
        self.refill_delta = refill_seconds * 60
        '''tiempo de espera para recargar una bala'''
        self.refill_time = 0
        '''tiempo transcurrido'''
    
    def make_shape(self, mass, size, elasticity=1, friction=1):
        '''
        crea un body y shape para un objeto con forma de caja
        Atributos:
            mass - masa
            size - tamaño en tupla (x,y)
            elasticity - opcional
            friction - opcional
        '''
        body = pymunk.Body(mass, pymunk.moment_for_box(mass, size))
        body.position = pymunk.Vec2d(self.center_x, self.center_y)
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = elasticity
        shape.friction = friction
        self.shape = shape
        self.collision_info()
        return (shape, body)


    def update(self):
        # velocidad angular y angulo
        self.shape.body.angular_velocity = math.radians(self.angular_velocity)
        self.angle = math.degrees(self.shape.body.angle)

        # posición
        self.center_x = self.shape.body.position.x - self.speed * math.sin(math.radians(self.angle))
        self.center_y = self.shape.body.position.y + self.speed * math.cos(math.radians(self.angle))
        self.shape.body.position = pymunk.Vec2d(self.center_x, self.center_y)

        # recarga de balas y panel de munición
        if self.bullets < 5:
            self.refill_time+=1
        if self.refill_time >= self.refill_delta and self.bullets < 5:
            self.refill_time = 0
            self.munition[self.bullets].fill()
            self.bullets+=1
    
    def avanzar(self):
        '''Para de rotar y avanza, cambia la dirección de rotación para la siuiente detenida'''
        if self.alive :
            self.angular_velocity = 0
            self.speed = 2
            self.direction *= -1
    
    def detener(self):
        '''Deja de avanzar y continúa rotando'''
        if self.alive :
            self.angular_velocity = self.rotate_speed * self.direction
            self.speed = 0
    
    def die(self):
        '''
        mata al jugador, detiene su rotación o si estaba avanzando
        remueve la munición del panel de munición
        cambia su imagen por la textura de muerto
        '''
        self.alive = False
        self.angular_velocity = 0
        self.speed = 0
        self.texture = arcade.load_texture("img/tank_dead_s.png")
        for m in self.munition.values():
            m.remove_from_sprite_lists()
    
    def shoot(self):
        '''
        Crea un objeto bala en la posición que se encuentre
        con ángulo en el que apunta y lo retorna.

        Retorna none si el tank está muerto o si no tiene balas
        '''
        if self.alive and self.bullets>0 :
            bullet = Bullet('img/bullet.png', 1, self.angle , self.center_x, self.center_y, self.player)
            bullet.make_shape(1, 7)
            bullet.velocity = (
                    15 * math.cos(math.radians(self.angle + 90)),
                    15 * math.sin(math.radians(self.angle + 90))
            )
            self.bullets-=1
            self.munition[self.bullets].use()
            return bullet
        return None
    
    def collision_info(self):
        '''añaden información una autoreferencia al body y el tipo de colision'''
        self.shape.body.data = self
        self.shape.collision_type = 2
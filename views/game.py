from conf import *
from sprites import *
from transformation import *
import pymunk
import random

MARGIN = 150

class Game(arcade.View):
    '''
    Vista del juego.
    Contiene la lógica del juego y generación del mapa.
    '''
    def __init__(self, players: int):
        super().__init__()
        arcade.set_background_color(COLOR_PRINCIPAL)
        self.players = players
        '''npumero de jugadores'''
        self.winner = 0
        '''ganador del juego'''

        self.texture = arcade.load_texture('img/bg_'+str(random.randint(1, 4))+'.png')
        '''textura del fondo'''

        # listas de sprites, los objetos son almacenados en la lista general de sprites
        self.tanks = arcade.SpriteList()
        self.sprites = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        
        self.tanks_sprite_info = [
            ( 'img/tank_r_s.png', MARGIN                  , MARGIN ),
            ( 'img/tank_b_s.png', SCREEN_WIDTH - MARGIN   , MARGIN if self.players > 2 else SCREEN_HEIGHT - MARGIN ),
            ( 'img/tank_y_s.png', MARGIN                  , SCREEN_HEIGHT - MARGIN ),
            ( 'img/tank_g_s.png', SCREEN_WIDTH - MARGIN   , SCREEN_HEIGHT - MARGIN )
            ]
        '''
        Lista de tuplas con información de los Tanks
            (imagen, center_x, center_y)
        '''
        
        self.space = pymunk.Space()
        '''espacio con pymunk'''
        self.space.damping = 0
        '''evitar que los onjetos se deslice luego de una colisión'''
        
        # añade los gestores de coliciones bullet/tank y bullet/object
        self.space.add_collision_handler(1, 2).begin = self.begin_collision_bullet_tank
        self.space.add_collision_handler(1, 3).begin = self.begin_collision_bullet_object

        # muros contenedores de la pantalla para que los tanks no escapen
        self.add_wall(0, 0, 0, SCREEN_HEIGHT) # left
        self.add_wall(0, 0, SCREEN_WIDTH, 0) # bottom
        self.add_wall(SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # right
        self.add_wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT) # top
        
        # usar los métodos de añadir rocas y arbustos random
        self.add_random_rocks(random.randint(2, 4))
        self.add_random_bushes(random.randint(5, 8))

        for i in range(players):
            # crea los jugadores, su body y shape
            image, center_x, center_y = self.tanks_sprite_info[i]
            player = Tank(image, 1, center_x, center_y, i+1)
            body, shape = player.make_shape(10, (45,45), 1, 1)
            self.space.add(body, shape)
            self.tanks.append(player)
            self.sprites.append(player)

            # añade una barricada de cajas alrededore de cada jugador
            self.add_barricade(
                center_x ,
                center_y ,
                1 if center_x == MARGIN else -1,
                1 if center_y == MARGIN else -1
                )
                
            # crea el panel de munición
            side = -1 if center_x == MARGIN else 1
            center_x = center_x + ( MARGIN -20 ) * side
            center_y += 30
            for m in range(5):
                munition = Munition(m, i, 90*side, center_x, center_y-15*m)
                self.sprites.append(munition)
                player.munition[m] = munition

    def add_wall(self, x1, y1, x2, y2):
        '''añade un muro contenedor entre dos puntos'''
        wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_shape = pymunk.Segment(wall_body, (x1, y1), (x2, y2), 5)
        wall_shape.friction = 1
        self.space.add(wall_body, wall_shape)
    
    def add_bullet(self, bullet):
        '''añade el shape y body al espacio y a las listas de sprites'''
        if bullet != None :
            self.space.add(bullet.shape.body, bullet.shape)
            self.bullets.append(bullet)
            self.sprites.append(bullet)
    
    def add_bush(self, x, y, angle):
        '''añade un arbusto en el mapa'''
        bush = Object('img/bush.png', 1, angle, x, y, destroyed_image='img/bush_destroyed.png')
        bush.make_shape_circle(2, 15, True, 1)
        self.space.add(bush.shape.body, bush.shape)
        self.sprites.append(bush)

    def add_rock(self, x, y, angle):
        '''añade una roca en el mapa'''
        rock = Object('img/rock.png', 1, angle, x, y, destructible=False)
        rock.make_shape_circle(2, 25, True)
        self.space.add(rock.shape.body, rock.shape)
        self.sprites.append(rock)
    
    def add_box(self, x, y, angle=0):
        '''a{ade una caja en el mapa'''
        box = Object('img/wood_box.png', 1, angle, x, y, destructible=False)
        box.make_shape_box(2, (50,50))
        self.space.add(box.shape.body, box.shape)
        self.sprites.append(box)

    def add_random_bushes(self, n=10):
        '''añade n arbustos en posiciones aleatorias*'''
        for i in range(n):
            x = random.randint(MARGIN*2, SCREEN_WIDTH-MARGIN*2)
            y = random.randint(0, SCREEN_HEIGHT)
            angle = random.randint(0, 7) * 45
            self.add_bush(x, y, angle)
    
    def add_random_rocks(self, n=10):
        '''añade n rocas en posiciones aleatorias*'''
        for i in range(n):
            x = random.randint(MARGIN*2, SCREEN_WIDTH-MARGIN*2)
            y = random.randint(0, SCREEN_HEIGHT)
            angle = random.randint(0, 7) * 45
            self.add_rock(x, y, angle)

    def add_barricade(self, center_x, center_y, side_x, side_y, space_between=70):
        '''añade una barricada dependiendo de la posición del tank (centro barricada)'''
        angle = 180 if side_x == -1 and side_y == -1 else -1*side_x*45 + side_y*45
        boxes_position = rotate(
            angle
            , [(
                    center_x - space_between,
                    center_y + space_between
                ), (
                    center_x,
                    center_y + space_between
                ), (
                    center_x + space_between,
                    center_y + space_between
                ), (
                    center_x + space_between,
                    center_y
                ), (
                    center_x + space_between,
                    center_y - space_between
                )],
            (center_x, center_y)
        )
        for b in boxes_position:
            self.add_box(b[0], b[1])
        
    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.texture
            )

        # dibuja los paneles de munición
        for i in range(self.players):
            image, center_x, center_y = self.tanks_sprite_info[i]
            side = 1 if center_x != MARGIN else -1
            center_x = center_x + MARGIN * side
            arcade.draw_rectangle_filled(center_x, center_y, 80, 100, COLOR_PLAYER[i+1])
        self.sprites.draw()
            
    def on_update(self, delta_time):
        self.space.step(1 / 60)
        self.sprites.update()
        # verifica si hay solo 1 o menos jugadores
        alive = 0
        for tank in self.tanks:
            if tank.alive : alive+=1
        if alive <= 1 :
            for i, tank in enumerate(self.tanks):
                if tank.alive : self.winner = i+1
            # pasa a la vista de ganador
            self.window.run_winner(self.winner, self.players)
    
    def on_key_press(self, symbol, modifiers):
        '''controles de los tanks - disparar y avanzar'''
        if symbol == arcade.key.Z :
            self.add_bullet(self.tanks[0].shoot())
            self.tanks[0].avanzar()
        if symbol == arcade.key.M :
            self.add_bullet(self.tanks[1].shoot())
            self.tanks[1].avanzar()
        if symbol == arcade.key.Q and self.players > 2 :
            self.add_bullet(self.tanks[2].shoot())
            self.tanks[2].avanzar()
        if symbol == arcade.key.P and self.players > 3 :
            self.add_bullet(self.tanks[3].shoot())
            self.tanks[3].avanzar()
    
    def on_key_release(self, symbol, modifiers):
        '''controles de los tanks - detener'''
        if symbol == arcade.key.Z : self.tanks[0].detener()
        if symbol == arcade.key.M : self.tanks[1].detener()
        if symbol == arcade.key.Q and self.players > 2: self.tanks[2].detener()
        if symbol == arcade.key.P and self.players > 3: self.tanks[3].detener()
    
    def begin_collision_bullet_tank(self, arbiter, space, data):
        '''Manejador de colisiones entre balas habilitadas (1) y tanks (2)'''
        bullet, tank = arbiter.shapes
        if bullet.collision_type == 2 and tank.collision_type == 1 :
            bullet, tank = tank, bullet
        
        bullet = bullet.body.data
        tank = tank.body.data

        if bullet.owner != tank.player :
            if tank.alive : tank.die()
            bullet.remove_from_sprite_lists()
            self.remove_shape(bullet)
        
        return True

    def begin_collision_bullet_object(self, arbiter, space, data):
        '''Manejador de colisiones entre balas habilitadas (1) y objetos (3)'''
        bullet, obj = arbiter.shapes
        if bullet.collision_type == 3 and obj.collision_type == 1 :
            bullet, obj = obj, bullet
        
        obj = obj.body.data
        bullet = bullet.body.data

        bullet.remove_from_sprite_lists()
        self.remove_shape(bullet)

        if obj.destructible :
            self.remove_shape(obj)
        obj.destroy()
        return True
    
    def remove_shape(self, sprite):
        '''remueve el body y shape del space'''
        if sprite.shape != None :
            self.space.remove(sprite.shape.body, sprite.shape)
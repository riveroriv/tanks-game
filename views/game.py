from conf import *
from sprites import *
from transformation import *
import pymunk
import random

MARGIN = 150

class Game(arcade.View):
    def __init__(self, players: int):
        super().__init__()
        arcade.set_background_color(COLOR_PRINCIPAL)
        self.players = players
        self.winner = 0

        self.texture = arcade.load_texture('img/bg_'+str(random.randint(1, 4))+'.png')

        self.tanks = arcade.SpriteList()
        self.sprites = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        
        self.tanks_sprite_info = [
            ( 'img/tank_r_s.png', MARGIN                  , MARGIN ),
            ( 'img/tank_b_s.png', SCREEN_WIDTH - MARGIN   , MARGIN if self.players > 2 else SCREEN_HEIGHT - MARGIN ),
            ( 'img/tank_y_s.png', MARGIN                  , SCREEN_HEIGHT - MARGIN ),
            ( 'img/tank_g_s.png', SCREEN_WIDTH - MARGIN   , SCREEN_HEIGHT - MARGIN )
            ]
        
        self.space = pymunk.Space()
        self.space.damping = 0
        
        handler_bullet_tank = self.space.add_collision_handler(1, 2)
        handler_bullet_tank.begin = self.begin_collision_bullet_tank

        handler_bullet_object = self.space.add_collision_handler(1, 3)
        handler_bullet_object.begin = self.begin_collision_bullet_object

        self.add_wall(0, 0, 0, SCREEN_HEIGHT) # left
        self.add_wall(0, 0, SCREEN_WIDTH, 0) # bottom
        self.add_wall(SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # right
        self.add_wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT) # top
        
        self.add_random_rocks(random.randint(2, 4))
        self.add_random_bushes(random.randint(5, 8))

        for i in range(players):
            image, center_x, center_y = self.tanks_sprite_info[i]
            player = Tank(image, 1, center_x, center_y, i+1)
            body, shape = player.make_shape(10, (45,45), 1, 1)
            self.space.add(body, shape)
            self.tanks.append(player)
            self.sprites.append(player)
            self.add_barricade(
                center_x ,
                center_y ,
                1 if center_x == MARGIN else -1,
                1 if center_y == MARGIN else -1
                )
                
            side = -1 if center_x == MARGIN else 1
            center_x = center_x + ( MARGIN -20 ) * side
            center_y += 30
            for m in range(5):
                munition = Munition(m, i, 90*side, center_x, center_y-15*m)
                self.sprites.append(munition)
                player.munition[m] = munition

    def add_wall(self, x1, y1, x2, y2):
        wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_shape = pymunk.Segment(wall_body, (x1, y1), (x2, y2), 5)
        wall_shape.friction = 1
        self.space.add(wall_body, wall_shape)
    
    def add_bullet(self, bullet):
        if bullet != None :
            self.space.add(bullet.shape.body, bullet.shape)
            self.bullets.append(bullet)
            self.sprites.append(bullet)
    
    def add_bush(self, x, y, angle):
        bush = Object('img/bush.png', 1, angle, x, y, fixed=True, destroyed_image='img/bush_destroyed.png')
        bush.make_shape_circle(2, 15, 0.3, 1)
        self.space.add(bush.shape.body, bush.shape)
        self.sprites.append(bush)

    def add_rock(self, x, y, angle):
        rock = Object('img/rock.png', 1, angle, x, y, fixed=True, destructible=False)
        rock.make_shape_circle(2, 25, 0.3, 1)
        self.space.add(rock.shape.body, rock.shape)
        self.sprites.append(rock)
    
    def add_box(self, x, y, angle=0):
        box = Object('img/wood_box.png', 1, angle, x, y, destructible=False)
        box.make_shape_box(2, (50,50))
        self.space.add(box.shape.body, box.shape)
        self.sprites.append(box)

    def add_random_bushes(self, n=10):
        for i in range(n):
            x = random.randint(MARGIN*2, SCREEN_WIDTH-MARGIN*2)
            y = random.randint(0, SCREEN_HEIGHT)
            angle = random.randint(0, 7) * 45
            self.add_bush(x, y, angle)
    
    def add_random_rocks(self, n=10):
        for i in range(n):
            x = random.randint(MARGIN*2, SCREEN_WIDTH-MARGIN*2)
            y = random.randint(0, SCREEN_HEIGHT)
            angle = random.randint(0, 7) * 45
            self.add_rock(x, y, angle)

    def add_barricade(self, center_x, center_y, side_x, side_y, space_between=70):
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
        for i in range(self.players):
            image, center_x, center_y = self.tanks_sprite_info[i]
            side = 1 if center_x != MARGIN else -1
            center_x = center_x + MARGIN * side
            arcade.draw_rectangle_filled(center_x, center_y, 80, 100, COLOR_PLAYER[i+1])
        self.sprites.draw()
            
    def on_update(self, delta_time):
        self.space.step(1 / 60)
        self.sprites.update()
        alive = 0
        for tank in self.tanks:
            if tank.alive : alive+=1
        if alive <= 1 :
            for i, tank in enumerate(self.tanks):
                if tank.alive : self.winner = i+1
            self.window.run_winner(self.winner, self.players)
    
    def on_key_press(self, symbol, modifiers):
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
        if symbol == arcade.key.Z : self.tanks[0].detener()
        if symbol == arcade.key.M : self.tanks[1].detener()
        if symbol == arcade.key.Q and self.players > 2: self.tanks[2].detener()
        if symbol == arcade.key.P and self.players > 3: self.tanks[3].detener()
    
    def begin_collision_bullet_tank(self, arbiter, space, data):
        bullet, tank = arbiter.shapes
        if bullet.collision_type == 2 and tank.collision_type == 1 :
            bullet, tank = tank, bullet
        
        bullet = bullet.body.data
        tank = tank.body.data

        if bullet.owner != tank.player :
            tank.die()
            bullet.remove_from_sprite_lists()
            
        return True

    def begin_collision_bullet_object(self, arbiter, space, data):
        bullet, obj = arbiter.shapes
        if bullet.collision_type == 3 and obj.collision_type == 1 :
            bullet, obj = obj, bullet
        bullet.body.data.remove_from_sprite_lists()
        obj = obj.body.data
        if obj.destructible :
            self.space.remove(obj.shape.body, obj.shape)
        obj.destroy()
        return True
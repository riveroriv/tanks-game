from conf import *
from sprites import *
import pymunk

class Game(arcade.View):
    def __init__(self, players: int):
        super().__init__()
        arcade.set_background_color(COLOR_PRINCIPAL)
        self.players = players
        self.winner = 0
        self.texture = arcade.load_texture('img/bg.png')

        self.tanks = arcade.SpriteList()
        self.sprites = arcade.SpriteList()
        self.bullets = arcade.SpriteList()
        
        margin = 100
        tanks = [
            ( 'img/tank_r.png', margin                  , margin ),
            ( 'img/tank_y.png', SCREEN_WIDTH - margin   , margin if self.players > 2 else SCREEN_HEIGHT - margin ),
            ( 'img/tank_g.png', margin                  , SCREEN_HEIGHT - margin ),
            ( 'img/tank_b.png', SCREEN_WIDTH - margin   , SCREEN_HEIGHT - margin )
            ]
        
        self.space = pymunk.Space()
        self.space.damping = 0

        self.add_wall(0, 0, 0, SCREEN_HEIGHT) # left
        self.add_wall(0, 0, SCREEN_WIDTH, 0) # bottom
        self.add_wall(SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT) # right
        self.add_wall(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT) # top

        for i in range(players):
            image, center_x, center_y = tanks[i]
            player = Tank(image, 0.3, center_x, center_y)
            body, shape = player.make_shape(10, (45,45), 1, 1)
            self.space.add(body, shape)
            self.tanks.append(player)
            self.sprites.append(player)
        
        self.add_objects()
    
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
    
    def add_bush(self, x, y):
        bush = Object('img/bush.png', 0.2, 0, x, y, True)
        bush.make_shape(2, (45,45), 0.3, 1)
        self.space.add(bush.shape.body, bush.shape)
        self.sprites.append(bush)
    
    def add_box(self, x, y):
        box = Object('img/wood_box.png', 0.04, 0, x, y)
        box.make_shape(2, (45,45))
        self.space.add(box.shape.body, box.shape)
        self.sprites.append(box)

    def add_objects(self):
        self.add_box(400,400)
        self.add_bush(500,500)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.texture
            )
        self.sprites.draw()
    
    def on_update(self, delta_time):
        self.space.step(1 / 60)
        self.sprites.update()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Z :
            self.tanks[0].avanzar()
            self.tanks[0].die()
            self.add_bullet(self.tanks[0].shoot())
        if symbol == arcade.key.M :
            self.tanks[1].avanzar()
            self.add_bullet(self.tanks[1].shoot())
        if symbol == arcade.key.Q and self.players > 2 :
            self.tanks[2].avanzar()
            self.add_bullet(self.tanks[2].shoot())
        if symbol == arcade.key.P and self.players > 3 :
            self.tanks[3].avanzar()
            self.add_bullet(self.tanks[3].shoot())
    
    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.Z : self.tanks[0].detener()
        if symbol == arcade.key.M : self.tanks[1].detener()
        if symbol == arcade.key.Q and self.players > 2: self.tanks[2].detener()
        if symbol == arcade.key.P and self.players > 3: self.tanks[3].detener()
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.run_winner(self.winner, self.players)
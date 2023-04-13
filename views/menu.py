from conf import *
from sprites import *

class Menu(arcade.View):
    def __init__(self, players: int):
        super().__init__()
        arcade.set_background_color(COLOR_PRINCIPAL)
        self.players = players
        self.title_speed = 0.15
        self.title_delta_y = 10
        
        self.tanks_positions = {
            2: [-100, 100, 0, 0],
            3: [-200, 0, 200, 0],
            4: [-300, -100, 100, 300],
        }
        self.tanks = [
            Tank('img/tank_r.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2),
            Tank('img/tank_b.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2),
            Tank('img/tank_y.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2),
            Tank('img/tank_g.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2)
            ]
        
        self.left = COLOR_BLANCO
        self.right = COLOR_BLANCO

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            self.players,
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1 / 8 ,
            arcade.color.WHITE, 80,
            font_name='Franklin Gothic Heavy', anchor_x='center'
            )
        arcade.draw_text(
            'players',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.5 / 8 ,
            arcade.color.WHITE, 30,
            font_name='Franklin Gothic Heavy', anchor_x='center'
            )
        arcade.draw_text(
            'Tanks!',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 6 / 8 ,
            arcade.color.BLACK, 100,
            font_name='Franklin Gothic Heavy', anchor_x='center'
            )
        arcade.draw_text(
            'Tanks!',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 6 / 8 + self.title_delta_y,
            arcade.color.WHITE, 100,
            font_name='Franklin Gothic Heavy', anchor_x='center'
            )
        arcade.draw_text(
            '[ space to start ]',
            SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5.5 / 8 ,
            arcade.color.WHITE, 20,
            font_name='Franklin Gothic Heavy', anchor_x='center'
            )
        dif = 120
        arcade.draw_triangle_filled(
            SCREEN_WIDTH / 2 - dif,
            SCREEN_HEIGHT * 1 / 8,
            SCREEN_WIDTH / 2 - dif,
            SCREEN_HEIGHT * 2 / 8,
            SCREEN_WIDTH / 2 - 50 - dif,
            SCREEN_HEIGHT * 1.5 / 8,
            self.left
        )
        arcade.draw_triangle_filled(
            SCREEN_WIDTH / 2 + dif,
            SCREEN_HEIGHT * 1 / 8,
            SCREEN_WIDTH / 2 + dif,
            SCREEN_HEIGHT * 2 / 8,
            SCREEN_WIDTH / 2 + 50 + dif,
            SCREEN_HEIGHT * 1.5 / 8,
            self.right
        )
        for tank in self.tanks[:self.players] : tank.draw()
    
    def on_update(self, delta_time):
        if self.title_delta_y > 20 or self.title_delta_y < 10:
            self.title_speed *=-1
        self.title_delta_y += self.title_speed
        
        for i, tank in enumerate(self.tanks):
            tank.center_x = (SCREEN_WIDTH/2) + self.tanks_positions[self.players][i]
        
        if self.players == 4 : self.right = COLOR_PRINCIPAL
        else : self.right = COLOR_BLANCO
        
        if self.players == 2 : self.left = COLOR_PRINCIPAL
        else : self.left = COLOR_BLANCO
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.RIGHT :
            if self.players < 4 : self.players += 1
        
        if symbol == arcade.key.LEFT :
            if self.players > 2 : self.players -= 1
        
        if symbol == arcade.key.SPACE or symbol == arcade.key.ENTER :
            self.window.run_game(self.players)
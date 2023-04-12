import arcade
import math
from sprites import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Tanks'

SCALING = 0.5
SPEED = 5
BULLET_SPEED = 15

COLOR_PRINCIPAL = arcade.color_from_hex_string('4c2a90')
COLOR_RESALTAR = arcade.color_from_hex_string('892BAA')
COLOR_BLANCO = arcade.color_from_hex_string('fff')

COLOR_PLAYER_1 = arcade.color_from_hex_string('f1421c')
COLOR_PLAYER_2 = arcade.color_from_hex_string('5383ea')
COLOR_PLAYER_3 = arcade.color_from_hex_string('face27')
COLOR_PLAYER_4 = arcade.color_from_hex_string('51d21e')

COLOR_PLAYER = {
    1: COLOR_PLAYER_1, #rojo
    2: COLOR_PLAYER_2, #azul
    3: COLOR_PLAYER_3, #amarillo
    4: COLOR_PLAYER_4 #verde
}

FONT_DIR = 'font/FGR.ttf'
FONT_NAME = 'Franklin Gothic Heavy'


class App(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.font = arcade.load_font(FONT_DIR)

        #menu_view = Menu()
        menu_view = Winner(1)
        self.show_view(menu_view)
        
        '''
        self.player = Tank('img/tank.png', 0.05, center_x=SCREEN_WIDTH/2, center_y=SCREEN_HEIGHT/2)
        self.background = arcade.load_texture('img/bg.jpg')
        '''


'''
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH/2,
            SCREEN_HEIGHT/2,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background
            )
        self.player.draw()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.M :
            self.player.avanzar()
    
    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.M :
            self.player.detener()

    def on_update(self, delta_time: float):
        self.player.update()
'''
class Menu(arcade.View):
    def __init__(self, players=2):
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
            next_view = Game(self.players)
            next_view.setup()
            self.window.show_view(next_view)

class Game(arcade.View):
    def __init__(self, players=2):
        super().__init__()
        self.players = players
    
    def setup(self):
        ''' This should set up your game and get it ready to play '''
        # Replace 'pass' with the code to set up your game
        pass
    
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text('Game', SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                        arcade.color.BLACK, font_size=30, anchor_x='center')

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        next_view = Winner(3, self.players)
        self.window.show_view(next_view)

class Winner(arcade.View):
    def __init__(self, winner: int, players=2):
        super().__init__()
        self.winner = winner
        self.players = players
        arcade.set_background_color(COLOR_PLAYER.get(self.winner, arcade.color.WHITE))
        self.imagen = arcade.load_texture('img/winner.png')

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            'PLAYER '+str(self.winner),
            30, SCREEN_HEIGHT - 120,
            arcade.color.WHITE, 100,
            font_name='Franklin Gothic Heavy'
            )
        arcade.draw_text(
            'WINS ',
            40, SCREEN_HEIGHT - 280,
            arcade.color.WHITE, 160,
            font_name='Franklin Gothic Heavy'
            )
        arcade.draw_text(
            '[ space to menu ] ',
            SCREEN_WIDTH*3/4, 50,
            arcade.color.WHITE, 20,
            font_name='Franklin Gothic Heavy'
            )
        arcade.draw_texture_rectangle(
            SCREEN_WIDTH/4 + 80,
            SCREEN_HEIGHT/4 + 50,
            SCREEN_WIDTH*3/5,
            SCREEN_HEIGHT*3/5,
            self.imagen
            )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE or symbol == arcade.key.ENTER :
            next_view = Menu(self.players)
            self.window.show_view(next_view)

if __name__ == '__main__':
    app = App()
    arcade.run()
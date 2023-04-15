from conf import *
from sprites import *

class Menu(arcade.View):
    '''
    Primet vista del juego.

    Tiene el título, la función de seleccionar
    el número de jugadores y de pasar a la siguiente pantalla
    '''

    def __init__(self, players: int):
        super().__init__()
        arcade.set_background_color(COLOR_PRINCIPAL)
        self.players = players
        '''número de jugadores'''
        self.title_speed = 0.15
        '''velocidad de movimiento del título'''
        self.title_delta_y = 10
        '''cuánto avanza el título'''

        self.tanks_positions = {
            2: [-100, 100, 0, 0],
            3: [-200, 0, 200, 0],
            4: [-300, -100, 100, 300],
        }
        '''posiciones de los Tanks cuando hay 2,3,4 jugadores'''
        self.tanks = [
            Tank('img/tank_r_b.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2 - 20),
            Tank('img/tank_b_b.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2 - 20),
            Tank('img/tank_y_b.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2 - 20),
            Tank('img/tank_g_b.png', 1, center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2 - 20)
            ]
        '''sprites de Tanks por defecto'''
        self.left = COLOR_BLANCO
        '''color flecha izquierda'''
        self.right = COLOR_BLANCO
        '''color dlecha derecha'''

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
        # flecha izquierda
        arcade.draw_triangle_filled(
            SCREEN_WIDTH / 2 - dif,
            SCREEN_HEIGHT * 1 / 8,
            SCREEN_WIDTH / 2 - dif,
            SCREEN_HEIGHT * 2 / 8,
            SCREEN_WIDTH / 2 - 50 - dif,
            SCREEN_HEIGHT * 1.5 / 8,
            self.left
        )
        # flecha derecha
        arcade.draw_triangle_filled(
            SCREEN_WIDTH / 2 + dif,
            SCREEN_HEIGHT * 1 / 8,
            SCREEN_WIDTH / 2 + dif,
            SCREEN_HEIGHT * 2 / 8,
            SCREEN_WIDTH / 2 + 50 + dif,
            SCREEN_HEIGHT * 1.5 / 8,
            self.right
        )
        # dibuja tanques según la cantidad de jugadores seleccionada
        for tank in self.tanks[:self.players] : tank.draw()
    
    def on_update(self, delta_time):
        # mueve el título
        if self.title_delta_y > 20 or self.title_delta_y < 10:
            self.title_speed *=-1
        self.title_delta_y += self.title_speed
        
        # actualiza la posición por si se aumenta o reduce jugadores
        for i, tank in enumerate(self.tanks):
            tank.center_x = (SCREEN_WIDTH/2) + self.tanks_positions[self.players][i]
        
        # camufla flecha derecha, máximo jugadores
        if self.players == 4 : self.right = COLOR_PRINCIPAL
        else : self.right = COLOR_BLANCO
        
        #camufla flecha izquierda, mínimo jugaodres
        if self.players == 2 : self.left = COLOR_PRINCIPAL
        else : self.left = COLOR_BLANCO
    
    def on_key_press(self, symbol, modifiers):
        # aumenta jugador
        if symbol == arcade.key.RIGHT :
            if self.players < 4 : self.players += 1
        
        # reduce jugador
        if symbol == arcade.key.LEFT :
            if self.players > 2 : self.players -= 1
        
        # cambia a la vista de juego
        if symbol == arcade.key.SPACE or symbol == arcade.key.ENTER :
            self.window.run_game(self.players)
from conf import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

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
            self.window.run_menu(self.players)
            #next_view = Menu(self.players)
            #self.window.show_view(next_view)
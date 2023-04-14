from conf import *

class Winner(arcade.View):
    def __init__(self, winner: int, players: int):
        super().__init__()
        self.winner = winner
        self.players = players
        self.imagen = arcade.load_texture('img/winner.png')
        arcade.set_background_color(COLOR_PLAYER.get(self.winner, arcade.color.WHITE))

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            'PLAYER '+str(self.winner),
            30, SCREEN_HEIGHT - 120,
            arcade.color.WHITE, 100,
            font_name='Franklin Gothic Heavy'
            )
        arcade.draw_text(
            'WINS' if self.winner != 0 else "DRAW",
            40, SCREEN_HEIGHT - 280,
            arcade.color.WHITE if self.winner != 0 else arcade.color.BLACK,
            160,
            font_name='Franklin Gothic Heavy'
            )
        arcade.draw_text(
            '[ space to menu ] ',
            SCREEN_WIDTH*3/4, 50,
            arcade.color.WHITE if self.winner != 0 else arcade.color.BLACK,
            20,
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
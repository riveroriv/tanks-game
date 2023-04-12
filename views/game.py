from conf import *

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
        #next_view = Winner(3, self.players)
        #self.window.show_view(next_view)
        self.window.run_winner(3, self.players)
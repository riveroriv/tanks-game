from conf import *
from views import *
from sprites import *

class App(arcade.Window):
    '''
    Clase que crea la ventana del juego, tiene funciones para cambiar las
    vistas y que ho haya importaciones circulares en las Views.

    Aquí se pueden añadir acciones comunes a todas las vistas como ser
    salir del juego si se presiona ESC.
    '''
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.font = arcade.load_font(FONT_DIR)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE :
            self.close()

    def run_menu(self, players=2):
        view = Menu(players)
        self.show_view(view)
    
    def run_game(self, players=2):
        view = Game(players)
        self.show_view(view)
    
    def run_winner(self, winner, players=2):
        view = Winner(winner, players)
        self.show_view(view)
    
    def run(self):
        self.run_menu()
        arcade.run()

if __name__ == '__main__':
    app = App()
    app.run()
import arcade
import math

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Tanks'

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

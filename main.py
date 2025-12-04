from pico2d import *
import game_framework
import play_mode as start_mode
import map_editor_mode as map_editor_mode

open_canvas(1980, 1080)
game_framework.run(start_mode)
close_canvas()
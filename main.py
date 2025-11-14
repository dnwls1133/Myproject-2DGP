from pico2d import *
import game_framework
import map_editor_mode as start_mode


open_canvas(1080, 960)
game_framework.run(start_mode)
close_canvas()
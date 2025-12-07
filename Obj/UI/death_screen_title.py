import game_framework

from pico2d import *




class DeathScreenTitle:
    def __init__(self):

        self.x,self.y = game_framework.camera_manager.get_window_size()


        self.img = load_image('sprites/UI/Death/Sprite/death_sreen_title.png')
    def update(self):
        pass







    def draw(self):
        draw_width = int(self.img.w * 3.0 )
        draw_height = int(self.img.h * 3.0)

        self.img.clip_draw(0,0,self.img.w,self.img.h,self.x,self.y,draw_width,draw_height)


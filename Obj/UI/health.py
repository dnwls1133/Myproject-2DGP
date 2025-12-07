import game_framework
from machine.animation import Animation
from pico2d import *
import common
import game_world



class Health:
    def __init__(self,x,y,index,owner):

        self.x,self.y = game_framework.camera_manager.get_window_size()
        self.index = index
        self.img = load_image('sprites/UI/health.png')
        self.x = x + 70 + self.img.w * index
        self.y = y + 10
        self.owner = owner
    def update(self):
        if self.owner.hp < self.index:
            game_world.remove_object(self)







    def draw(self):
        draw_width = int(self.img.w * 3.0 )
        draw_height = int(self.img.h * 3.0)

        self.img.clip_draw(0,0,self.img.w,self.img.h,self.x,self.y,draw_width,draw_height)


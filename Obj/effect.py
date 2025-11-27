from pico2d import *
import game_framework
import game_world

class Effect:
    def __init__(self,x,y,animation_name,anim_manager,delay=0.1,scale=1.0):
        self.x = x
        self.y = y
        self.scale = scale

        # 애니메이션 로드
        anim_data = anim_manager.get_anim_data(animation_name)
        from machine.animation import Animation
        self.animation = Animation(anim_data)
        self.animation.set_delay(delay)

        self.is_finished = False


    def update(self):
        self.animation.update()

        # 애니메이션 종료 체크
        if self.animation.is_animation_end():
            self.is_finished = True
            game_world.remove_object(self)

    def draw(self):
        if not self.is_finished:
            self.animation.draw(self.x,self.y,self.scale)
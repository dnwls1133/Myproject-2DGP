import game_framework
from machine.animation import Animation







class Crisanta:
    def __init__(self,anim_manager):

        self.x,self.y = game_framework.camera_manager.get_window_size()
        self.x /= 2
        self.y /= 2
        self.x -= 300


        anim_names = [
            'main_menu_crisanta']
        # 딕셔너리로 애니메이션 관리
        self.animations = {}

        for name in anim_names:
            anim_data = anim_manager.get_animation(name)
            if anim_data is None:
                raise ValueError(f"Animation '{name}' not found in AnimationManager.")
                return
            self.animations[name] = Animation(anim_data)

        self.current_animation = self.animations['main_menu_crisanta']
        self.current_animation.set_delay(0.2)  # 프레임 지연 시간 설정






    def set_animation(self, name):
        """ 애니메이션 변경"""
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.current_frame = 0
            self.current_animation.frame_time = 0








    def update(self):
        if self.current_animation:
            self.current_animation.update()






    def draw(self):
        if self.current_animation:
            self.current_animation.draw(self.x, self.y,scale = 3.0)

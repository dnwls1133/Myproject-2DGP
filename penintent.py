from machine.animation import Animation



class Penintent:
    def __init__(self, anim_manager):
        self.x, self.y = 400,200

        # 애니메이션 이름 리스트
        anim_names = [
            'idle', 'attack', 'run', 'start_run', 'stop_run',
            'crouch', 'crouch_up', 'dodge', 'falling_over',
            'getting_up', 'parry_failed', 'parry_success'
        ]

        # 딕셔너리로 애니메이션 관리
        self.animations = {}

        for name in anim_names:
            anim_data = anim_manager.get_animation(name)
            if anim_data is None:
                raise ValueError(f"Animation '{name}' not found in AnimationManager.")
                return
            self.animations[name] = Animation(anim_data)


        self.current_animation = self.animations['idle']

    def set_animation(self,name):
        """ 애니메이션 변경"""
        if name in self.animations:
            self.current_animation = self.animations[name]

    def update(self):
        if self.current_animation:
            self.current_animation.update()



    def draw(self):
        if self.current_animation:
            self.current_animation.draw(self.x,self.y)

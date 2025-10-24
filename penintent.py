from animation import Animation



class Penintent:
    def __init__(self, anim_manager):
        self.x, self.y = 400,200

        # None 체크 추가
        idle_data = anim_manager.get_animation('idle')
        attack_data = anim_manager.get_animation('attack')
        run_data = anim_manager.get_animation('run')
        start_run_data = anim_manager.get_animation('start_run')
        stop_run_data = anim_manager.get_animation('stop_run')
        crouch_data = anim_manager.get_animation('crouch')
        crouch_up_data = anim_manager.get_animation('crouch_up')
        dodge_data = anim_manager.get_animation('dodge')
        falling_over_data = anim_manager.get_animation('falling_over')
        getting_up_data = anim_manager.get_animation('getting_up')
        parry_failed_data = anim_manager.get_animation('parry_failed')
        parry_success_data = anim_manager.get_animation('parry_success')
        elder_jump_data = anim_manager.get_animation('elder_boss_jump')


         # None 체크 추가


        if idle_data is None or attack_data is None or run_data is None or start_run_data is None or stop_run_data is None or crouch_data is None or crouch_up_data is None or dodge_data is None or falling_over_data is None or getting_up_data is None or parry_failed_data is None or parry_success_data is None:
            print("애니메이션 데이터가 없습니다!")
            # 기본값 설정으로 오류 방지
            self.idle_animation = None
            self.attack_animation = None
            self.current_animation = None
            self.run_animation = None
            self.start_run_animation = None
            self.stop_run_animation = None
            self.crouch_animation = None
            self.crouch_up_animation = None
            self.dodge_animation = None
            self.falling_over_animation = None
            self.getting_up_animation = None
            self.parry_failed_animation = None
            self.parry_success_animation = None
            self.elder_boss_jump_animation = None
            return

        self.idle_animation = Animation(idle_data)
        self.attack_animation = Animation(attack_data)
        self.run_animation = Animation(run_data)
        self.start_run_animation = Animation(start_run_data)
        self.stop_run_animation = Animation(stop_run_data)
        self.crouch_animation = Animation(crouch_data)
        self.crouch_up_animation = Animation(crouch_up_data)
        self.dodge_animation = Animation(dodge_data)
        self.falling_over_animation = Animation(falling_over_data)
        self.getting_up_animation = Animation(getting_up_data)
        self.parry_failed_animation = Animation(parry_failed_data)
        self.parry_success_animation = Animation(parry_success_data)
        self.elder_boss_jump_animation = Animation(elder_jump_data)
        self.current_animation = self.elder_boss_jump_animation

    def update(self):
        if self.current_animation:
            self.current_animation.update(0.005)



    def draw(self):
        if self.current_animation:
            self.current_animation.draw(self.x,self.y)

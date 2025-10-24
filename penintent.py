from animation import Animation



class Penintent:
    def __init__(self, anim_manager):
        self.x, self.y = 400,200

        # None 체크 추가
        idle_data = anim_manager.get_animation('idle')
        attack_data = anim_manager.get_animation('attack')

        if idle_data is None or attack_data is None:
            print("애니메이션 데이터가 없습니다!")
            # 기본값 설정으로 오류 방지
            self.idle_animation = None
            self.attack_animation = None
            self.current_animation = None
            return

        self.idle_animation = Animation(idle_data)
        self.attack_animation = Animation(attack_data)
        self.current_animation = self.idle_animation

    def update(self):
        if self.current_animation:
            self.current_animation.update(0.005)

    def draw(self):
        if self.current_animation:
            self.current_animation.draw(self.x,self.y)

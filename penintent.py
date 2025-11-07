import game_framework
from machine.animation import Animation
from machine.state_machine import StateMachine
from sdl2 import *
import machine.events





class Idle:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        self.penintent.face_dir = 1

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Attack:
    pass
class Run:
    pass
class Start_Run:
    pass
class Stop_Run:
    pass
class Crouch:
    pass
class Crouch_Up:
    pass
class Dodge:
    pass
class Falling_Over:
    pass
class Getting_Up:
    pass
class Parry_Failed:
    pass
class Parry_Success:
    pass

class Penintent:
    def __init__(self, anim_manager):
        # 애니메이션 이름 리스트
        anim_names = [
            'idle', 'attack', 'run', 'start_run', 'stop_run',
            'crouch', 'crouch_up', 'dodge', 'falling_over',
            'getting_up', 'parry_failed', 'parry_success'
        ]

        self.x, self.y = 400,200
        self.face_dir = 1
        # 물리 속성
        self.vx = 0
        self.vy = 0

        self.on_ground = False

        # 물리 상수
        self.gravity = -800.0  # 중력 가속도
        self.max_fall_speed = -1000.0  # 최대 낙하 속도
        self.friction = 0.8  # 마찰 계수

        # 이동 상수
        self.move_speed = 300.0  # 이동 속도
        self.jump_speed = 500.0  # 점프 속도



        # 딕셔너리로 애니메이션 관리
        self.animations = {}

        for name in anim_names:
            anim_data = anim_manager.get_animation(name)
            if anim_data is None:
                raise ValueError(f"Animation '{name}' not found in AnimationManager.")
                return
            self.animations[name] = Animation(anim_data)


        self.current_animation = self.animations['idle']

        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.RUN = Run(self)
        self.START_RUN = Start_Run(self)
        self.STOP_RUN = Stop_Run(self)
        self.CROUCH = Crouch(self)
        self.CROUCH_UP = Crouch_Up(self)
        self.DODGE = Dodge(self)
        self.FALLING_OVER = Falling_Over(self)
        self.GETTING_UP = Getting_Up(self)
        self.PARRY_FAILED = Parry_Failed(self)
        self.PARRY_SUCCESS = Parry_Success(self)


        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {},
                self.RUN: {}
            }
        )


    def set_animation(self,name):
        """ 애니메이션 변경"""
        if name in self.animations:
            self.current_animation = self.animations[name]

    def handle_input(self):
        pass

    def update(self):
        self.state_machine.update()
        #self.handle_input()

        # dt = game_framework.time_manager.get_fixed_dt()
        # # 1. 중력 적용
        # self.vy += self.gravity * dt
        #
        # # 2. 최대 낙하 속도 제한
        # if self.vy < self.max_fall_speed:
        #     self.vy = self.max_fall_speed
        #
        # if self.on_ground:
        #     # 3. 지면에 있을 때 마찰 적용
        #     self.vx *= self.friction
        # # 4. 속도가 너무 작으면 0으로 설정
        # if abs(self.vx) < 1:
        #         self.vx = 0
        # # 5. 위치 업데이트 (dt 적용!)
        # self.x += self.vx * dt
        # self.y += self.vy * dt
        #
        # # 6. 임시 바닥 충돌
        # ground_y = 100
        # if self.y <= ground_y:
        #     self.y = ground_y
        #     self.vy = 0
        #     self.on_ground = True
        # else:
        #     self.on_ground = False
        #
        # if self.current_animation:
        #     self.current_animation.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if self.current_animation:
            self.current_animation.draw(self.x,self.y)

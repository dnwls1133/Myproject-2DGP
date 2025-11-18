import game_framework
from machine.animation import Animation
from machine.state_machine import StateMachine
from sdl2 import *
from machine import events
from collider import Collider
import math
import random



class Idle:
    def __init__(self, elder_brother):
        self.elder_brother = elder_brother

    def enter(self, e):

        self.elder_brother.vx = 0
        self.elder_brother.set_animation('elder_brother_death')
        self.elder_brother.current_animation.set_delay(0.1)
        if self.elder_brother.face_dir == 1:
            self.elder_brother.current_animation.set_flip('')
        else:
            self.elder_brother.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.elder_brother.current_animation:
            self.elder_brother.current_animation.update()

        # 물리 처리
        dt = game_framework.time_manager.get_fixed_dt()

        # 바닥 체크
        char_bottom = self.elder_brother.y - self.elder_brother.collider.height / 2

        if char_bottom > self.elder_brother.ground:
            # 공중에 있을 때 중력 적용
            self.elder_brother.vy += self.elder_brother.gravity * dt
            if self.elder_brother.vy < self.elder_brother.max_fall_speed:
                self.elder_brother.vy = self.elder_brother.max_fall_speed
            self.elder_brother.is_grounded = False
        else:
            # 바닥에 닿았을 때
            self.elder_brother.y = self.elder_brother.ground + self.elder_brother.collider.height / 2
            self.elder_brother.vy = 0
            self.elder_brother.is_grounded = True

        # 위치 업데이트
        self.elder_brother.y += self.elder_brother.vy * dt

    def draw(self):
        if self.elder_brother.current_animation:
            self.elder_brother.current_animation.draw(self.elder_brother.x, self.elder_brother.y)
    pass

class ElderBrother:
    def __init__(self,anim_manager):

        self.collider = Collider(self, offset_x=0, offset_y=0, width=159, height=171)


        anim_names = ['elder_brother_idle',
                      'elder_brother_attack',
                      'elder_brother_jump',
                      'elder_brother_death']
        self.x, self.y = 800, 500
        self.face_dir = 1
        # 물리 속성
        self.vx = 0
        self.vy = 0

        self.on_ground = False
        self.ground = 100
        # 물리 상수
        self.gravity = -1233.0  # 중력 가속도
        self.max_fall_speed = -1000.0  # 최대 낙하 속도
        self.friction = 0.8  # 마찰 계수

        # 이동 상수
        self.move_speed = 250.0  # 이동 속도
        self.jump_speed = 600.0  # 점프 속도

        # 딕셔너리로 애니메이션 관리
        self.animations = {}

        for name in anim_names:
            anim_data = anim_manager.get_animation(name)
            if anim_data is None:
                raise ValueError(f"Animation '{name}' not found in AnimationManager.")
                return
            self.animations[name] = Animation(anim_data)

        self.current_animation = self.animations['elder_brother_idle']

        self.IDLE = Idle(self)


        self.state_machine = StateMachine(
            self.IDLE,{
                self.IDLE : {events.animation_end : self.IDLE}
            }
        )

    def set_animation(self, name):
        """ 애니메이션 변경"""
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.current_frame = 0
            self.current_animation.frame_time = 0




    def update(self):
        # 키 입력을 이벤트로 변환
        for event in game_framework.key_manager.get_pressed_events():
            self.state_machine.handle_state_event(('INPUT', event))

        for event in game_framework.key_manager.get_released_events():
            self.state_machine.handle_state_event(('INPUT', event))

        # 상태 머신 업데이트 - 각 상태의 do()에서 물리 처리가 실행됨
        self.state_machine.update()


    def draw(self):
        self.state_machine.draw()
        if self.current_animation:
            self.current_animation.draw(self.x, self.y)
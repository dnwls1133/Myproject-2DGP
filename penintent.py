import game_framework
from machine.animation import Animation
from machine.state_machine import StateMachine
from sdl2 import *
from machine import events





class Idle:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

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
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('attack')
        self.penintent.current_animation.set_stop_point(10)

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                self.penintent.state_machine.handle_state_event(('ANIMATION_END',None))

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Run:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('run')
        self.penintent.vx = self.penintent.move_speed
        if events.d_down(e) or events.a_up(e):
            self.penintent.face_dir = 1
            self.penintent.vx = self.penintent.move_speed
        elif events.a_down(e) or events.d_up(e):
            self.penintent.face_dir = -1
            self.penintent.face_dir = -1 * 5
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        dt = game_framework.time_manager.get_fixed_dt()
        # 1. 중력 적용
        self.penintent.vy += self.penintent.gravity * dt

        # 2. 최대 낙하 속도 제한
        if self.penintent.vy < self.penintent.max_fall_speed:
            self.penintent.vy = self.penintent.max_fall_speed

        # if self.penintent.on_ground:
        #     # 3. 지면에 있을 때 마찰 적용
        #     self.penintent.vx *= self.penintent.friction
        # 4. 속도가 너무 작으면 0으로 설정
        if abs(self.penintent.vx) < 1:
            self.penintent.vx = 0
        # 5. 위치 업데이트 (dt 적용!)
        self.penintent.x += self.penintent.vx * dt
        self.penintent.y += self.penintent.vy * dt

        # 6. 임시 바닥 충돌
        ground_y = 100
        if self.penintent.y <= ground_y:
            self.penintent.y = ground_y
            self.penintent.vy = 0
            self.penintent.on_ground = True
        else:
            self.penintent.on_ground = False

        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass

class Start_Run:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('start_run')
        self.penintent.vx = self.penintent.move_speed
        if events.d_down(e) or events.a_up(e):
            if self.penintent.face_dir == -1:
                self.penintent.current_animation.set_offset(-20,0)
            self.penintent.face_dir = 1

        elif events.a_down(e) or events.d_up(e):
            if self.penintent.face_dir == 1:
                self.penintent.current_animation.set_offset(20,0)
            self.penintent.face_dir = -1

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):

        dt = game_framework.time_manager.get_fixed_dt()
        # 1. 중력 적용
        self.penintent.vy += self.penintent.gravity * dt

        # 2. 최대 낙하 속도 제한
        if self.penintent.vy < self.penintent.max_fall_speed:
            self.penintent.vy = self.penintent.max_fall_speed

        # if self.penintent.on_ground:
        #     # 3. 지면에 있을 때 마찰 적용
        #     self.penintent.vx *= self.penintent.friction
        # 4. 속도가 너무 작으면 0으로 설정
        if abs(self.penintent.vx) < 1:
                self.penintent.vx = 0
        # 5. 위치 업데이트 (dt 적용!)
        self.penintent.x += self.penintent.vx * dt
        self.penintent.y += self.penintent.vy * dt

        # 6. 임시 바닥 충돌
        ground_y = 100
        if self.penintent.y <= ground_y:
            self.penintent.y = ground_y
            self.penintent.vy = 0
            self.penintent.on_ground = True
        else:
            self.penintent.on_ground = False

        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                self.penintent.state_machine.handle_state_event(('ANIMATION_END',None))

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Stop_Run:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('stop_run')

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                self.penintent.state_machine.handle_state_event(('ANIMATION_END',None))

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Crouch:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Crouch_Up:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Dodge:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        self.penintent.current_animation.set_stop_point(5)
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        self.penintent.current_animation.reset_stop_point()
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass

class Falling_Over:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Getting_Up:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Parry_Failed:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Parry_Success:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass

class Jump:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('idle')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass


class Penintent:
    def __init__(self, anim_manager):
        # 애니메이션 이름 리스트
        anim_names = [
            'idle', 'attack', 'run', 'start_run', 'stop_run',
            'crouch', 'crouch_up', 'dodge', 'falling_over',
            'getting_up', 'parry_failed', 'parry_success'
        ]

        self.x, self.y = 400,100
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
        self.JUMP = Jump(self)


        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {events.a_down: self.START_RUN, events.d_down: self.START_RUN, events.a_up: self.START_RUN, events.d_up: self.START_RUN,
                            events.s_down: self.CROUCH, events.space_down: self.JUMP, events.k_down: self.ATTACK},
                self.START_RUN: {events.animation_end: self.RUN, events.s_down: self.CROUCH, events.space_down: self.JUMP,
                                 events.k_down: self.ATTACK,events.a_up: self.STOP_RUN, events.d_up:self.STOP_RUN},
                self.RUN: {events.space_down: self.JUMP , events.a_up : self.STOP_RUN, events.d_up: self.STOP_RUN,
                           events.s_down: self.CROUCH, events.a_down: self.STOP_RUN, events.d_down: self.STOP_RUN,
                           events.k_down: self.ATTACK},
                self.STOP_RUN: {events.animation_end: self.IDLE, events.s_down: self.CROUCH},
                self.ATTACK: {events.animation_end: self.IDLE},
                self.CROUCH: {events.s_up: self.CROUCH_UP},
                self.CROUCH_UP: {events.animation_end: self.IDLE},
                self.JUMP: {events.animation_end: self.IDLE}
            }
        )


    def set_animation(self,name):
        """ 애니메이션 변경"""
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.current_frame = 0
            self.current_animation.frame_time = 0

    def handle_input(self):
        pass

    def update(self):

        # 키 입력을 이벤트로 변환
        # SDL 이벤트 객체를 직접 전달
        for event in game_framework.key_manager.get_pressed_events():
            self.state_machine.handle_state_event(('INPUT', event))

        for event in game_framework.key_manager.get_released_events():
            self.state_machine.handle_state_event(('INPUT', event))

        self.state_machine.update()
        game_framework.camera_manager.set_position(self.x, self.y)



        # if self.current_animation:
        #     self.current_animation.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        if self.current_animation:
            self.current_animation.draw(self.x,self.y)

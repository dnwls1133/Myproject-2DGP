import game_framework
from machine.animation import Animation
from machine.state_machine import StateMachine
from sdl2 import *
from machine import events
from collider import Collider




class Idle:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):

        self.penintent.vx = 0
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

        # 물리 처리
        dt = game_framework.time_manager.get_fixed_dt()

        # 바닥 체크
        char_bottom = self.penintent.y - self.penintent.collider.height / 2

        if char_bottom > self.penintent.ground:
            # 공중에 있을 때 중력 적용
            self.penintent.vy += self.penintent.gravity * dt
            if self.penintent.vy < self.penintent.max_fall_speed:
                self.penintent.vy = self.penintent.max_fall_speed
            self.penintent.is_grounded = False
        else:
            # 바닥에 닿았을 때
            self.penintent.y = self.penintent.ground + self.penintent.collider.height / 2
            self.penintent.vy = 0
            self.penintent.is_grounded = True

        # 위치 업데이트
        self.penintent.y += self.penintent.vy * dt

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Attack:
    def __init__(self, penintent):
        self.penintent = penintent
        self.keys_held_on_enter = set()


    def enter(self, e):
        self.penintent.set_animation('attack')
        self.penintent.current_animation.set_stop_point(10)

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

        if game_framework.key_manager.is_held(SDLK_a):
            self.keys_held_on_enter.add('a')
        if game_framework.key_manager.is_held(SDLK_d):
            self.keys_held_on_enter.add('d')


    def exit(self, e):
        self.penintent.attack_collider.active = False
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()


            # 공격 판정 프레임 구간 설정 (예: 3~7 프레임)
            current_frame = self.penintent.current_animation.current_frame
            if 3 <= current_frame <= 7:
                self.penintent.attack_collider.active = True
            else:
                self.penintent.attack_collider.active = False



            if self.penintent.current_animation.is_animation_end():
                # ✅ Attack 종료 시 현재 키 상태 확인
                key_manager = game_framework.key_manager

                # 이동 키가 눌려있는지 확인
                a_pressed = key_manager.is_down(SDLK_a)
                d_pressed = key_manager.is_down(SDLK_d)

                a_held = key_manager.is_held(SDLK_a)
                d_held = key_manager.is_held(SDLK_d)

                if a_held or d_held:
                    # 이동 키가 눌려있으면 RUN으로
                    if a_held:
                        if d_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                        else:
                            self.penintent.state_machine.handle_state_event(('A_HELD', None))

                    else:
                        if a_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                        else:
                            self.penintent.state_machine.handle_state_event(('D_HELD', None))
                else:
                    # 모든 이동 키가 떼어져있으면 IDLE로
                    self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Run:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('run')

        # ✅ 1. 방향 먼저 변경
        if events.d_down(e) or events.a_up(e):
            if self.penintent.face_dir == -1:
                self.penintent.current_animation.set_offset(-20, 0)
            self.penintent.face_dir = 1

        elif events.a_down(e) or events.d_up(e):
            if self.penintent.face_dir == 1:
                self.penintent.current_animation.set_offset(20, 0)
            self.penintent.face_dir = -1

        # ✅ 2. 변경된 방향으로 vx 설정
        self.penintent.vx = self.penintent.move_speed * self.penintent.face_dir

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        self.penintent.vx = 0
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()

        # 물리 처리
        dt = game_framework.time_manager.get_fixed_dt()

        # 바닥 체크
        char_bottom = self.penintent.y - self.penintent.collider.height / 2

        if char_bottom > self.penintent.ground:
            # 공중에 있을 때 중력 적용
            self.penintent.vy += self.penintent.gravity * dt
            if self.penintent.vy < self.penintent.max_fall_speed:
                self.penintent.vy = self.penintent.max_fall_speed
            self.penintent.is_grounded = False
        else:
            # 바닥에 닿았을 때
            self.penintent.y = self.penintent.ground + self.penintent.collider.height / 2
            self.penintent.vy = 0
            self.penintent.is_grounded = True

        # 위치 업데이트
        self.penintent.x += self.penintent.vx * dt
        self.penintent.y += self.penintent.vy * dt

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass

class Start_Run:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('start_run')
        # ✅ 1. 방향 먼저 변경
        if events.d_down(e) or events.a_up(e) or events.d_held(e):
            if self.penintent.face_dir == -1:
                self.penintent.current_animation.set_offset(-20, 0)
            self.penintent.face_dir = 1

        elif events.a_down(e) or events.d_up(e) or events.a_held(e):
            if self.penintent.face_dir == 1:
                self.penintent.current_animation.set_offset(20, 0)
            self.penintent.face_dir = -1

        # ✅ 2. 변경된 방향으로 vx 설정
        self.penintent.vx = self.penintent.move_speed * self.penintent.face_dir

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        self.penintent.vx = 0
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                self.penintent.state_machine.handle_state_event(('ANIMATION_END',None))

        # 물리 처리
        dt = game_framework.time_manager.get_fixed_dt()

        # 바닥 체크
        char_bottom = self.penintent.y - self.penintent.collider.height / 2

        if char_bottom > self.penintent.ground:
            # 공중에 있을 때 중력 적용
            self.penintent.vy += self.penintent.gravity * dt
            if self.penintent.vy < self.penintent.max_fall_speed:
                self.penintent.vy = self.penintent.max_fall_speed
            self.penintent.is_grounded = False
        else:
            # 바닥에 닿았을 때
            self.penintent.y = self.penintent.ground + self.penintent.collider.height / 2
            self.penintent.vy = 0
            self.penintent.is_grounded = True

        # 위치 업데이트
        self.penintent.x += self.penintent.vx * dt
        self.penintent.y += self.penintent.vy * dt

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
        #Idle로 전환할 때 입력 초기화
        if e == ('ANIMATION_END',None):
            game_framework.key_manager.clear_pressed_events()
            game_framework.key_manager.clear_released_events()
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
        self.penintent.set_animation('crouch')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        # ✅ Attack 종료 시 현재 키 상태 확인
        key_manager = game_framework.key_manager

        # 이동 키가 눌려있는지 확인
        a_pressed = key_manager.is_down(SDLK_a)
        d_pressed = key_manager.is_down(SDLK_d)

        if a_pressed or d_pressed:
            if a_pressed:
                self.penintent.face_dir = -1
            else:
                self.penintent.face_dir = 1
            if self.penintent.face_dir == 1:
                self.penintent.current_animation.set_flip('')
            else:
                self.penintent.current_animation.set_flip('h')

        if self.penintent.current_animation:
            if not self.penintent.current_animation.is_animation_end():
                self.penintent.current_animation.update()

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass

class Crouch_Up:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('crouch_up')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        # ✅ Attack 종료 시 현재 키 상태 확인
        key_manager = game_framework.key_manager

        # 이동 키가 눌려있는지 확인
        a_pressed = key_manager.is_down(SDLK_a)
        d_pressed = key_manager.is_down(SDLK_d)

        a_held = key_manager.is_held(SDLK_a)
        d_held = key_manager.is_held(SDLK_d)

        if a_held or d_held:
            # 이동 키가 눌려있으면 RUN으로
            if a_held:
                if d_pressed:
                    self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                else:
                    self.penintent.state_machine.handle_state_event(('A_HELD', None))

            else:
                if a_pressed:
                    self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                else:
                    self.penintent.state_machine.handle_state_event(('D_HELD', None))
        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass
class Dodge:
    def __init__(self, penintent):
        self.penintent = penintent
        self.slide_speed = 0
    def enter(self, e):
        self.penintent.set_animation('dodge')
        self.penintent.current_animation.set_delay(0.04)

        # 슬라이딩 초기 속도 설정
        self.slide_speed = 1500.0 * self.penintent.face_dir

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        self.penintent.current_animation.reset_stop_point()
        self.slide_speed = 0
        pass

    def do(self):
        dt = game_framework.time_manager.get_fixed_dt()

        # 슬라이딩 이동
        current_frame = self.penintent.current_animation.current_frame

        if current_frame < 8:
            # 초반 숙이는 동작은 빠르게
            self.penintent.current_animation.set_delay(0.01)
        else:
            # 슬라이딩 구간은 원래 속도로
            self.penintent.current_animation.set_delay(0.05)

        if 8<= current_frame <= 13:
            # 마찰력으로 속도 감소
            self.slide_speed *= 0.92
            self.penintent.vx = self.slide_speed
        else:
            self.penintent.vx = 0

        # ✅ Attack 종료 시 현재 키 상태 확인
        key_manager = game_framework.key_manager

        # 이동 키가 눌려있는지 확인
        a_pressed = key_manager.is_down(SDLK_a)
        d_pressed = key_manager.is_down(SDLK_d)
        s_pressed = key_manager.is_down(SDLK_s)

        a_held = key_manager.is_held(SDLK_a)
        d_held = key_manager.is_held(SDLK_d)
        s_held = key_manager.is_held(SDLK_s)

        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                if a_held or d_held or s_held:
                    # 이동 키가 눌려있으면 RUN으로
                    if a_held:
                        if s_pressed:
                            self.penintent.state_machine.handle_state_event(('S_HELD', None))
                        elif d_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                        else:
                            self.penintent.state_machine.handle_state_event(('A_HELD', None))
                    elif d_held:
                        if s_pressed:
                            self.penintent.state_machine.handle_state_event(('S_HELD', None))
                        elif a_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                        else:
                            self.penintent.state_machine.handle_state_event(('D_HELD', None))
                    elif s_held:
                        if a_pressed or d_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                        else:
                            self.penintent.state_machine.handle_state_event(('S_HELD', None))
                else:
                    self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))

        # 물리 처리
        char_bottom = self.penintent.y - self.penintent.collider.height / 2

        if char_bottom > self.penintent.ground:
            # 공중에 있을 때 중력 적용
            self.penintent.vy += self.penintent.gravity * dt
            if self.penintent.vy < self.penintent.max_fall_speed:
                self.penintent.vy = self.penintent.max_fall_speed
            self.penintent.is_grounded = False
        else:
            # 바닥에 닿았을 때
            self.penintent.y = self.penintent.ground + self.penintent.collider.height / 2
            self.penintent.vy = 0
            self.penintent.is_grounded = True

        # 위치 업데이트
        self.penintent.x += self.penintent.vx * dt
        self.penintent.y += self.penintent.vy * dt

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass

class Falling_Over:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('falling_over')
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        pass

    def do(self):
        if self.penintent.current_animation:
            if not self.penintent.current_animation.is_animation_end():
                self.penintent.current_animation.update()


        dt = game_framework.time_manager.get_fixed_dt()
            # 물리 처리
        char_bottom = self.penintent.y - self.penintent.collider.height / 2
        if char_bottom > self.penintent.ground:
            # 공중에 있을 때 중력 적용
            self.penintent.vy += self.penintent.gravity * dt
            if self.penintent.vy < self.penintent.max_fall_speed:
                self.penintent.vy = self.penintent.max_fall_speed
            self.penintent.is_grounded = False
        else:
            # 바닥에 닿았을 때
            self.penintent.y = self.penintent.ground + self.penintent.collider.height / 2
            self.penintent.vy = 0
            self.penintent.is_grounded = True
        # 위치 업데이트
        self.penintent.x += self.penintent.vx * dt
        self.penintent.y += self.penintent.vy * dt

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
        self.penintent.set_animation('parry_failed')
        self.penintent.collider.active = False
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        self.penintent.collider.active = True
        pass

    def do(self):
        # ✅ Attack 종료 시 현재 키 상태 확인
        key_manager = game_framework.key_manager

        # 이동 키가 눌려있는지 확인
        a_pressed = key_manager.is_down(SDLK_a)
        d_pressed = key_manager.is_down(SDLK_d)
        s_pressed = key_manager.is_down(SDLK_s)

        a_held = key_manager.is_held(SDLK_a)
        d_held = key_manager.is_held(SDLK_d)
        s_held = key_manager.is_held(SDLK_s)

        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                if a_held or d_held or s_held:
                    # 이동 키가 눌려있으면 RUN으로
                    if a_held:
                        if s_pressed:
                            self.penintent.state_machine.handle_state_event(('S_HELD', None))
                        elif d_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))

                        else:
                            self.penintent.state_machine.handle_state_event(('A_HELD', None))


                    elif d_held:
                        if s_pressed:
                            self.penintent.state_machine.handle_state_event(('S_HELD', None))
                        elif a_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                        else:
                            self.penintent.state_machine.handle_state_event(('D_HELD', None))

                    elif s_held:
                        if a_pressed or d_pressed:
                            self.penintent.state_machine.handle_state_event(('ALL_KEYS_UP', None))
                        else:
                            self.penintent.state_machine.handle_state_event(('S_HELD', None))
                else:
                    self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
            if self.penintent.current_animation.is_animation_end():
                self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))
    pass
class Parry_Success:
    def __init__(self, penintent):
        self.penintent = penintent

    def enter(self, e):
        self.penintent.set_animation('parry_success')
        self.penintent.collider.active = False
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        self.penintent.collider.active = True
        pass

    def do(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass

class Jump:
    def __init__(self, penintent):
        self.penintent = penintent
        self.upanddown = 0
    def enter(self, e):
        self.penintent.set_animation('jump')
        self.penintent.current_animation.set_delay(0.2)
        self.upanddown = 0
        # ✅ Attack 종료 시 현재 키 상태 확인
        key_manager = game_framework.key_manager

        # 이동 키가 눌려있는지 확인
        a_pressed = key_manager.is_down(SDLK_a)
        d_pressed = key_manager.is_down(SDLK_d)

        a_held = key_manager.is_held(SDLK_a)
        d_held = key_manager.is_held(SDLK_d)

        if a_held or d_held:
            if a_held:
                if d_held:
                    self.penintent.vx = 0
                else:
                    self.penintent.face_dir = -1
                    self.penintent.vx = self.penintent.move_speed * self.penintent.face_dir

            elif d_held:
                if a_held:
                    self.penintent.vx = 0
                else:
                    self.penintent.face_dir = 1
                    self.penintent.vx = self.penintent.move_speed * self.penintent.face_dir


        self.penintent.vy = self.penintent.jump_speed
        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

    def exit(self, e):
        self.penintent.vx = 0
        pass

    def do(self):
        key_manager = game_framework.key_manager

        # 이동 키가 눌려있는지 확인
        a_pressed = key_manager.is_down(SDLK_a)
        d_pressed = key_manager.is_down(SDLK_d)
        a_held = key_manager.is_held(SDLK_a)
        d_held = key_manager.is_held(SDLK_d)

        # 공중에서 좌우 이동 제어
        if a_held or d_held:
            if a_held:
                if d_held:
                    self.penintent.vx = 0
                else:
                    self.penintent.face_dir = -1
                    self.penintent.vx = self.penintent.move_speed * self.penintent.face_dir
            elif d_held:
                if a_held:
                    self.penintent.vx = 0
                else:
                    self.penintent.face_dir = 1
                    self.penintent.vx = self.penintent.move_speed * self.penintent.face_dir

        if self.penintent.face_dir == 1:
            self.penintent.current_animation.set_flip('')
        else:
            self.penintent.current_animation.set_flip('h')

        # 애니메이션 업데이트
        if self.penintent.current_animation:
            self.penintent.current_animation.update()
            if self.penintent.current_animation.is_animation_end():
                if self.upanddown == 0:
                    self.penintent.set_animation('jump_off')
                    self.penintent.current_animation.set_delay(0.1)
                    self.upanddown = 1
                elif self.upanddown == 1:
                    if a_held or d_held:
                        if a_held:
                            if d_held:
                                self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))
                            else:
                                self.penintent.state_machine.handle_state_event(('A_HELD', None))
                        elif d_held:
                            if a_held:
                                self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))
                            else:
                                self.penintent.state_machine.handle_state_event(('D_HELD', None))

                    else:
                        self.penintent.state_machine.handle_state_event(('ANIMATION_END', None))
                    self.penintent.current_animation.set_delay(0.05)

        # 물리 처리 - Jump는 항상 중력 영향을 받음
        dt = game_framework.time_manager.get_fixed_dt()

        # 중력 적용
        self.penintent.vy += self.penintent.gravity * dt
        if self.penintent.vy < self.penintent.max_fall_speed:
            self.penintent.vy = self.penintent.max_fall_speed

        # 위치 업데이트
        self.penintent.x += self.penintent.vx * dt
        self.penintent.y += self.penintent.vy * dt

        # 바닥 체크
        char_bottom = self.penintent.y - self.penintent.collider.height / 2
        if char_bottom <= self.penintent.ground:
            self.penintent.y = self.penintent.ground + self.penintent.collider.height / 2
            self.penintent.vy = 0
            self.penintent.is_grounded = True

    def draw(self):
        if self.penintent.current_animation:
            self.penintent.current_animation.draw(self.penintent.x, self.penintent.y)
    pass


class Penintent:
    def __init__(self, anim_manager):
        game_framework.camera_manager.set_target(self)

        self.collider = Collider(self, offset_x=0, offset_y=0, width=40, height=90)

        # 공격 충돌체 (기본적으로 비활성화)
        self.attack_collider = Collider(self, offset_x = 60, offset_y = 0, width = 80, height = 90)
        self.attack_collider.active = False


        # 애니메이션별 콜라이더 프리셋: (offset_x, offset_y, width, height)
        # 필요하면 애니메이션 이름과 값들을 튜닝
        self.collider_presets = {
            'idle': {'offset_x': 20, 'offset_y': 0, 'width': 40, 'height': 90},
            'run': {'offset_x': 20, 'offset_y': 0, 'width': 40, 'height': 90},
            'start_run': {'offset_x': 10, 'offset_y': 0, 'width': 40, 'height': 90},
            'stop_run': {'offset_x': 20, 'offset_y': 0, 'width': 40, 'height': 90},
            'crouch': {'offset_x': 20, 'offset_y': -20, 'width': 40, 'height': 60},
            'crouch_up': {'offset_x': 20, 'offset_y': 0, 'width': 40, 'height': 90},
            'dodge': {'offset_x': 0, 'offset_y': -30, 'width': 50, 'height': 50},
            'attack': {'offset_x': 0, 'offset_y': 0, 'width': 60, 'height': 90},
            'jump': {'offset_x': 0, 'offset_y': 0, 'width': 40, 'height': 90},
            # 필요 시 더 추가
        }
        self.attack_collider_presets = {
            'attack': {'offset_x': 60, 'offset_y': 10, 'width': 80, 'height': 60}
        }

        # 애니메이션 이름 리스트
        anim_names = [
            'idle', 'attack', 'run', 'start_run', 'stop_run',
            'crouch', 'crouch_up', 'dodge', 'falling_over',
            'getting_up', 'parry_failed', 'parry_success',
            'jump', 'jump_off', 'jump_front'
        ]
        # 히트 타이머
        self.hit_flash_timer = 0.0
        self.hit_flash_duration = 0.2  # 피격 플래시 지속 시간

        # 캐릭터 속성
        self.hp = 100

        self.x, self.y = 400,500
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
                            events.s_down: self.CROUCH, events.space_down: self.JUMP, events.k_down: self.ATTACK,
                             events.shift_down : self.DODGE,events.j_down: self.PARRY_FAILED,events.dead : self.FALLING_OVER},
                self.START_RUN: {events.animation_end: self.RUN, events.s_down: self.CROUCH, events.space_down: self.JUMP,
                                 events.k_down: self.ATTACK,events.a_up: self.STOP_RUN, events.d_up:self.STOP_RUN,
                                 events.a_down: self.STOP_RUN, events.d_down:self.STOP_RUN,events.shift_down : self.DODGE,
                                 events.j_down: self.PARRY_FAILED,events.dead : self.FALLING_OVER},
                self.RUN: {events.space_down: self.JUMP , events.a_up : self.STOP_RUN, events.d_up: self.STOP_RUN,
                           events.s_down: self.CROUCH, events.a_down: self.STOP_RUN, events.d_down: self.STOP_RUN,
                           events.k_down: self.ATTACK,events.shift_down : self.DODGE,events.j_down: self.PARRY_FAILED
                          ,events.dead : self.FALLING_OVER},
                self.STOP_RUN: {events.animation_end: self.IDLE, events.s_down: self.CROUCH,
                                events.a_down: self.START_RUN, events.d_down: self.START_RUN,
                                events.a_up: self.START_RUN, events.d_up: self.START_RUN,events.dead : self.FALLING_OVER
                                },
                self.ATTACK: {events.all_keys_up: self.IDLE,
                events.a_held: self.START_RUN,
                events.d_held: self.START_RUN,events.dead : self.FALLING_OVER},
                self.CROUCH: {events.s_up: self.CROUCH_UP,events.shift_down : self.DODGE,
                              events.j_down: self.PARRY_FAILED,events.dead : self.FALLING_OVER},
                self.CROUCH_UP: {events.animation_end: self.IDLE,
                                 events.all_keys_up: self.IDLE,
                                 events.a_held: self.START_RUN,
                                 events.d_held: self.START_RUN,events.dead : self.FALLING_OVER
                                 },
                self.JUMP: {events.animation_end: self.IDLE,
                            events.a_held: self.START_RUN,
                            events.d_held: self.START_RUN,events.dead : self.FALLING_OVER
                            },
                self.DODGE: {events.animation_end: self.IDLE,
                    events.a_held: self.START_RUN,
                    events.d_held: self.START_RUN,
                    events.s_held: self.CROUCH,
                    events.all_keys_up: self.IDLE,
                    events.j_down: self.PARRY_FAILED,events.dead : self.FALLING_OVER
                },
                self.PARRY_FAILED: {events.animation_end: self.IDLE,
                                    events.a_held: self.START_RUN,
                                    events.d_held: self.START_RUN,
                                    events.s_held: self.CROUCH,
                                    events.all_keys_up: self.IDLE,events.dead : self.FALLING_OVER
                                    },
                self.FALLING_OVER : {

                }

            }
        )

        self.is_grounded = False  # 땅에 닿아있는지 여부


    def apply_attack_collider_preset(self, ani_name):
        """공격 충돌체 프리셋 적용"""
        preset = self.attack_collider_presets.get(ani_name)
        if not preset:
            self.attack_collider.active = False
            return

        ox = preset['offset_x']
        oy = preset['offset_y']
        w = preset['width']
        h = preset['height']

        # 방향에 따라 x offset 반전
        if self.face_dir == -1:
            ox = -ox

        self.attack_collider.set_offset_and_size(ox, oy, w, h)
        self.attack_collider.active = True




    def apply_collider_preset(self, ani_name):
        preset = self.collider_presets.get(ani_name)
        if not preset:
            return

        ox = preset['offset_x']
        oy = preset['offset_y']
        w = preset['width']
        h = preset['height']

        if self.face_dir == -1:
            ox = -ox

        # Collider 구현에 따라 가능한 API를 시도해서 적용 (호한성 확보)
        if hasattr(self.collider, 'set_offset_and_size'):
            # 통합 API가 있으면 가장 간단하게 호출
            try:
                self.collider.set_offset_and_size(ox, oy, w, h)
                return
            except Exception:
                pass

                # 개별 메서드/속성으로 설정 (존재 여부에 따라)
                if hasattr(self.collider, 'set_offset'):
                    try:
                        self.collider.set_offset(ox, oy)
                    except Exception:
                        setattr(self.collider, 'offset_x', ox)
                        setattr(self.collider, 'offset_y', oy)
                else:
                    setattr(self.collider, 'offset_x', ox)
                    setattr(self.collider, 'offset_y', oy)

                if hasattr(self.collider, 'set_size'):
                    try:
                        self.collider.set_size(w, h)
                    except Exception:
                        setattr(self.collider, 'width', w)
                        setattr(self.collider, 'height', h)
                else:
                    setattr(self.collider, 'width', w)
                    setattr(self.collider, 'height', h)

    def clamp_to_world(self):
        """월드 경계 내로 위치 제한"""
        world_width = game_framework.camera_manager.world_width
        world_height = game_framework.camera_manager.world_height

        if world_width is not None:
            self.x = max(0, min(self.x, world_width))
        if world_height is not None:
            self.y = max(0, min(self.y, world_height))

    def set_animation(self,name):
        """ 애니메이션 변경"""
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.current_frame = 0
            self.current_animation.frame_time = 0

            self.apply_collider_preset(name)

            if name == 'attack':
                self.apply_attack_collider_preset(name)
            else:
                self.attack_collider.active = False

    def handle_input(self):
        pass

    def update(self):
        # 키 입력을 이벤트로 변환
        for event in game_framework.key_manager.get_pressed_events():
            self.state_machine.handle_state_event(('INPUT', event))

        for event in game_framework.key_manager.get_released_events():
            self.state_machine.handle_state_event(('INPUT', event))

        # 상태 머신 업데이트 - 각 상태의 do()에서 물리 처리가 실행됨
        self.state_machine.update()

        if self.hit_flash_timer > 0:
            dt = game_framework.time_manager.get_fixed_dt()
            self.hit_flash_timer -= dt
            if self.hit_flash_timer < 0:
                self.hit_flash_timer = 0


    def on_collision_enter(self, group, other,collider_type):
        """Collider Manager로부터 호출되는 충돌 콜백 (현재 사용 안 함)"""
        if group == 'elderBrother_attack:player' and collider_type == 'base':
            self.hp -= 10
            self.hit_flash_timer = self.hit_flash_duration  # ← 피격 효과 트리거
            if self.hp <= 0:
                self.state_machine.handle_state_event(("DEAD",None))

        pass

    def on_collision(self, group, other, collider_type):
        """충돌 지속"""
        pass  # 필요시 구현

    def on_collision_exit(self, group, other, collider_type):
        """충돌 종료"""
        pass  # 필요시 구현

    def check_terrain_collision(self):
        """지형과의 충돌 검사 (현재 사용 안 함)"""
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()
        if self.current_animation and self.hit_flash_timer > 0:
            self.current_animation.set_color_mode(255,100,100)
            self.current_animation.draw(self.x, self.y)
        elif self.current_animation:
            self.current_animation.reset_color_mode()
            self.current_animation.draw(self.x, self.y)


        self.collider.draw_debug()
        if self.attack_collider.active:
            self.attack_collider.draw_debug()

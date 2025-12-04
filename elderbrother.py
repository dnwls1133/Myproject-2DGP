import game_framework
from pico2d import *
from machine.animation import Animation
from machine.state_machine import StateMachine
from sdl2 import *
from machine import events
from collider import Collider
import game_world
import math
import random
from physics_config import PhysicsConfig

jump_voice_sound = None
jump_sound = None
landing_sound = None

attack_sound = None
attack_hit_sound = None
attack_voice_sound = None
attack_damaged_sound = None


def load_sounds():
    global jump_voice_sound, jump_sound, landing_sound,attack_sound,attack_hit_sound,attack_voice_sound,attack_damaged_sound
    if jump_voice_sound is None:
        jump_voice_sound = load_wav('music/SFX/ELDER_BROTHER_JUMP_VOICE.wav')
        jump_sound = load_wav('music/SFX/ELDER_BROTHER_JUMP.wav')
        landing_sound = load_wav('music/SFX/ELDER_BROTHER_LANDING.wav')

    if attack_sound is None:
        attack_sound = load_wav('music/SFX/ELDER_BROTHER_ATTACK.wav')
        attack_hit_sound = load_wav('music/SFX/ELDER_BROTHER_ATTACK_HIT.wav')
        attack_voice_sound = load_wav('music/SFX/ELDER_BROTHER_ATTACK_VOICE.wav')
        attack_damaged_sound = load_wav('music/SFX/PENITENT_HEAVY_ENEMY_HIT.wav')




class Idle:
    def __init__(self, elder_brother):
        self.elder_brother = elder_brother

        self.check_interval = 0.3
        self.check_timer = 0.0

    def get_detection_range(self):
        return 200 if self.elder_brother.is_opening else 600

    def get_attack_range(self):
        return 100 if self.elder_brother.is_opening else 400

    def enter(self, e):

        self.elder_brother.vx = 0
        self.elder_brother.set_animation('elder_brother_idle')
        self.elder_brother.current_animation.set_delay(0.1)
        if self.elder_brother.face_dir == 1:
            self.elder_brother.current_animation.set_flip('')
        else:
            self.elder_brother.current_animation.set_flip('h')
        self.check_timer = 0.0

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


        # AI 판단 주기 업데이트
        self.check_timer += dt
        if self.check_timer >= self.check_interval and self.elder_brother.is_grounded:
            player = self.elder_brother.get_player()
            if player:
                distance = abs(self.elder_brother.x - player.x)
                if distance <= self.get_attack_range():
                    self.elder_brother.state_machine.handle_state_event(('AI_ATTACK',None))
                elif distance <= self.get_detection_range():
                    self.elder_brother.state_machine.handle_state_event(('AI_JUMP',None))

            self.check_timer = 0.0




    def draw(self):
        if self.elder_brother.current_animation:
            self.elder_brother.current_animation.draw(self.elder_brother.x, self.elder_brother.y)


class Jump:
    def __init__(self, elder_brother):
        self.elder_brother = elder_brother
        self.air_time = 0.8
        self.max_jump_height = 600  # 최고 점프 높이

    def enter(self, e):

        self.elder_brother.set_animation('elder_brother_jump')
        self.elder_brother.current_animation.set_delay(0.1)

        player = self.elder_brother.get_player()

        if player and self.elder_brother.is_grounded:
            # 플레이어까지의 수평 거리
            distance = player.x - self.elder_brother.x


            self.elder_brother.vx = distance / self.air_time
            # 최고 높이와 체공 시간으로 점프 속도 계산
            # v0y = (4 * max_height) / (air_time / 2)
            self.elder_brother.vy = (4 * self.max_jump_height) / (self.air_time / 2)

            # 중력도 체공 시간과 최고 높이에 맞게 조정
            # g = (8 * max_height) / (air_time / 2)^2
            self.elder_brother.gravity = -(8 * self.max_jump_height) / ((self.air_time / 2) ** 2)
            # 방향 설정
            if distance > 0:
                self.elder_brother.face_dir = 1
                self.elder_brother.current_animation.set_flip('')
            else:
                self.elder_brother.face_dir = -1
                self.elder_brother.current_animation.set_flip('h')

        jump_voice_sound.set_volume(64)
        jump_voice_sound.play()

        jump_sound.set_volume(64)
        jump_sound.play()




    def exit(self, e):

        pass

    def do(self):
        if self.elder_brother.current_animation:
            self.elder_brother.current_animation.update()
            if self.elder_brother.current_animation.is_animation_end():
                self.elder_brother.state_machine.handle_state_event(('ANIMATION_END',None))


        current_frame = self.elder_brother.current_animation.current_frame
        # 점프 애니메이션 프레임에 따른 수직 속도 조절

        if 20 <= current_frame <= 24:
            self.elder_brother.jump_attack_collider.active = True
        else:
            self.elder_brother.jump_attack_collider.active = False

        if 9<= current_frame :
            # 물리 처리
            dt = game_framework.time_manager.get_fixed_dt()

            # 바닥 체크
            char_bottom = self.elder_brother.y - self.elder_brother.collider.height / 2

            self.elder_brother.vy += self.elder_brother.gravity * dt
            if self.elder_brother.vy < self.elder_brother.max_fall_speed:
                self.elder_brother.vy = self.elder_brother.max_fall_speed

            self.elder_brother.y += self.elder_brother.vy * dt
            self.elder_brother.x += self.elder_brother.vx * dt

            if char_bottom <= self.elder_brother.ground and self.elder_brother.vy <= 0:
                # 바닥에 닿았을 때
                self.elder_brother.y = self.elder_brother.ground + self.elder_brother.collider.height / 2
                self.elder_brother.vy = 0
                self.elder_brother.vx = 0
                self.elder_brother.is_grounded = True
                game_framework.camera_manager.shake(5,0.5)
                self.elder_brother.create_effects(
                    'elder_brother_hardlanding',
                    self.elder_brother.x,
                    self.elder_brother.y - 75,

                    delay=0.05,
                    scale=2.0,
                    flip='' if self.elder_brother.face_dir == 1 else 'h'
                )
                self.elder_brother.create_effects(
                    'elder_brother_corpse',
                    self.elder_brother.x + random.randint(-200, 200),
                    self.elder_brother.y - 75,
                    delay=0.05,
                    scale=1.0,
                    flip='' if self.elder_brother.face_dir == 1 else 'h'
                )
                landing_sound.set_volume(64)
                landing_sound.play()

        if self.elder_brother.y >= self.max_jump_height and self.elder_brother.is_opening:
            self.elder_brother.is_opening = False
            self.elder_brother.ground = 100
            game_world.change_depth(self.elder_brother,3)



    def draw(self):
        if self.elder_brother.current_animation:
            self.elder_brother.current_animation.draw(self.elder_brother.x, self.elder_brother.y)


class Attack:
    def __init__(self, elder_brother):
        self.elder_brother = elder_brother

    def enter(self, e):

        self.elder_brother.vx = 0
        self.elder_brother.set_animation('elder_brother_attack')
        self.elder_brother.current_animation.set_delay(0.05)



        # 플레이어 방향보기
        player = self.elder_brother.get_player()


        if player:
            if player.x > self.elder_brother.x:
                self.elder_brother.face_dir = 1
                self.elder_brother.current_animation.set_flip('')
            else:
                self.elder_brother.face_dir = -1
                self.elder_brother.current_animation.set_flip('h')

        self.elder_brother.apply_attack_collider_preset('elder_brother_attack')
        attack_voice_sound.set_volume(64)
        attack_voice_sound.play()


    def exit(self, e):
        pass

    def do(self):
        if self.elder_brother.current_animation:
            self.elder_brother.current_animation.update()

        # 물리 처리
        dt = game_framework.time_manager.get_fixed_dt()

        current_frame = self.elder_brother.current_animation.current_frame
        if 16 <= current_frame<= 20:
            self.elder_brother.current_animation.set_delay(0.1)
            self.elder_brother.attack_collider.active = True
            if current_frame ==16:
                game_framework.camera_manager.shake(5, 0.5)
                self.elder_brother.create_effects(
                    'elder_brother_hardlanding',
                    self.elder_brother.x,
                    self.elder_brother.y - 75,

                    delay=0.05,
                    scale=2.0,
                    flip='' if self.elder_brother.face_dir == 1 else 'h'
                )
                attack_sound.set_volume(64)
                attack_sound.play()



        preset = self.elder_brother.attack_collider_presets.get('elder_brother_attack')
        if self.elder_brother.attack_collider.active == True:
            ox = preset['offset_x']
            oy = preset['offset_y']
            w = preset['width']
            h = preset['height']

            # 방향에 따라 x offset 반전
            if self.elder_brother.face_dir == 1:
                ox += (current_frame -16) * 40

            else:
                ox = -ox - (current_frame -16) * 40
            if current_frame % 2 == 0:
                self.elder_brother.create_effects(
                    'elder_brother_beam',
                    self.elder_brother.x + ox,
                    self.elder_brother.y - 75,
                    delay=0.05,
                    scale=1.0,
                    flip='' if self.elder_brother.face_dir == 1 else 'h'
                )
                for i in range(3):
                    self.elder_brother.create_effects(
                        'elder_brother_corpse',
                        self.elder_brother.x + ox + random.randint(-30, 30),
                        self.elder_brother.y - 20 + random.randint(-20, 80),
                        delay=0.05,
                        scale=1.0,
                        flip='' if self.elder_brother.face_dir == 1 else 'h'
                    )

            self.elder_brother.attack_collider.set_offset_and_size(ox, oy, w, h)

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

        # 공격 애니메이션 종료 체크
        if self.elder_brother.current_animation.is_animation_end():
            self.elder_brother.state_machine.handle_state_event(('ANIMATION_END',None))

    def draw(self):
        if self.elder_brother.current_animation:
            self.elder_brother.current_animation.draw(self.elder_brother.x, self.elder_brother.y)


class Death:
    def __init__(self, elder_brother):
        self.elder_brother = elder_brother

    def enter(self, e):

        game_framework.time_manager.set_time_scale(0.5)  # 시간 느리게 설정
        self.elder_brother.set_animation('elder_brother_death')
        self.elder_brother.current_animation.set_delay(0.1)
        if self.elder_brother.face_dir == 1:
            self.elder_brother.current_animation.set_flip('')

        else:
            self.elder_brother.current_animation.set_flip('h')
        self.elder_brother.vx = -1 * self.elder_brother.face_dir * 300
        self.elder_brother.vy = 600
        self.elder_brother.hit_flash_timer = 5.0
        self.elder_brother.collider.active = False

    def exit(self, e):
        pass

    def do(self):
        if self.elder_brother.current_animation:
            if not self.elder_brother.current_animation.is_animation_end():
                self.elder_brother.current_animation.update()
            else:
                game_framework.time_manager.set_time_scale(1.0)



        # 물리 처리
        dt = game_framework.time_manager.get_fixed_dt()

        # 바닥 체크
        char_bottom = self.elder_brother.y - self.elder_brother.collider.height / 2

        self.elder_brother.vy += self.elder_brother.gravity * dt
        if self.elder_brother.vy < self.elder_brother.max_fall_speed:
            self.elder_brother.vy = self.elder_brother.max_fall_speed

        self.elder_brother.y += self.elder_brother.vy * dt
        self.elder_brother.x += self.elder_brother.vx * dt

        if char_bottom <= self.elder_brother.ground and self.elder_brother.vy <= 0:
            # 바닥에 닿았을 때
            self.elder_brother.y = self.elder_brother.ground + self.elder_brother.collider.height / 2
            self.elder_brother.vy = 0
            self.elder_brother.vx = 0
            self.elder_brother.is_grounded = True



    def draw(self):
        if self.elder_brother.current_animation:

            self.elder_brother.current_animation.draw(self.elder_brother.x, self.elder_brother.y)





class ElderBrother:
    def __init__(self,anim_manager):
        load_sounds()
        self.anim_manager = anim_manager
        self.collider = Collider(self, offset_x=0, offset_y=0, width=159, height=171)

        self.attack_collider = Collider(self, offset_x=80, offset_y=0, width=60, height=170)
        self.attack_collider.active = False

        self.jump_attack_collider = Collider(self, offset_x=0, offset_y=-50, width=360, height=90)
        self.jump_attack_collider.active = False

        self.attack_collider_presets = {
            'elder_brother_attack': {'offset_x': 80, 'offset_y': 0, 'width': 60, 'height': 170}
        }

        anim_names = ['elder_brother_idle',
                      'elder_brother_attack',
                      'elder_brother_jump',
                      'elder_brother_death']
        self.hp = 100
        self.x, self.y = 1300, 150
        self.face_dir = -1

        # 물리 속성
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.ground = 200

        # ==================== 실제 물리 단위 기반 속성 ====================
        # PhysicsConfig를 통해 실제 물리 값을 픽셀 단위로 변환
        physics = PhysicsConfig.get_boss_physics()

        # 중력 (pixels/s^2) - 실제 중력 9.81m/s^2를 픽셀로 변환
        self.gravity = physics['gravity']  # -981 pixels/s^2

        # 최대 낙하 속도 (pixels/s) - 실제 12m/s (보스는 더 무거움)
        self.max_fall_speed = physics['max_fall_speed']  # -1200 pixels/s

        # 점프 속도 (pixels/s) - 실제 8m/s (보스는 더 높이 점프)
        self.jump_speed = physics['jump_speed']  # 800 pixels/s

        # 마찰 계수 (무차원)
        self.friction = 0.8

        # 이동 속도 (pixels/s) - 보스는 일반적으로 이동하지 않음
        self.move_speed = 250.0

        # 실제 물리 단위 저장 (디버그 및 참조용)
        self.height_meters = PhysicsConfig.Boss.HEIGHT_METERS
        self.jump_speed_mps = PhysicsConfig.Boss.JUMP_SPEED_MPS
        # ================================================================

        self.is_opening = True
        self.is_grounded = False

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
        self.JUMP = Jump(self)
        self.ATTACK = Attack(self)
        self.DEATH = Death(self)


        self.state_machine = StateMachine(
            self.IDLE,{
                self.IDLE : {events.ai_attack : self.ATTACK,
                             events.ai_jump : self.JUMP,
                             events.dead : self.DEATH},
                self.JUMP: {events.animation_end : self.IDLE,
                             events.dead : self.DEATH},
                self.ATTACK: {events.animation_end : self.IDLE,
                             events.dead : self.DEATH},
                self.DEATH: {}
            }
        )

        self.hit_flash_timer = 0.0
        self.hit_flash_duration = 0.2  # 피격 플래시 지속 시간

    def get_real_position(self):
        """실제 미터 단위 위치 반환 (디버그용)"""
        return (
            PhysicsConfig.pixels_to_meters(self.x),
            PhysicsConfig.pixels_to_meters(self.y)
        )

    def get_real_velocity(self):
        """실제 m/s 단위 속도 반환 (디버그용)"""
        return (
            PhysicsConfig.pps_to_mps(self.vx),
            PhysicsConfig.pps_to_mps(self.vy)
        )

    def create_effects(self, anim_name,x,y,delay=0.05,scale=1.5,flip=''):
        from Obj.effect import Effect
        import game_world



        hit_effect = Effect(
            x,
            y,
            anim_name,
            self.anim_manager,
            delay=delay,
            scale=scale,
            flip=flip
        )
        game_world.add_object(hit_effect,4) # 이펙트를 적절한 레이어에 추가


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



    def set_animation(self, name):
        """ 애니메이션 변경"""
        if name in self.animations:
            self.current_animation = self.animations[name]
            self.current_animation.current_frame = 0
            self.current_animation.frame_time = 0

            if name == 'elder_brother_attack':
                self.apply_attack_collider_preset(name)
            else:
                self.attack_collider.active = False




    def get_player(self):
        """플레이어 객체 반환 (현재는 None 반환)"""
        import game_world
        return game_world.get_penintent()

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


    def on_collision_enter(self, group, other, collider_type):
        global attack_damaged_sound
        if group == 'player_attack:elderBrother' and collider_type == 'base':  # ← 'attack'이 아니라 'base'
            self.hp -= 0.5
            self.hit_flash_timer = self.hit_flash_duration  # ← 피격 효과 트리거
            game_framework.camera_manager.shake(5,0.3)
            effect_x = self.x
            effect_y = self.y
            self.create_effects(
                'penitent_attack_spark1',
                effect_x,
                effect_y,
                delay=0.05,
                scale=1.5,
                flip='' if self.face_dir == 1 else 'h'
            )
            attack_damaged_sound.set_volume(64)
            attack_damaged_sound.play()
            print(f"Elder Brother HP: {self.hp}")
            if self.hp <= 0:
                self.state_machine.handle_state_event(('DEAD', None))

    def on_collision(self, group, other, collider_type):
        """충돌 지속"""
        pass  # 필요시 구현

    def on_collision_exit(self, group, other, collider_type):
        """충돌 종료"""
        pass  # 필요시 구현

    def draw(self):
        self.state_machine.draw()

        if self.is_opening:
            self.current_animation.set_color_mode(10, 10, 10)
            self.current_animation.draw(self.x, self.y)
        else:
            if self.current_animation and self.hit_flash_timer > 0:
                self.current_animation.set_color_mode(255, 100, 100)
                self.current_animation.draw(self.x, self.y)
            elif self.current_animation:
                self.current_animation.reset_color_mode()
                self.current_animation.draw(self.x, self.y)


        self.collider.draw_debug()

        if self.attack_collider.active:
            self.attack_collider.draw_debug()

        if self.jump_attack_collider.active:
            self.jump_attack_collider.draw_debug()

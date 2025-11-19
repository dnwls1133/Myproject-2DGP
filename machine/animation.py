from pico2d import *
import json
import game_framework
import ctypes
from sdl2 import SDL_SetTextureColorMod
def register_animations(anim_manager):
    anim_manager.register_animation(
        'idle',
        "sprites/player/texture2d/player_idle/penitent_idle_anim.json",
        "sprites/player/texture2d/player_idle/penitent_idle_anim.png"
    )
    anim_manager.register_animation(
        'attack',
        "sprites/player/texture2d/player_attack/penitent_attack_combo_anim.json",
        "sprites/player/texture2d/player_attack/penitent_attack_combo_anim.png"
    )
    anim_manager.register_animation(
        'start_run',
        "sprites/player/texture2d/player_run/penitent_start_run_anim.json",
        "sprites/player/texture2d/player_run/penitent_start_run_anim.png"
    )
    anim_manager.register_animation(
        'run',
        "sprites/player/texture2d/player_run/penitent_running_anim.json",
        "sprites/player/texture2d/player_run/penitent_running_anim.png"
    )
    anim_manager.register_animation(
        'stop_run',
        "sprites/player/texture2d/player_run/penitent_stop_run_anim.json",
        "sprites/player/texture2d/player_run/penitent_stop_run_anim.png"
    )
    anim_manager.register_animation(
        'crouch',
        "sprites/player/texture2d/player_crouch/penitent_crouch_anim.json",
        "sprites/player/texture2d/player_crouch/penitent_crouch_anim.png"
    )
    anim_manager.register_animation(
        'crouch_up',
        "sprites/player/texture2d/player_crouch/penitent_crouch_up_anim.json",
        "sprites/player/texture2d/player_crouch/penitent_crouch_up_anim.png"
    )
    anim_manager.register_animation(
        'dodge',
        "sprites/player/texture2d/player_dodge/penitent_dodge_anim.json",
        "sprites/player/texture2d/player_dodge/penitent_dodge_anim.png"
    )
    anim_manager.register_animation(
        'falling_over',
        "sprites/player/texture2d/player_falling/penitent_falling_over_anim.json",
        "sprites/player/texture2d/player_falling/penitent_falling_over_anim.png"
    )
    anim_manager.register_animation(
        'getting_up',
        "sprites/player/texture2d/player_falling/penitent_getting_up_anim.json",
        "sprites/player/texture2d/player_falling/penitent_getting_up_anim.png"
    )
    anim_manager.register_animation(
        'parry_failed',
        "sprites/player/texture2d/player_parry/penitent_parry_failed_anim.json",
        "sprites/player/texture2d/player_parry/penitent_parry_failed_anim.png"
    )
    anim_manager.register_animation(
        'parry_success',
        "sprites/player/texture2d/player_parry/penitent_parry_anim.json",
        "sprites/player/texture2d/player_parry/penitent_parry_anim.png"
    )
    anim_manager.register_animation(
        'jump',
        "sprites/player/texture2d/player_jump/penitent_jump_anim.json",
        "sprites/player/texture2d/player_jump/penitent_jump_anim.png"
    )
    anim_manager.register_animation(
        'jump_off',
        "sprites/player/texture2d/player_jump/penitent_jump_off_anim.json",
        "sprites/player/texture2d/player_jump/penitent_jump_off_anim.png"
    )
    anim_manager.register_animation(
        'jump_front',
        "sprites/player/texture2d/player_jump/penitent_jum_forward_anim.json",
        "sprites/player/texture2d/player_jump/penitent_jum_forward_anim.png"
    )
    anim_manager.register_animation(
        'elder_brother_idle',
        "sprites/elderbrother/texture2d/elderBrother_idle_anim.json",
        "sprites/elderbrother/texture2d/elderBrother_idle_anim.png"
    )
    anim_manager.register_animation(
        'elder_brother_attack',
        "sprites/elderbrother/texture2d/elderBrother_attack_anim.json",
        "sprites/elderbrother/texture2d/elderBrother_attack_anim.png"
    )
    anim_manager.register_animation(
        'elder_brother_death',
        "sprites/elderbrother/texture2d/elderBrother_death_anim.json",
        "sprites/elderbrother/texture2d/elderBrother_death_anim.png"
    )
    anim_manager.register_animation(
        'elder_brother_jump',
        "sprites/elderbrother/texture2d/elder_brother_jump/elder_brother_jump_anim.json",
        "sprites/elderbrother/texture2d/elder_brother_jump/elder_brother_jump_anim.png"
    )
    anim_manager.register_animation(
        'main_menu_background',
        "sprites/main_menu/texture2d/UI/crisanta-bg-main-menu_anim.json",
        "sprites/main_menu/texture2d/UI/crisanta-bg-main-menu_anim.png"
    )
    anim_manager.register_animation(
        'main_menu_crisanta',
        "sprites/main_menu/texture2d/UI/crisanta-main-menu_anim.json",
        "sprites/main_menu/texture2d/UI/crisanta-main-menu_anim.png"
    )


class AnimationManager:
    def __init__(self):
        self.animations = {}
        self.images = {}


    def register_animation(self,name,json_file,image_file):
        """애니메이션을 등록합니다."""
        # JSON 데이터 로드
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        frames = []
        for sprite in data['sprites']:
            frame_info = {
                'fileName' : sprite['fileName'],
                'width' : sprite['width'],
                'height' : sprite['height'],
                'x' : sprite['x'],
                'y' : sprite['y'],
                'offsetX': sprite.get('offsetX', 0),  # JSON에서 읽기
                'offsetY': sprite.get('offsetY', 0)  # JSON에서 읽기
            }
            frames.append(frame_info)

        # 프레임 정렬
        # sort()는 파이썬의 내장 리스트 정렬 메서드이빈다.
        # key 매개변수에 정렬 기준을 정하는 함수를 전달
        # lambda x: - 각 프레임 정보를 받는 익명 함수
        #x['fileName'] - 파일명 추출 (예: "sprite_001.png")
        #.split('_')[-1] - 언더스코어로 분할 후 마지막 부분 추출 ("001.png")
        #.split('.')[0] - 점으로 분할 후 첫 번째 부분 추출 ("001")
        #int() - 문자열을 숫자로 변환


        frames.sort(key = lambda x: int(x['fileName'].split('_')[-1].split('.')[0]))

        # 이미지 로드
        if image_file not in self.images:
            self.images[image_file] = load_image(image_file)
        self.animations[name] = {
            'frames': frames,
            'data' : data,
            'image': self.images[image_file]
        }
    def get_animation(self,name):
        """등록된 애니메이션을 반환합니다."""
        return self.animations.get(name)



class Animation:
    def __init__(self,animation_data):
        self.frames = animation_data['frames']
        self.data = animation_data['data']
        self.image = animation_data['image']
        self.current_frame = 0
        self.frame_time = 0.0
        self.frame_delay = 0.05  # 각 프레임당 지속 시간 (초)
        self.flip = ''  # 'h' for horizontal flip, '' for normal
        self.stop_point = len(self.frames) -1  # 애니메이션이 멈출 프레임 인덱스
        self.color_mod = (255, 255, 255)  # 기본 색상 변조 (흰색, 변경 없음)


        # 애니메이션별 오프셋 (숙이기, 점프 등)
        self.offset_x = 0
        self.offset_y = 0

    def set_color_mode(self,r,g,b):
        self.color_mod = (r,g,b)

    def reset_color_mode(self):
        self.color_mod = (255,255,255)

    def set_delay(self,frame_delay):
        """프레임 지연 시간을 설정합니다."""
        self.frame_delay = frame_delay

    def set_offset(self,offset_x,offset_y):
        """애니메이션 오프셋을 설정합니다."""
        self.offset_x = offset_x
        self.offset_y = offset_y

    def set_flip(self, flip):
        """애니메이션의 좌우 반전을 설정합니다."""
        self.flip = flip

    def update(self):
        """애니메이션 프레임을 업데이트합니다."""
        dt = game_framework.time_manager.get_fixed_dt()
        self.frame_time += dt

        if self.frame_time >= self.frame_delay:
            self.frame_time -= self.frame_delay
            self.current_frame = (self.current_frame + 1) % (self.stop_point + 1)


    def draw(self,x,y,scale=1):  # 2.5 대신 3으로 변경 (정수 배율)
        """애니메이션을 그립니다."""




        frame_info = self.frames[self.current_frame]

        # 윈도우-뷰포트 배율 계산
        viewport_scale_x = game_framework.camera_manager.screen_width / game_framework.camera_manager.window_width
        viewport_scale_y = game_framework.camera_manager.screen_height / game_framework.camera_manager.window_height

        # 정수 배율로 픽셀 아트 선명도 유지 + 윈도우-뷰포트 배율 적용
        draw_width = int(frame_info['width'] * scale * viewport_scale_x)
        draw_height = int(frame_info['height'] * scale * viewport_scale_y)

        offset_x = frame_info.get('offsetX', 0)
        offset_y = frame_info.get('offsetY', 0)

        # 오프셋 적용
        # 좌우 반전 시 X 오프셋 보정
        texture = self.image.texture

        r,g,b  = self.color_mod
        SDL_SetTextureColorMod(texture, r, g, b)


        if self.flip == 'h':
            # 반전 시 offset_x를 반대로 적용
            adjusted_x = x - offset_x * scale
        else:
            adjusted_x = x + offset_x * scale

        adjusted_y = y + offset_y * scale

        screen_x , screen_y = game_framework.camera_manager.world_to_screen(
            adjusted_x, adjusted_y
        )

        self.image.clip_composite_draw(
            frame_info['x'],
            self.data['spriteSheetHeight'] - frame_info['y'] - frame_info['height'],
            frame_info['width'],
            frame_info['height'],
            0,  # 회전 각도
            self.flip,  # 'h' 또는 ''
            screen_x,
            screen_y,
            draw_width,
            draw_height
        )

        SDL_SetTextureColorMod(texture, 255, 255, 255)

    def set_stop_point(self, stop_point):
        """애니메이션이 멈출 프레임을 설정합니다."""
        if 0 <= stop_point < len(self.frames):
            self.stop_point = stop_point
        else:
            print(f"Warning: Invalid stop_point {stop_point}. Must be between 0 and {len(self.frames)-1}")

    def reset_stop_point(self):
        """stop_point를 마지막 프레임으로 재설정합니다."""
        self.stop_point = len(self.frames) - 1

    def is_animation_end(self):
        """애니메이션이 끝났는지 확인합니다."""
        return self.current_frame >= self.stop_point

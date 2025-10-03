from pico2d import *
import json


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
                'y' : sprite['y']
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
        self.frame_time = 0
        self.frame_delay = 0.1  # 각 프레임당 지속 시간 (초)

    def update(self,delta_time):
        """애니메이션 프레임을 업데이트합니다."""
        self.frame_time += delta_time
        if self.frame_time >= self.frame_delay:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self,x,y,scale=2):  # 2.5 대신 3으로 변경 (정수 배율)
        """애니메이션을 그립니다."""
        frame_info = self.frames[self.current_frame]
        # 정수 배율로 픽셀 아트 선명도 유지
        draw_width = int(frame_info['width'] * scale)
        draw_height = int(frame_info['height'] * scale)

        self.image.clip_draw(
            frame_info['x'],
            self.data['spriteSheetHeight'] - frame_info['y'] - frame_info['height'],  # Y좌표 뒤집기
            frame_info['width'],
            frame_info['height'],
            x,
            y,
            draw_width,
            draw_height
        )

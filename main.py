
from pico2d import *
import json


def load_animation_frames(json_path):
    """애니메이션 프레임 정보를 로드합니다."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    frames = []
    for sprite in data['sprites']:
        frame_info = {
            'fileName': sprite['fileName'],
            'width' : sprite['width'],
            'height': sprite['height'],
            'x' : sprite['x'],
            'y' : sprite['y']

        }
        frames.append(frame_info)

    frames.sort(key=lambda x: int(x['fileName'].split('_')[-1].split('.')[0]))
    return frames, data

# 프레임 정보 로드
frames, anim_data = load_animation_frames('sprites/Player/Texture2D/idle/penintent_idle_anim.json')
run_frames, run_anim_data = load_animation_frames('sprites/Player/Texture2D/Player_Run/penintent_start_run_anim.json')

# 프레임 정보 출력
print(f'총 프레임 수: {len(frames)}')
print(f'스프라이트 시트 크기: {anim_data["spriteSheetWidth"]} x {anim_data["spriteSheetHeight"]}')
print("\n프레임 정보:")

for i, frame in enumerate(frames):
    print(f"프레임 {i+1}: {frame['fileName']} (크기: {frame['width']}x{frame['height']}, 위치: ({frame['x']}, {frame['y']}))")

# Game object class here

class Penintent:
    def __init__(self):
        self.x, self.y = 400,90
        self.frame = 0
        self.image = load_image('sprites/Player/Texture2D/Player_Run/penintent_start_run_anim.png')
    def update(self):
        self.frame = (self.frame +1) % len(run_frames)

    def draw(self):
        frame_info = run_frames[self.frame]
        # 원본 비율 유지하면서 적절한 크기로 조정
        scale = 2.5  # 배율 조정
        draw_width = frame_info['width'] * scale
        draw_height = frame_info['height'] * scale

        self.image.clip_draw(
            frame_info['x'],
            run_anim_data['spriteSheetHeight'] - frame_info['y'] - frame_info['height'],  # Y좌표 뒤집기
            frame_info['width'],
            frame_info['height'],
            self.x,
            self.y,
            draw_width,
            draw_height
        )





def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False




def reset_world():
    global running
    global world
    running = True
    world = [] 
    penintent = Penintent()
    world.append(penintent)



def update_world():
    for game_object in world:
        game_object.update()

    pass
def render_world():
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()

running = True

open_canvas()

reset_world()
while running:
    handle_events()
    # 게임 로직
    update_world()
    render_world()
    delay(0.1)


close_canvas()




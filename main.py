from pico2d import *
from machine.animation import AnimationManager
from machine.animation import register_animations

from penintent import Penintent

# 먼저 canvas를 열어서 pico2d를 완전히 초기화 (픽셀 아트에 적합한 크기)
open_canvas(1024, 768)  # 더 큰 해상도로 설정

# 애니메이션 매니저 초기화
anim_manager = AnimationManager()

try:
    # 애니메이션 등록
    register_animations(anim_manager)
    print("애니메이션 등록 완료")
except Exception as e:
    print(f"애니메이션 등록 실패: {e}")


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_k:
                if world[0].current_animation != world[0].attack_animation:
                    world[0].current_animation = world[0].attack_animation
                    world[0].current_animation.current_frame = 0
                    world[0].current_animation.frame_time = 0

            elif event.key == SDLK_ESCAPE:
                running = False



def reset_world():
    global running
    global world
    running = True
    world = [] 
    penintent = Penintent(anim_manager)  # anim_manager 인자 추가
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

reset_world()
while running:
    handle_events()
    # 게임 로직
    update_world()
    render_world()
    delay(0.00005)

close_canvas()

from pico2d import *
from machine.key_manager import KeyManager

from machine.animation import AnimationManager
from machine.animation import register_animations
import game_world
import game_framework
from penintent import Penintent


# 애니메이션 매니저 초기화
anim_manager = None

# Key Manager 초기화
key_manager = None


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()




def init():
    global anim_manager, key_manager

    anim_manager = AnimationManager()
    key_manager = KeyManager()

    try:
        # 애니메이션 등록
        register_animations(anim_manager)
        print("애니메이션 등록 완료")
    except Exception as e:
        print(f"애니메이션 등록 실패: {e}")

    penintent = Penintent(anim_manager)  # anim_manager 인자 추가
    game_world.add_object(penintent,1)

def update():
    game_world.update()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass

from pico2d import *

from machine.animation import AnimationManager
from machine.animation import register_animations
import game_world
import game_framework
from Obj.UI.crisanta_bg import CrisantaBg
from Obj.UI.crisanta import Crisanta

import play_mode

# 애니메이션 매니저 초기화
anim_manager = None
floor_manager = None




def handle_events():

    if game_framework.key_manager.quit:
        game_framework.quit()


def init():
    global anim_manager, floor_manager

    game_framework.camera_manager.set_zoom(1.0)  # 3.0에서 2.0으로 조정 (너무 확대되면 문제 발생)


    anim_manager = AnimationManager()


    try:
        # 애니메이션 등록
        register_animations(anim_manager)
        print("애니메이션 등록 완료")
    except Exception as e:
        print(f"애니메이션 등록 실패: {e}")

    # 크리산타 배경 객체 생성 및 추가
    crisanta_bg = CrisantaBg(anim_manager)
    game_world.add_object(crisanta_bg, 0)

    crisanta = Crisanta(anim_manager)
    game_world.add_object(crisanta, 1)



def update():
    camera_speed = 5
    if game_framework.key_manager.is_down(SDLK_LEFT):
        game_framework.camera_manager.move(-camera_speed, 0)
    if game_framework.key_manager.is_down(SDLK_RIGHT):
        game_framework.camera_manager.move(camera_speed, 0)
    if game_framework.key_manager.is_down(SDLK_UP):
        game_framework.camera_manager.move(0, camera_speed)
    if game_framework.key_manager.is_down(SDLK_DOWN):
        game_framework.camera_manager.move(0, -camera_speed)
    if game_framework.key_manager.is_down(SDLK_p):
        game_framework.camera_manager.shake(10,0.5)
    if game_framework.key_manager.is_down(SDLK_SPACE):
        game_framework.change_mode(play_mode)

    game_world.update()

    # 충돌 체크는 game_framework에서 자동으로 실행됨 (중복 제거)

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

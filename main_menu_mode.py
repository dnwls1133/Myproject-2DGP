from pico2d import *

from machine.animation import AnimationManager
from machine.animation import register_animations
import game_world
import game_framework
import machine.collider_manager
from penintent import Penintent
from elderbrother import ElderBrother
from brotherhood_background_0 import BrotherhoodBackground0
from map_editor_mode import bg_tiles, terrain_tiles, decoration_tiles
from floor_object import FloorManager, FloorObject

from tilemap import TileMap

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
    if game_framework.key_manager.is_down(SDLK_ESCAPE):
        game_framework.quit()

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

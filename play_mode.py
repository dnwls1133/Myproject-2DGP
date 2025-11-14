from pico2d import *

from machine.animation import AnimationManager
from machine.animation import register_animations
import game_world
import game_framework
import machine.collider_manager
from penintent import Penintent
from brotherhood_background_0 import BrotherhoodBackground0
from map_editor_mode import bg_tiles, terrain_tiles, decoration_tiles


from tilemap import TileMap

# 애니메이션 매니저 초기화
anim_manager = None




def handle_events():

    if game_framework.key_manager.quit:
        game_framework.quit()


def init():
    global anim_manager
    game_framework.camera_manager.set_zoom(3.0)  # 원본 크기
    machine.collider_manager.clear_collision_pairs()

    anim_manager = AnimationManager()


    try:
        # 애니메이션 등록
        register_animations(anim_manager)
        print("애니메이션 등록 완료")
    except Exception as e:
        print(f"애니메이션 등록 실패: {e}")


    # 타일맵 로드
    tilemap_bg = TileMap()
    tilemap_bg.load_tile_images(bg_tiles)
    tilemap_bg.load_from_file('start_map_bg.json')
    game_world.add_object(tilemap_bg,1)

    tilemap_terrain = TileMap()
    tilemap_terrain.load_tile_images(terrain_tiles)
    tilemap_terrain.load_from_file('start_map.json')
    game_world.add_object(tilemap_terrain, 2)

    tilemap_deco = TileMap()
    tilemap_deco.load_tile_images(decoration_tiles)
    tilemap_deco.load_from_file('start_map_decoration.json')
    game_world.add_object(tilemap_deco, 3)


    penintent = Penintent(anim_manager)  # anim_manager 인자 추가
    game_world.add_object(penintent,4)



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
    game_world.update()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()
    machine.collider_manager.clear_collision_pairs()
def pause():
    pass

def resume():
    pass

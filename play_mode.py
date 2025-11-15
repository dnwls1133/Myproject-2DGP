from pico2d import *

from machine.animation import AnimationManager
from machine.animation import register_animations
import game_world
import game_framework
import machine.collider_manager
from penintent import Penintent
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
    game_framework.camera_manager.set_zoom(2.0)  # 3.0에서 2.0으로 조정 (너무 확대되면 문제 발생)
    machine.collider_manager.clear_collision_pairs()

    anim_manager = AnimationManager()


    try:
        # 애니메이션 등록
        register_animations(anim_manager)
        print("애니메이션 등록 완료")
    except Exception as e:
        print(f"애니메이션 등록 실패: {e}")


    # 타일맵 로드 (레이어 0: 배경)
    tilemap_bg = TileMap()
    tilemap_bg.load_tile_images(bg_tiles)
    tilemap_bg.load_from_file('start_map_bg.json')
    game_world.add_object(tilemap_bg, 0)
    print(f"배경 타일맵 로드 완료 (그리드: {len([t for row in tilemap_bg.tiles for t in row if t > 0])}개, 자유: {len(tilemap_bg.free_tiles)}개)")

    # 타일맵 로드 (레이어 1: 지형)
    tilemap_terrain = TileMap()
    tilemap_terrain.load_tile_images(terrain_tiles)
    tilemap_terrain.load_from_file('start_map.json')
    game_world.add_object(tilemap_terrain, 2)
    print(f"지형 타일맵 로드 완료 (그리드: {len([t for row in tilemap_terrain.tiles for t in row if t > 0])}개, 자유: {len(tilemap_terrain.free_tiles)}개)")


    # 타일맵 로드 (레이어 3: 장식 - 플레이어 위에 그려질 수 있음)
    tilemap_deco = TileMap()
    tilemap_deco.load_tile_images(decoration_tiles)
    tilemap_deco.load_from_file('start_map_decoration.json')
    game_world.add_object(tilemap_deco, 1)
    print(f"장식 타일맵 로드 완료 (그리드: {len([t for row in tilemap_deco.tiles for t in row if t > 0])}개, 자유: {len(tilemap_deco.free_tiles)}개)")

    # FloorManager 생성 및 바닥 객체 로드
    floor_manager = FloorManager()
    try:
        import json
        with open('start_map_floors.json', 'r', encoding='utf-8') as f:
            floor_data = json.load(f)
            floor_manager.load_from_dict(floor_data)
    except FileNotFoundError:
        print("바닥 파일이 없습니다. 기본 바닥을 생성합니다.")
        # 기본 바닥 생성 (테스트용)
        floor1 = FloorObject(400, 100, 800, 50, 'ground')
        floor_manager.add_floor(floor1)
        print("기본 바닥 생성 완료")

    game_world.add_object(floor_manager, 2)

    # 플레이어 (레이어 2: 타일보다 위에 그려지도록)
    penintent = Penintent(anim_manager)
    # 플레이어에게 타일맵 참조 전달
    penintent.terrain_tilemap = tilemap_terrain
    penintent.decoration_tilemap = tilemap_deco
    game_world.add_object(penintent, 2)
    print(f"플레이어 생성 완료: 위치 ({penintent.x}, {penintent.y})")

    # 충돌 페어 등록: 플레이어 vs 바닥
    for floor in floor_manager.get_all_floors():
        machine.collider_manager.add_collision_pair('player:floor', penintent, floor)

    print(f"충돌 페어 등록 완료: player:floor ({len(floor_manager.get_all_floors())}개 바닥)")

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

    # 충돌 체크 실행
    machine.collider_manager.check_all_collisions()

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

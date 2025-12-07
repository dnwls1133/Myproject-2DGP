from pico2d import *

from machine.animation import AnimationManager
from machine.animation import register_animations
import game_world
import game_framework
import machine.collider_manager
#from penintent import Penintent
from elderbrother import ElderBrother
from brotherhood_background_0 import BrotherhoodBackground0
from map_editor_mode import bg_tiles, terrain_tiles, decoration_tiles, fg_tiles
from floor_object import FloorManager, FloorObject
from Obj.UI.penient_life_ui import Penient_life_ui
from Obj.UI.health import Health
from Obj.UI.death_screen_title import DeathScreenTitle

from tilemap import TileMap

from wall import Wall

import common

# 애니메이션 매니저 초기화
anim_manager = None
floor_manager = None
bgm = None
fade_alpha = 255  # 페이드인 효과용
fade_speed = 300  # 초당 alpha 감소량
black_screen = None
elderbrother = None
bgm_on = False
penintent_death = False
boss_death = False
def handle_events():

    if game_framework.key_manager.quit:
        game_framework.quit()


def init():
    from penintent import Penintent

    global anim_manager, floor_manager,bgm, fade_alpha, black_screen, elderbrother
    fade_alpha = 255

    # 검은 화면 이미지 로드
    black_screen = load_image('black_screen.png')

    bgm = load_music('music\Dame_Tu_Tormento.mp3')
    game_framework.camera_manager.set_world_size(1800,1000)
    game_framework.camera_manager.set_zoom(3.0)  # 3.0에서 2.0으로 조정 (너무 확대되면 문제 발생)
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
    tilemap_bg.load_from_file('map/boss_bg.json')
    game_world.add_object(tilemap_bg, 0)
    print(f"배경 타일맵 로드 완료 (그리드: {len([t for row in tilemap_bg.tiles for t in row if t > 0])}개, 자유: {len(tilemap_bg.free_tiles)}개)")

    # 타일맵 로드 (레이어 1: 지형)
    tilemap_terrain = TileMap()
    tilemap_terrain.load_tile_images(terrain_tiles)
    tilemap_terrain.load_from_file('map/boss_terrain.json')
    game_world.add_object(tilemap_terrain, 2)
    print(f"지형 타일맵 로드 완료 (그리드: {len([t for row in tilemap_terrain.tiles for t in row if t > 0])}개, 자유: {len(tilemap_terrain.free_tiles)}개)")


    # 타일맵 로드 (레이어 3: 장식 - 플레이어 위에 그려질 수 있음)
    tilemap_deco = TileMap()
    tilemap_deco.load_tile_images(decoration_tiles)
    tilemap_deco.load_from_file('map/boss_decoration.json')
    game_world.add_object(tilemap_deco, 1)
    print(f"장식 타일맵 로드 완료 (그리드: {len([t for row in tilemap_deco.tiles for t in row if t > 0])}개, 자유: {len(tilemap_deco.free_tiles)}개)")

    tilemap_fg = TileMap()
    tilemap_fg.load_tile_images(fg_tiles)
    tilemap_fg.load_from_file('map/boss_foreground.json')
    game_world.add_object(tilemap_fg, 5)
    print(f"전경 타일맵 로드 완료 (그리드: {len([t for row in tilemap_fg.tiles for t in row if t > 0])}개, 자유: {len(tilemap_fg.free_tiles)}개)")

    # FloorManager 생성 및 바닥 객체 로드
    floor_manager = FloorManager()
    try:
        floor_manager = FloorManager.load_from_file('map/boss_floor.json')
        print(f"바닥 정보 로드 완료: {len(floor_manager.floors)}개")
    except FileNotFoundError:
        print("바닥 파일이 없습니다. 기본 바닥을 생성합니다.")
        # 기본 바닥 생성 (테스트용)
        floor1 = FloorObject(400, 100, 800, 50, 'ground')
        floor_manager.add_floor(floor1)
        print("기본 바닥 생성 완료")
    except Exception as e:
        print(f"바닥 파일 로드 실패: {e}")
        floor_manager = FloorManager()

    game_world.add_object(floor_manager, 2)

    elderbrother = ElderBrother(anim_manager)
    game_world.add_object(elderbrother, 0)
    print(f"형님 생성 완료: 위치 ({elderbrother.x}, {elderbrother.y})")
    for i in range(elderbrother.hp):
        health = Health(100, 50,i,elderbrother)
        game_world.add_object(health, 5)
    # 플레이어 (레이어 2: 타일보다 위에 그려지도록)
    common.penintent = Penintent(anim_manager,10,200)
    # 플레이어에게 타일맵 참조 전달
    common.penintent.terrain_tilemap = tilemap_terrain
    common.penintent.decoration_tilemap = tilemap_deco
    # ✅ 상태 명시적 초기화
    common.penintent.x = 10
    common.penintent.y = 200
    common.penintent.vx = 0
    common.penintent.vy = 0
    common.penintent.is_grounded = False
    common.penintent.state_machine.current_state = common.penintent.IDLE
    common.penintent.set_animation('idle')
    game_world.add_object(common.penintent, 3)
    print(f"플레이어 생성 완료: 위치 ({common.penintent.x}, {common.penintent.y})")


    wall = Wall(-20,300,10,1000)
    game_world.add_object(wall,2)
    machine.collider_manager.add_collision_pair('player:wall', common.penintent, wall)

    # 충돌 페어 등록 : 플레이어 공격 -> 엘더 형님 본체
    machine.collider_manager.add_collision_pair(
        'player_attack:elderBrother',
        common.penintent,
        elderbrother
    )

    # 충돌 페어 등록 : 엘더 형님 공격 -> 플레이어 본체
    machine.collider_manager.add_collision_pair(
        'elderBrother_attack:player',
        elderbrother,
        common.penintent
    )

    print("충돌 페어 등록 완료")

    # 충돌 페어 등록 : 플레이어 본체 -> 모든 바닥
    for floor in floor_manager.get_all_floors():
        machine.collider_manager.add_collision_pair('player:floor', common.penintent, floor)

    print(f"충돌 페어 등록 완료: player:floor ({len(floor_manager.get_all_floors())}개 바닥)")

    penitent_life_ui = Penient_life_ui()
    game_world.add_object(penitent_life_ui, 6)
    for i in range(common.penintent.hp):
        health = Health(penitent_life_ui.x , penitent_life_ui.y,i,common.penintent)
        game_world.add_object(health, 5)

    #bgm.repeat_play()

    #bgm.set_volume(64)


def update():
    global fade_alpha, elderbrother, bgm_on, penintent_death, boss_death
    import main_menu_mode
    if elderbrother.is_opening == False and bgm_on == False:
        bgm_on = True
        bgm.repeat_play()
        bgm.set_volume(64)
        game_framework.camera_manager.set_zoom(2.0)
    if common.penintent.is_dead and penintent_death == False:
        penintent_death = True
        death_screen = DeathScreenTitle()
        game_world.add_object(death_screen,7)
        game_framework.camera_manager.set_zoom(3.0)  # 3.0에서 2.0으로 조정 (너무 확대되면 문제 발생)


    # 페이드인 효과
    if fade_alpha > 0:
        fade_alpha -= fade_speed * game_framework.time_manager.get_fixed_dt()
        if fade_alpha < 0:
            fade_alpha = 0
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
    if game_framework.key_manager.is_down(SDLK_RETURN) and common.penintent.is_dead:
        game_framework.change_mode(main_menu_mode)
    if fade_alpha == 0:
        game_world.update()


    # 충돌 체크는 game_framework에서 자동으로 실행됨 (중복 제거)

def draw():
    clear_canvas()
    game_world.render()

    # 페이드 효과
    if fade_alpha > 0 and black_screen:
        canvas_w = get_canvas_width()
        canvas_h = get_canvas_height()
        black_screen.opacify(fade_alpha / 255.0)
        black_screen.draw(canvas_w // 2, canvas_h // 2, canvas_w, canvas_h)

    update_canvas()

def finish():
    global bgm, bgm_on, penintent_death, boss_death
    game_world.clear()
    machine.collider_manager.clear_collision_pairs()
    if bgm:
        bgm.stop()
    bgm_on = False
    penintent_death = False
    boss_death = False

def pause():
    pass

def resume():
    pass

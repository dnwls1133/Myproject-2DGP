from pico2d import *
import game_framework
from tilemap import TileMap
import ctypes

# SDL 마우스 상태 함수 가져오기
SDL_GetMouseState = ctypes.CDLL('SDL2.dll').SDL_GetMouseState
SDL_GetMouseState.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
SDL_GetMouseState.restype = ctypes.c_uint32

# 레이어별 타일맵
tilemap_bg = None
tilemap_decoration = None
tilemap_terrain = None

camera_x, camera_y = 0, 0
selected_tile = 1
mouse_x, mouse_y = 0, 0
is_dragging = False  # 드래그 상태
dragging_button = None  # 드래그 중인 버튼 (SDL_BUTTON_LEFT 또는 SDL_BUTTON_RIGHT)
# 그리드 크기 (편집 규칙: 그리드는 고정 크기)
grid_size = 32  # 그리드 크기
# 현재 레이어: 'background', 'decoration', 'terrain'
current_layer = 'terrain'

# 자유 배치 모드 관련 변수
free_placement_mode = False  # 자유 배치 모드
tile_scale = 1.0  # 타일 크기 배율
tile_rotation = 0  # 타일 회전 각도 (도)
tile_flip_x = False # X축 반전
tile_flip_y = False # Y축 반전


# Undo/Redo 시스템
undo_stack = []  # 되돌리기 스택
redo_stack = []  # 다시 실행 스택
max_undo_steps = 50  # 최대 되돌리기 단계

# 예시 타일 설정: 실제로 더 많은 타일을 로드하세요
bg_tiles = {
    1: {'path': 'sprites/map/Texture2D/Background/brotherhood-background-beginning_0.png', 'solid': False},
    2: {'path': 'sprites/map/Texture2D/Background/brotherhood-background-beginning_1.png', 'solid': False},
    3: {'path': 'sprites/map/Texture2D/Background/brotherhood-background-beginning_2.png', 'solid': False},
    4: {'path': 'sprites/map/Texture2D/Background/brotherhood-background-beginning_3.png', 'solid': False},
    5: {'path': 'sprites/map/Texture2D/Background/brotherhood-background-beginning_4.png', 'solid': False},
    6: {'path': 'sprites/map/Texture2D/Background/brotherhood-background-beginning_5.png', 'solid': False},
    7: {'path': 'sprites/map/Texture2D/Background/brotherhood-background-beginning_6.png', 'solid': False},
    8: {'path': 'sprites/map/Texture2D/Background/Sprite/background-boss-background_0.png', 'solid': False},
    9: {'path': 'sprites/map/Texture2D/Background/Sprite/background-boss-background_1.png', 'solid': False},
    10: {'path': 'sprites/map/Texture2D/Background/Sprite/background-boss-background_2.png', 'solid': False},
    11: {'path': 'sprites/map/Texture2D/Background/Sprite/background-boss-background_3.png', 'solid': False},
    12: {'path': 'sprites/map/Texture2D/Background/Sprite/background-boss-background_4.png', 'solid': False},
    13: {'path': 'sprites/map/Texture2D/Background/Sprite/background-boss-background_5.png', 'solid': False},
    15: {'path': 'sprites/map/Texture2D/Background/Sprite/brotherhodd-start-background_1.png', 'solid': False},
    14: {'path': 'sprites/map/Texture2D/Background/Sprite/brotherhodd-start-background_0.png', 'solid': False},
    16: {'path': 'sprites/map/Texture2D/Background/Sprite/brotherhodd-start-background_2.png', 'solid': False},
    17: {'path': 'sprites/map/Texture2D/Background/Sprite/brotherhodd-start-background_3.png', 'solid': False},
    18: {'path': 'sprites/map/Texture2D/Background/Sprite/brotherhodd-start-background_4.png', 'solid': False},
    19: {'path': 'sprites/map/Texture2D/Background/Sprite/brotherhodd-start-background_5.png', 'solid': False}

}

decoration_tiles = {
    1: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_0.png', 'solid': True},
    2: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_1.png', 'solid': True},
    3: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_2.png', 'solid': True},
    4: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_3.png', 'solid': True},
    5: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_4.png', 'solid': True},
    6: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_5.png', 'solid': True},
    7: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_6.png', 'solid': True},
    8: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_7.png', 'solid': True},
    9: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_8.png', 'solid': True},
    10: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_9.png', 'solid': True},
    11: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_10.png', 'solid': True},
    12: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_11.png', 'solid': True},
    13: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_12.png', 'solid': True},
    14: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_13.png', 'solid': True},
    15: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_15.png', 'solid': True},
    16: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_17.png', 'solid': True},
    17: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_18.png', 'solid': True},
    18: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_20.png', 'solid': True},
    19: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_21.png', 'solid': True},
    20: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_27.png', 'solid': False},
    21: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_28.png', 'solid': True},
    22: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_31.png', 'solid': True},
    23: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_32.png', 'solid': True},
    24: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_33.png', 'solid': True},
    25: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_34.png', 'solid': True},
    26: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_35.png', 'solid': True},
    27: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_36.png', 'solid': True},
    28: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_37.png', 'solid': True},
    29: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_38.png', 'solid': True},
    30: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_39.png', 'solid': True},
    31: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_40.png', 'solid': True},
    32: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_41.png', 'solid': True},
    33: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_42.png', 'solid': True},
    34: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_43.png', 'solid': True},
    35: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_44.png', 'solid': True},
    36: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_45.png', 'solid': True},
    37: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_46.png', 'solid': True},
    38: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_47.png', 'solid': True},
    39: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_48.png', 'solid': True},
    40: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_49.png', 'solid': True},
    41: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_50.png', 'solid': True},
    42: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_51.png', 'solid': True},
    43: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_52.png', 'solid': True},
    44: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_53.png', 'solid': True},
    45: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_54.png', 'solid': True},
    46: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_55.png', 'solid': True},
    47: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_56.png', 'solid': True},
    48: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_57.png', 'solid': True}
}

# terrain_tiles 수동 할당 (실제 존재하는 파일들)
terrain_tiles = {
    1: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_0.png', 'solid': True},
    2: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_1.png', 'solid': True},
    3: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_2.png', 'solid': True},
    4: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_3.png', 'solid': True},
    5: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_4.png', 'solid': True},
    6: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_5.png', 'solid': True},
    7: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_6.png', 'solid': True},
    8: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_7.png', 'solid': True},
    9: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_8.png', 'solid': True},
    10: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_9.png', 'solid': True},
    11: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_10.png', 'solid': True},
    12: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_11.png', 'solid': True},
    13: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_12.png', 'solid': True},
    14: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_13.png', 'solid': True},
    15: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_15.png', 'solid': True},
    16: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_17.png', 'solid': True},
    17: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_18.png', 'solid': True},
    18: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_20.png', 'solid': True},
    19: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_21.png', 'solid': True},
    20: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_27.png', 'solid': True},
    21: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_28.png', 'solid': True},
    22: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_31.png', 'solid': True},
    23: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_32.png', 'solid': True},
    24: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_33.png', 'solid': True},
    25: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_34.png', 'solid': True},
    26: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_35.png', 'solid': True},
    27: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_36.png', 'solid': True},
    28: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_37.png', 'solid': True},
    29: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_38.png', 'solid': True},
    30: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_39.png', 'solid': True},
    31: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_40.png', 'solid': True},
    32: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_41.png', 'solid': True},
    33: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_42.png', 'solid': True},
    34: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_43.png', 'solid': True},
    35: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_44.png', 'solid': True},
    36: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_45.png', 'solid': True},
    37: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_46.png', 'solid': True},
    38: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_47.png', 'solid': True},
    39: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_48.png', 'solid': True},
    40: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_49.png', 'solid': True},
    41: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_50.png', 'solid': True},
    42: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_51.png', 'solid': True},
    43: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_52.png', 'solid': True},
    44: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_53.png', 'solid': True},
    45: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_54.png', 'solid': True},
    46: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_55.png', 'solid': True},
    47: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_56.png', 'solid': True},
    48: {'path': 'sprites/map/Texture2D/Sprite/brotherhood-spritesheet_57.png', 'solid': True}
}

print(f"로드된 terrain 타일 개수: {len(terrain_tiles)}")

layer_depths = {
    'background': 0,
    'decoration' : 10,
    'terrain': 20
}

# 서브레이어 개념 추가 (같은 레이어 내에서도 깊이 구분)
sub_layer_depth = 0  # 현재 선택된 서브레이어 깊이 (0~9)



def get_current_tilemap():
    if current_layer == 'background':
        return tilemap_bg
    if current_layer == 'decoration':
        return tilemap_decoration
    return tilemap_terrain


def init():
    global tilemap_bg, tilemap_decoration, tilemap_terrain

    # 배경 레이어 (주로 큰 배경 이미지 여러장)
    tilemap_bg = TileMap(grid_size, grid_size)
    tilemap_bg.create_empty_map(50, 30)

    # 장식 레이어 (전경/배경 장식, 충돌 없음)
    tilemap_decoration = TileMap(grid_size, grid_size)
    tilemap_decoration.create_empty_map(50, 30)

    # 지형 레이어 (플레이어가 밟는 땅 등, 충돌 체크용)
    tilemap_terrain = TileMap(grid_size, grid_size)
    tilemap_terrain.create_empty_map(50, 30)



    tilemap_bg.load_tile_images(bg_tiles)
    tilemap_decoration.load_tile_images(decoration_tiles)
    tilemap_terrain.load_tile_images(terrain_tiles)

    game_framework.camera_manager.set_zoom(1.0)

def finish():
    global tilemap_bg, tilemap_decoration, tilemap_terrain
    tilemap_bg = None
    tilemap_decoration = None
    tilemap_terrain = None


def save_all():
    # 레이어별로 파일 분리 저장
    global tilemap_bg, tilemap_decoration, tilemap_terrain
    if tilemap_bg:
        tilemap_bg.save_to_file('map_bg.json')
    if tilemap_decoration:
        tilemap_decoration.save_to_file('map_decoration.json')
    if tilemap_terrain:
        tilemap_terrain.save_to_file('map_terrain.json')
    print('모든 레이어 저장 완료')


def load_all():
    try:
        if tilemap_bg:
            tilemap_bg.load_from_file('map_bg.json')
    except Exception:
        pass
    try:
        if tilemap_decoration:
            tilemap_decoration.load_from_file('map_decoration.json')
    except Exception:
        pass
    try:
        if tilemap_terrain:
            tilemap_terrain.load_from_file('map_terrain.json')
    except Exception:
        pass
    print('가능한 레이어 로드 완료')


def set_tile_with_depth(tilemap,tile_x,tile_y,tile_id,depth):
    tilemap.set_tile(tile_x,tile_y,tile_id)
    tilemap.set_tile_depth(tile_x,tile_y,depth)

def save_state_to_undo():
    """현재 상태를 Undo 스택에 저장"""
    global undo_stack, redo_stack
    import copy

    # 현재 상태 저장
    state = {
        'layer': current_layer,
        'bg_tiles': copy.deepcopy(tilemap_bg.tiles) if tilemap_bg else None,
        'bg_depths': copy.deepcopy(tilemap_bg.tile_depths) if tilemap_bg else None,
        'bg_free': copy.deepcopy(tilemap_bg.free_tiles) if tilemap_bg else None,
        'deco_tiles': copy.deepcopy(tilemap_decoration.tiles) if tilemap_decoration else None,
        'deco_depths': copy.deepcopy(tilemap_decoration.tile_depths) if tilemap_decoration else None,
        'deco_free': copy.deepcopy(tilemap_decoration.free_tiles) if tilemap_decoration else None,
        'terrain_tiles': copy.deepcopy(tilemap_terrain.tiles) if tilemap_terrain else None,
        'terrain_depths': copy.deepcopy(tilemap_terrain.tile_depths) if tilemap_terrain else None,
        'terrain_free': copy.deepcopy(tilemap_terrain.free_tiles) if tilemap_terrain else None,
    }

    undo_stack.append(state)

    # 최대 개수 제한
    if len(undo_stack) > max_undo_steps:
        undo_stack.pop(0)

    # 새로운 작업이 발생하면 redo 스택 초기화
    redo_stack.clear()

def undo():
    """이전 상태로 되돌리기"""
    global undo_stack, redo_stack
    import copy

    if not undo_stack:
        print("되돌릴 수 없습니다.")
        return

    # 현재 상태를 redo 스택에 저장
    current_state = {
        'layer': current_layer,
        'bg_tiles': copy.deepcopy(tilemap_bg.tiles) if tilemap_bg else None,
        'bg_depths': copy.deepcopy(tilemap_bg.tile_depths) if tilemap_bg else None,
        'bg_free': copy.deepcopy(tilemap_bg.free_tiles) if tilemap_bg else None,
        'deco_tiles': copy.deepcopy(tilemap_decoration.tiles) if tilemap_decoration else None,
        'deco_depths': copy.deepcopy(tilemap_decoration.tile_depths) if tilemap_decoration else None,
        'deco_free': copy.deepcopy(tilemap_decoration.free_tiles) if tilemap_decoration else None,
        'terrain_tiles': copy.deepcopy(tilemap_terrain.tiles) if tilemap_terrain else None,
        'terrain_depths': copy.deepcopy(tilemap_terrain.tile_depths) if tilemap_terrain else None,
        'terrain_free': copy.deepcopy(tilemap_terrain.free_tiles) if tilemap_terrain else None,
    }
    redo_stack.append(current_state)

    # 이전 상태 복원
    prev_state = undo_stack.pop()
    restore_state(prev_state)
    print(f"Undo 실행 (남은 Undo: {len(undo_stack)})")

def redo():
    """다시 실행"""
    global undo_stack, redo_stack
    import copy

    if not redo_stack:
        print("다시 실행할 수 없습니다.")
        return

    # 현재 상태를 undo 스택에 저장
    current_state = {
        'layer': current_layer,
        'bg_tiles': copy.deepcopy(tilemap_bg.tiles) if tilemap_bg else None,
        'bg_depths': copy.deepcopy(tilemap_bg.tile_depths) if tilemap_bg else None,
        'bg_free': copy.deepcopy(tilemap_bg.free_tiles) if tilemap_bg else None,
        'deco_tiles': copy.deepcopy(tilemap_decoration.tiles) if tilemap_decoration else None,
        'deco_depths': copy.deepcopy(tilemap_decoration.tile_depths) if tilemap_decoration else None,
        'deco_free': copy.deepcopy(tilemap_decoration.free_tiles) if tilemap_decoration else None,
        'terrain_tiles': copy.deepcopy(tilemap_terrain.tiles) if tilemap_terrain else None,
        'terrain_depths': copy.deepcopy(tilemap_terrain.tile_depths) if tilemap_terrain else None,
        'terrain_free': copy.deepcopy(tilemap_terrain.free_tiles) if tilemap_terrain else None,
    }
    undo_stack.append(current_state)

    # Redo 상태 복원
    next_state = redo_stack.pop()
    restore_state(next_state)
    print(f"Redo 실행 (남은 Redo: {len(redo_stack)})")

def restore_state(state):
    """저장된 상태 복원"""
    global current_layer
    import copy

    if tilemap_bg and state['bg_tiles'] is not None:
        tilemap_bg.tiles = copy.deepcopy(state['bg_tiles'])
        tilemap_bg.tile_depths = copy.deepcopy(state['bg_depths'])
        tilemap_bg.free_tiles = copy.deepcopy(state['bg_free'])

    if tilemap_decoration and state['deco_tiles'] is not None:
        tilemap_decoration.tiles = copy.deepcopy(state['deco_tiles'])
        tilemap_decoration.tile_depths = copy.deepcopy(state['deco_depths'])
        tilemap_decoration.free_tiles = copy.deepcopy(state['deco_free'])

    if tilemap_terrain and state['terrain_tiles'] is not None:
        tilemap_terrain.tiles = copy.deepcopy(state['terrain_tiles'])
        tilemap_terrain.tile_depths = copy.deepcopy(state['terrain_depths'])
        tilemap_terrain.free_tiles = copy.deepcopy(state['terrain_free'])

    current_layer = state['layer']
def handle_events():
    global selected_tile, mouse_x, mouse_y, camera_x, camera_y, is_dragging, current_layer, dragging_button, sub_layer_depth
    global free_placement_mode, tile_scale, tile_rotation, tile_flip_x, tile_flip_y


    # 캔버스 크기 가져오기
    canvas_width, canvas_height = get_canvas_width(), get_canvas_height()


    # 실제 마우스 버튼 상태 체크
    mouse_state_x = ctypes.c_int()
    mouse_state_y = ctypes.c_int()
    button_state = SDL_GetMouseState(ctypes.byref(mouse_state_x), ctypes.byref(mouse_state_y))

    # 좌클릭과 우클릭 상태 확인
    left_button_pressed = button_state & 0x01  # SDL_BUTTON_LEFT
    right_button_pressed = button_state & 0x04  # SDL_BUTTON_RIGHT

    # 버튼이 떼어졌는지 체크
    if is_dragging and not left_button_pressed and not right_button_pressed:
        is_dragging = False
        dragging_button = None

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()

            # Ctrl 키 상태 확인
            ctrl_held = SDL_GetModState() & KMOD_CTRL
            shift_held = SDL_GetModState() & KMOD_SHIFT

            # Ctrl+S: 저장 / Ctrl+Shift+S: 다른 이름으로 저장
            if event.key == SDLK_s and ctrl_held:
                cur = get_current_tilemap()
                if cur:
                    if shift_held:
                        if cur.save_map_as():
                            print(f"{current_layer} 레이어 다른 이름으로 저장 완료")
                    else:
                        if cur.save_map():
                            print(f"{current_layer} 레이어 저장 완료")

            # Ctrl+O: 불러오기
            elif event.key == SDLK_o and ctrl_held:
                cur = get_current_tilemap()
                if cur and cur.load_map():
                    print(f"{current_layer} 레이어 불러오기 완료")

            # Ctrl+N: 새 맵
            elif event.key == SDLK_n and ctrl_held:
                cur = get_current_tilemap()
                if cur:
                    cur.new_map()
                    print(f"{current_layer} 레이어 새 맵 생성")

            # Ctrl+Z: Undo (되돌리기)
            elif event.key == SDLK_z and ctrl_held and not shift_held:
                undo()

            # Ctrl+Y 또는 Ctrl+Shift+Z: Redo (다시 실행)
            elif (event.key == SDLK_y and ctrl_held) or (event.key == SDLK_z and ctrl_held and shift_held):
                redo()

            elif event.key == SDLK_q:
                cur = get_current_tilemap()
                if cur and cur.tile_images:
                    max_tile = max(cur.tile_images.keys())
                    selected_tile = selected_tile - 1 if selected_tile > 1 else max_tile
                    print(f"선택된 타일: {selected_tile} (레이어: {current_layer})")
            elif event.key == SDLK_e:
                cur = get_current_tilemap()
                if cur and cur.tile_images:
                    max_tile = max(cur.tile_images.keys())
                    selected_tile = selected_tile + 1 if selected_tile < max_tile else 1
                    print(f"선택된 타일: {selected_tile} (레이어: {current_layer})")
            elif event.key == SDLK_TAB:
                # 레이어 순환: background -> decoration -> terrain -> background
                if current_layer == 'background':
                    current_layer = 'decoration'
                elif current_layer == 'decoration':
                    current_layer = 'terrain'
                else:
                    current_layer = 'background'
                print(f"현재 레이어: {current_layer}")
            elif event.key == SDLK_l and ctrl_held:
                clear_current_layer()
            elif event.key == SDLK_l and shift_held and ctrl_held:
                clear_all_layers()
            elif event.key == SDLK_UP:
                sub_layer_depth = min(9, sub_layer_depth + 1)
                print(f"서브레이어 깊이: {sub_layer_depth}")
            elif event.key == SDLK_DOWN:  # 깊이 감소
                sub_layer_depth = max(0, sub_layer_depth - 1)
                print(f"서브레이어 깊이: {sub_layer_depth}")

            # F 키: 자유 배치 모드 전환
            elif event.key == SDLK_f:
                free_placement_mode = not free_placement_mode
                print(f"자유 배치 모드: {'ON' if free_placement_mode else 'OFF'}")

            # [ ] 키: 타일 크기 조절
            elif event.key == SDLK_LEFTBRACKET:  # [ 키
                tile_scale = max(0.25, tile_scale - 0.25)
                print(f"타일 크기: {tile_scale}x")
            elif event.key == SDLK_RIGHTBRACKET:  # ] 키
                tile_scale = min(4.0, tile_scale + 0.25)
                print(f"타일 크기: {tile_scale}x")

            # , . 키 + Shift: 타일 회전
            elif event.key == SDLK_COMMA and shift_held:  # < 키 (Shift + ,)
                tile_rotation = (tile_rotation - 15) % 360
                print(f"타일 회전: {tile_rotation}도")
            elif event.key == SDLK_PERIOD and shift_held:  # > 키 (Shift + .)
                tile_rotation = (tile_rotation + 15) % 360
                print(f"타일 회전: {tile_rotation}도")

            # R 키: 타일 변형 초기화
            elif event.key == SDLK_r:
                tile_scale = 1.0
                tile_rotation = 0
                tile_flip_x = False
                tile_flip_y = False
                print("타일 변형 초기화")

            elif event.key == SDLK_x:
                tile_flip_x = not tile_flip_x
                print(f"타일 가로 뒤집기: {'ON' if tile_flip_x else 'OFF'}")

            elif event.key == SDLK_y:
                tile_flip_y = not tile_flip_y
                print(f"타일 세로 뒤집기: {'ON' if tile_flip_y else 'OFF'}")

        elif event.type == SDL_MOUSEMOTION:
            mouse_x, mouse_y = event.x, canvas_height - 1 - event.y

            if is_dragging and dragging_button is not None:
                cur = get_current_tilemap()
                if cur:
                    depth = layer_depths[current_layer] + sub_layer_depth

                    if free_placement_mode:
                        # 자유 배치: 픽셀 단위
                        world_x = mouse_x + camera_x
                        world_y = mouse_y + camera_y

                        if dragging_button == SDL_BUTTON_LEFT:
                            cur.add_free_tile(selected_tile, world_x, world_y, tile_scale, tile_rotation, depth,tile_flip_x, tile_flip_y)
                        elif dragging_button == SDL_BUTTON_RIGHT:
                            cur.remove_free_tile_at(world_x, world_y)
                    else:
                        # 그리드 배치
                        tile_x = (mouse_x + camera_x) // grid_size
                        tile_y = (mouse_y + camera_y) // grid_size

                        if dragging_button == SDL_BUTTON_LEFT:
                            set_tile_with_depth(cur,tile_x,tile_y,selected_tile,depth)
                        elif dragging_button == SDL_BUTTON_RIGHT:
                            cur.set_tile(tile_x, tile_y, 0)

        elif event.type == SDL_MOUSEBUTTONDOWN:
            # 마우스 버튼을 누르기 전에 현재 상태 저장 (Undo용)
            save_state_to_undo()

            is_dragging = True
            dragging_button = event.button
            mouse_x, mouse_y = event.x, canvas_height - 1 - event.y
            cur = get_current_tilemap()
            if cur:
                depth = layer_depths[current_layer] + sub_layer_depth

                if free_placement_mode:
                    # 자유 배치: 픽셀 단위
                    world_x = mouse_x + camera_x
                    world_y = mouse_y + camera_y

                    if event.button == SDL_BUTTON_LEFT:
                        cur.add_free_tile(selected_tile, world_x, world_y, tile_scale, tile_rotation, depth,tile_flip_x, tile_flip_y)
                    elif event.button == SDL_BUTTON_RIGHT:
                        cur.remove_free_tile_at(world_x, world_y)
                else:
                    # 그리드 배치
                    tile_x = (mouse_x + camera_x) // grid_size
                    tile_y = (mouse_y + camera_y) // grid_size

                    if event.button == SDL_BUTTON_LEFT:
                        set_tile_with_depth(cur, tile_x, tile_y, selected_tile, depth)
                    elif event.button == SDL_BUTTON_RIGHT:
                        cur.set_tile(tile_x, tile_y, 0)

        elif event.type == SDL_MOUSEBUTTONUP:
            is_dragging = False
            dragging_button = None

def clear_current_layer():
    """현재 레이어의 모든 타일을 지웁니다."""
    cur = get_current_tilemap()
    if cur:
        cur.new_map()
        print(f"{current_layer} 레이어 초기화 완료")


def clear_all_layers():
    """모든 레이어의 타일을 지웁니다."""
    global tilemap_bg, tilemap_decoration, tilemap_terrain
    if tilemap_bg:
        tilemap_bg.new_map()
    if tilemap_decoration:
        tilemap_decoration.new_map()
    if tilemap_terrain:
        tilemap_terrain.new_map()
    print("모든 레이어 초기화 완료")

def update():
    global camera_x, camera_y

    # WASD 키로 카메라 이동 (연속 이동)
    camera_speed = 10  # 카메라 이동 속도

    # SDL_GetKeyboardState로 현재 키 상태 확인
    from ctypes import c_int, POINTER, cast
    import ctypes

    # SDL 키보드 상태 가져오기
    SDL_GetKeyboardState = ctypes.CDLL('SDL2.dll').SDL_GetKeyboardState
    SDL_GetKeyboardState.argtypes = [POINTER(c_int)]
    SDL_GetKeyboardState.restype = POINTER(ctypes.c_uint8)

    num_keys = c_int(0)
    keyboard_state = SDL_GetKeyboardState(ctypes.byref(num_keys))

    # WASD 키 확인
    if keyboard_state[26]:  # W 키 (SDL_SCANCODE_W = 26)
        camera_y += camera_speed
    if keyboard_state[22]:  # S 키 (SDL_SCANCODE_S = 22)
        camera_y = max(0, camera_y - camera_speed)  # 0 이하로 내려가지 않도록
    if keyboard_state[4]:   # A 키 (SDL_SCANCODE_A = 4)
        camera_x = max(0, camera_x - camera_speed)  # 0 이하로 가지 않도록
    if keyboard_state[7]:   # D 키 (SDL_SCANCODE_D = 7)
        camera_x += camera_speed


def draw():
    clear_canvas()

    screen_w = get_canvas_width()
    screen_h = get_canvas_height()

    # 모든 레이어의 타일을 수집하여 깊이 기준으로 정렬
    all_tiles = []

    # 1. 배경 레이어 타일 수집
    if tilemap_bg:
        # 그리드 타일
        for y, row in enumerate(tilemap_bg.tiles):
            for x, tile_id in enumerate(row):
                if tile_id > 0:
                    depth = tilemap_bg.get_tile_depth(x, y)
                    all_tiles.append((depth, 'background', 'grid', x, y, tile_id))
        # 자유 배치 타일
        for free_tile in tilemap_bg.free_tiles:
            all_tiles.append((free_tile.depth, 'background', 'free', free_tile))

    # 2. 장식 레이어 타일 수집
    if tilemap_decoration:
        # 그리드 타일
        for y, row in enumerate(tilemap_decoration.tiles):
            for x, tile_id in enumerate(row):
                if tile_id > 0:
                    depth = tilemap_decoration.get_tile_depth(x, y)
                    all_tiles.append((depth, 'decoration', 'grid', x, y, tile_id))
        # 자유 배치 타일
        for free_tile in tilemap_decoration.free_tiles:
            all_tiles.append((free_tile.depth, 'decoration', 'free', free_tile))

    # 3. 지형 레이어 타일 수집
    if tilemap_terrain:
        # 그리드 타일
        for y, row in enumerate(tilemap_terrain.tiles):
            for x, tile_id in enumerate(row):
                if tile_id > 0:
                    depth = tilemap_terrain.get_tile_depth(x, y)
                    all_tiles.append((depth, 'terrain', 'grid', x, y, tile_id))
        # 자유 배치 타일
        for free_tile in tilemap_terrain.free_tiles:
            all_tiles.append((free_tile.depth, 'terrain', 'free', free_tile))

    # 깊이 기준으로 정렬 (낮은 값이 먼저 = 뒤에 그려짐)
    all_tiles.sort(key=lambda t: t[0])

    # 정렬된 순서대로 타일 그리기
    for item in all_tiles:
        depth = item[0]
        layer_name = item[1]
        tile_type = item[2]

        tilemap = get_tilemap_by_name(layer_name)
        if not tilemap:
            continue

        if tile_type == 'grid':
            # 그리드 타일
            tile_x, tile_y, tile_id = item[3], item[4], item[5]
            if tile_id in tilemap.tile_images:
                world_x = tile_x * grid_size + grid_size // 2
                world_y = tile_y * grid_size + grid_size // 2
                screen_x = world_x - camera_x
                screen_y = world_y - camera_y
                tilemap.tile_images[tile_id].draw(screen_x, screen_y)

        elif tile_type == 'free':
            # 자유 배치 타일
            free_tile = item[3]
            if free_tile.tile_id in tilemap.tile_images:
                screen_x = free_tile.x - camera_x
                screen_y = free_tile.y - camera_y

                img = tilemap.tile_images[free_tile.tile_id]

                # 회전 각도를 라디안으로 변환
                rotation_rad = free_tile.rotation * 3.14159 / 180

                # 반전 문자열 생성
                flip_str = ''
                if free_tile.flip_x:
                    flip_str += 'h'  # horizontal flip
                if free_tile.flip_y:
                    flip_str += 'v'  # vertical flip

                img.composite_draw(
                    rotation_rad,
                    flip_str,
                    screen_x, screen_y,
                    int(img.w * free_tile.scale),
                    int(img.h * free_tile.scale)
                )

    # 선택된 타일 미리보기 (좌측 상단)
    cur = get_current_tilemap()
    if cur and selected_tile in cur.tile_images:
        cur.tile_images[selected_tile].draw(50, screen_h - 30)

    # 현재 상태 표시
    draw_text(f"Layer: {current_layer}", 10, screen_h - 60)
    draw_text(f"Sub-depth: {sub_layer_depth}", 10, screen_h - 80)
    draw_text(f"Total depth: {layer_depths[current_layer] + sub_layer_depth}", 10, screen_h - 100)
    draw_text(f"Mode: {'FREE' if free_placement_mode else 'GRID'}", 10, screen_h - 120)
    draw_text(f"Scale: {tile_scale}x", 10, screen_h - 140)
    draw_text(f"Rotation: {tile_rotation}°", 10, screen_h - 160)

    # 마우스 프리뷰 (변형 적용)
    if cur and selected_tile in cur.tile_images:
        if free_placement_mode:
            # 자유 배치: 마우스 위치 그대로
            preview_x = mouse_x
            preview_y = mouse_y
        else:
            # 그리드 배치: 스냅된 위치
            tile_x = (mouse_x + camera_x) // grid_size
            tile_y = (mouse_y + camera_y) // grid_size
            world_px = tile_x * grid_size + grid_size // 2
            world_py = tile_y * grid_size + grid_size // 2
            preview_x = world_px - camera_x
            preview_y = world_py - camera_y

        img = cur.tile_images[selected_tile]
        rotation_rad = tile_rotation * 3.14159 / 180

        flip_str = ''
        if tile_flip_x:
            flip_str += 'h'
        if tile_flip_y:
            flip_str += 'v'

        img.opacify(0.5)
        img.composite_draw(
            rotation_rad,
            flip_str,  # 반전 적용,
            preview_x, preview_y,
            int(img.w * tile_scale),
            int(img.h * tile_scale)
        )
        img.opacify(1.0)

    update_canvas()

def get_tilemap_by_name(layer_name):
    """레이어 이름으로 타일맵 객체 반환"""
    if layer_name == 'background':
        return tilemap_bg
    elif layer_name == 'decoration':
        return tilemap_decoration
    elif layer_name == 'terrain':
        return tilemap_terrain
    return None


def draw_text(text, x, y):
    """간단한 텍스트 렌더링 (pico2d에서는 기본 지원 안 함, PIL 필요)"""
    # 임시로 콘솔 출력으로 대체하거나, PIL/폰트 로드 필요
    pass

def pause():
    pass


def resume():
    pass
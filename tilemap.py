import json
import os
from tkinter import Tk,filedialog
from pico2d import *
import game_framework

class FreeTile:
    """자유 배치 타일 클래스"""
    def __init__(self, tile_id, x, y, scale=1.0, rotation=0, depth=0,flip_x=False, flip_y=False):
        self.tile_id = tile_id
        self.x = x  # 픽셀 단위 월드 좌표
        self.y = y
        self.scale = scale
        self.rotation = rotation
        self.depth = depth
        self.flip_x = flip_x
        self.flip_y = flip_y

class TileMap:
    def __init__(self,tile_width=32, tile_height=32):
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles = []
        self.tile_images = {}  # 타일 ID별 이미지
        self.tile_types = {}  # tile_type -> tile_types로 수정
        self.tile_sizes = {}  # 타일 ID별 크기 정보
        self.tile_depths = []  # 타일 ID별 깊이 정보
        self.map_width = 0
        self.map_height = 0
        self.current_file = None # 현재 작업 중인 파일 경로
        self.free_tiles = []  # 자유 배치 타일 목록


    def load_tile_images(self, tile_info):
        """개별 타일 이미지 로드"""
        for tile_id, info in tile_info.items():
            if 'path' in info:
                img = load_image(info['path'])
                self.tile_images[tile_id] = img
                self.tile_types[tile_id] = info

                # 각 타일의 실제 크기 저장
                self.tile_sizes[tile_id] = (img.w, img.h)
                print(f"타일 {tile_id}: {img.w} x {img.h}")

    def create_empty_map(self, width, height):
        """빈 타일맵 생성"""
        self.map_width = width
        self.map_height = height
        self.tiles = [[0 for _ in range(width)] for _ in range(height)]
        self.tile_depths = [[0 for _ in range(width)] for _ in range(height)]

    def set_tile(self, x, y, tile_id):
        """특정 위치에 타일 설정"""
        if 0 <= y < self.map_height and 0 <= x < self.map_width:
            self.tiles[y][x] = tile_id
    def set_tile_depth(self, x, y, depth):
        if 0 <= y < len(self.tile_depths) and 0 <= x < len(self.tile_depths[0]):
            self.tile_depths[y][x] = depth

    def get_tile_depth(self, x, y):
        """타일의 깊이값을 반환합니다."""
        if 0 <= y < len(self.tile_depths) and 0 <= x < len(self.tile_depths[0]):
            return self.tile_depths[y][x]
        return 0


    def get_tile(self, x, y):
        """특정 위치의 타일 ID 반환"""
        if 0 <= y < self.map_height and 0 <= x < self.map_width:
            return self.tiles[y][x]
        return None
    def get_tile_size(self, tile_id):
        """타일 ID에 해당하는 타일의 크기 반환"""
        return self.tile_sizes.get(tile_id, (32,32))

    def draw(self, ratio = 0.0, camera_y=0,scale=2.0,use_camera=True):
        """타일맵을 그립니다."""

        if use_camera:
            camera_x, camera_y = game_framework.camera_manager.get_position()

            # 윈도우-뷰포트 배율 계산
            viewport_scale_x = game_framework.camera_manager.screen_width / game_framework.camera_manager.window_width
            viewport_scale_y = game_framework.camera_manager.screen_height / game_framework.camera_manager.window_height
        else:
            # 에디터 모드: 카메라 사용 안함
            scale = 1.0
            viewport_scale_x = 1.0
            viewport_scale_y = 1.0

        # 모든 타일을 깊이 기준으로 수집
        all_tiles = []

        # 그리드 타일 수집
        for y, row in enumerate(self.tiles):
            for x, tile_id in enumerate(row):
                if tile_id > 0 and tile_id in self.tile_images:
                    depth = self.get_tile_depth(x, y)
                    all_tiles.append(('grid', depth, x, y, tile_id))

        # 자유 배치 타일 수집
        for tile in self.free_tiles:
            if tile.tile_id in self.tile_images:
                all_tiles.append(('free', tile.depth, tile))

        # 깊이 기준으로 정렬 (낮은 값이 먼저 = 뒤에 그려짐)
        all_tiles.sort(key=lambda t: t[1])

        # 정렬된 순서대로 그리기
        for item in all_tiles:
            tile_type = item[0]

            if tile_type == 'grid':
                # 그리드 타일
                _, depth, x, y, tile_id = item

                # 월드 좌표 계산
                world_x = x * self.tile_width + self.tile_width / 2
                world_y = y * self.tile_height + self.tile_height / 2

                if use_camera:
                    # 게임 모드: 카메라 변환 적용
                    screen_x, screen_y = game_framework.camera_manager.world_to_screen(world_x, world_y)
                else:
                    # 에디터 모드: 화면 좌표 그대로 사용
                    screen_x = world_x - camera_x
                    screen_y = world_y - camera_y

                img = self.tile_images[tile_id]

                # 윈도우-뷰포트 배율 적용된 크기
                draw_width = int(img.w * scale * viewport_scale_x)
                draw_height = int(img.h * scale * viewport_scale_y)

                img.composite_draw(
                    0,  # 회전 각도 (라디안)
                    '',  # 반전 옵션 ('h' 또는 'v')
                    screen_x, screen_y,  # 위치
                    draw_width, draw_height  # 크기
                )

            elif tile_type == 'free':
                # 자유 배치 타일
                _, depth, tile = item
                img = self.tile_images[tile.tile_id]

                # 월드 좌표
                world_x = tile.x
                world_y = tile.y

                if use_camera:
                    # 게임 모드: 카메라 변환 적용
                    screen_x, screen_y = game_framework.camera_manager.world_to_screen(world_x, world_y)

                    # 윈도우-뷰포트 배율 적용
                    draw_width = int(img.w * tile.scale * viewport_scale_x)
                    draw_height = int(img.h * tile.scale * viewport_scale_y)
                else:
                    # 에디터 모드: 화면 좌표 그대로 사용
                    screen_x = world_x - camera_x
                    screen_y = world_y - camera_y

                    draw_width = int(img.w * tile.scale)
                    draw_height = int(img.h * tile.scale)

                # 회전 각도를 라디안으로 변환
                rotation_rad = tile.rotation * 3.14159 / 180

                # 반전 문자열 생성
                flip_str = ''
                if tile.flip_x:
                    flip_str += 'h'  # horizontal flip
                if tile.flip_y:
                    flip_str += 'v'  # vertical flip

                img.composite_draw(
                    rotation_rad,  # 회전 각도 적용
                    flip_str,  # 반전 옵션 적용
                    screen_x, screen_y,  # 위치
                    draw_width, draw_height  # 크기
                )




    def save_map_as(self):
        """타일맵을 다른 이름으로 저장"""
        root = Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="맵 저장"
        )

        root.destroy()

        if file_path:
            self.current_file = file_path
            self.save_to_file(file_path)
            return True
        return False

    def save_map(self):
        if self.current_file:
            self.save_to_file(self.current_file)
            return True
        else:
            return self.save_map_as()

    def save_to_file(self, file_path):
        """타일맵을 JSON 파일로 저장"""
        """실제 파일 저장 로직"""
        data = {
            "tile_width": self.tile_width,
            "tile_height": self.tile_height,
            "map_width": self.map_width,
            "map_height": self.map_height,
            "tiles": self.tiles,
            "tile_depths": self.tile_depths,
            "tile_sizes": self.tile_sizes,
            "free_tiles": [  # 자유 배치 타일 정보 저장
                {
                    'tile_id': ft.tile_id,
                    'x': ft.x,
                    'y': ft.y,
                    'scale': ft.scale,
                    'rotation': ft.rotation,
                    'depth': ft.depth,
                    'flip_x': ft.flip_x,
                    'flip_y': ft.flip_y
                }
                for ft in self.free_tiles
            ]
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"맵 저장 완료: {file_path}")

    def load_map(self):
        """타일맵 불러오기 대화상자 표시"""
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="맵 불러오기"
        )

        root.destroy()

        if file_path and os.path.exists(file_path):
            return self.load_from_file(file_path)
        return False

    def load_from_file(self, file_path):
        """실제 파일 로드 로직"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.tile_width = data["tile_width"]
            self.tile_height = data["tile_height"]
            self.map_width = data["map_width"]
            self.map_height = data["map_height"]
            self.tiles = data["tiles"]
            self.tile_depths = data.get("tile_depths", [[0 for _ in range(self.map_width)] for _ in range(self.map_height)])
            self.tile_sizes = data.get("tile_sizes", {})

            # 자유 배치 타일 복원
            self.free_tiles = []
            if 'free_tiles' in data:
                for ft_data in data['free_tiles']:
                    free_tile = FreeTile(
                        tile_id=ft_data['tile_id'],
                        x=ft_data['x'],
                        y=ft_data['y'],
                        scale=ft_data.get('scale', 1.0),
                        rotation=ft_data.get('rotation', 0),
                        depth=ft_data.get('depth', 0),
                        flip_x=ft_data.get('flip_x', False),
                        flip_y=ft_data.get('flip_y', False)
                    )
                    self.free_tiles.append(free_tile)

            self.current_file = file_path

            print(f"맵 로드 완료: {file_path} (자유 타일: {len(self.free_tiles)}개)")
            return True
        except Exception as e:
            print(f"맵 로드 실패: {e}")
            return False

    def new_map(self):
        """새 맵 생성"""
        self.tiles = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.tile_depths = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.free_tiles = []  # 자유 배치 타일도 초기화
        self.current_file = None
        print("새 맵 생성 완료")

    def update(self):
        pass

    def add_free_tile(self, tile_id, x, y, scale=1.0, rotation=0, depth=0, flip_x=False, flip_y=False):
        """자유 배치 타일 추가"""
        tile = FreeTile(tile_id, x, y, scale, rotation, depth, flip_x, flip_y)
        self.free_tiles.append(tile)
        return tile

    def remove_free_tile_at(self, x, y, threshold=32):
        """특정 위치 근처의 자유 타일 제거"""
        for tile in self.free_tiles[:]:
            if abs(tile.x - x) < threshold and abs(tile.y - y) < threshold:
                self.free_tiles.remove(tile)
                return True
        return False

    def get_free_tile_at(self, x, y, threshold=32):
        """특정 위치 근처의 자유 타일 반환"""
        for tile in self.free_tiles:
            if abs(tile.x - x) < threshold and abs(tile.y - y) < threshold:
                return tile
        return None

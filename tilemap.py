import json
import os
from tkinter import Tk,filedialog
from pico2d import *
import game_framework



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

    def draw(self, camera_x=0, camera_y=0,scale=2.0,use_camera=True):
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


        for y, row in enumerate(self.tiles):
            for x, tile_id in enumerate(row):
                if tile_id > 0 and tile_id in self.tile_images:
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
            "tile_sizes": self.tile_sizes
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
            self.tile_sizes = data.get("tile_sizes", {})
            self.current_file = file_path

            print(f"맵 로드 완료: {file_path}")
            return True
        except Exception as e:
            print(f"맵 로드 실패: {e}")
            return False

    def new_map(self):
        """새 맵 생성"""
        self.tiles = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        self.current_file = None
        print("새 맵 생성 완료")

    def update(self):
        pass
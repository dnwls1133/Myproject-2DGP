from pico2d import *
import game_framework


class BrotherhoodBackground0:
    def __init__(self):
        self.image = load_image("sprites/map/texture2d/brotherhood-background-beginning_0.png")
        self.img_width = 630
        self.img_height = 776

        # ✅ 확대 배율 설정 (예: 3배)
        self.scale = 3.0
        self.scaled_width = int(self.img_width * self.scale)
        self.scaled_height = int(self.img_height * self.scale)


    def update(self):
        pass


    def draw(self):
        # 카메라가 보는 영역 계산
        cam_x = game_framework.camera_manager.camera_x
        cam_y = game_framework.camera_manager.camera_y
        screen_w = game_framework.camera_manager.screen_width
        screen_h = game_framework.camera_manager.screen_height

        # 윈도우-뷰포트 배율 계산
        viewport_scale_x = screen_w / game_framework.camera_manager.window_width
        viewport_scale_y = screen_h / game_framework.camera_manager.window_height

        # 배율 적용된 크기
        scaled_width = int(self.img_width * self.scale * viewport_scale_x)
        scaled_height = int(self.img_height * self.scale * viewport_scale_y)

        # 화면에 보이는 월드 영역
        window_half_w = game_framework.camera_manager.window_width / 2
        window_half_h = game_framework.camera_manager.window_height / 2
        left = cam_x - window_half_w
        right = cam_x + window_half_w
        bottom = cam_y - window_half_h
        top = cam_y + window_half_h

        # 타일 반복 범위 계산 (월드 좌표 기준)
        tile_world_width = self.img_width * self.scale
        tile_world_height = self.img_height * self.scale
        start_x = int(left // tile_world_width) * tile_world_width
        start_y = int(bottom // tile_world_height) * tile_world_height

        # 배경 타일 그리기
        x = start_x
        while x < right + tile_world_width:
            y = start_y
            while y < top + tile_world_height:
                # 타일 중심 좌표 (월드)
                tile_center_x = x + tile_world_width / 2
                tile_center_y = y + tile_world_height / 2

                screen_x, screen_y = game_framework.camera_manager.world_to_screen(
                    tile_center_x, tile_center_y
                )

                # 윈도우-뷰포트 배율이 적용된 크기로 그리기
                self.image.draw(screen_x, screen_y, scaled_width, scaled_height)

                y += tile_world_height
            x += tile_world_width

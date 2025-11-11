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

        # 화면에 보이는 월드 영역
        left = cam_x - screen_w // 2
        right = cam_x + screen_w // 2
        bottom = cam_y - screen_h // 2
        top = cam_y + screen_h // 2

        # ✅ 확대된 크기로 타일 반복 범위 계산
        start_x = int(left // self.scaled_width) * self.scaled_width
        start_y = int(bottom // self.scaled_height) * self.scaled_height

        # 배경 타일 그리기
        x = start_x
        while x < right + self.scaled_width:
            y = start_y
            while y < top + self.scaled_height:
                # 타일 중심 좌표
                tile_center_x = x + self.scaled_width // 2
                tile_center_y = y + self.scaled_height // 2

                screen_x, screen_y = game_framework.camera_manager.world_to_screen(
                    tile_center_x, tile_center_y
                )

                # ✅ 확대된 크기로 그리기
                self.image.draw(screen_x, screen_y, self.scaled_width, self.scaled_height)

                y += self.scaled_height
            x += self.scaled_width


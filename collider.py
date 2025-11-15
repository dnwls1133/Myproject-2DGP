from pico2d import *
import game_framework


class Collider:
    def __init__(self, owner, offset_x=0, offset_y=0, width=0, height=0):
        self.owner = owner # 이 충돌체를 소유한 객체
        self.offset_x = offset_x # 객체 중심으로부터의 x 오프셋
        self.offset_y = offset_y # 객체 중심으로부터의 y 오프셋
        self.width = width # 충돌체의 너비
        self.height = height # 충돌체의 높이
        self.active = True # 충돌체 활성화 여부
        self.is_colliding = False  # 현재 충돌 중인지 여부

    def set_offset(self, offset_x, offset_y):
        """충돌체 오프셋 설정"""
        self.offset_x = offset_x
        self.offset_y = offset_y

    def set_size(self, width, height):
        """충돌체 크기 설정"""
        self.width = width
        self.height = height

    def set_offset_and_size(self, offset_x, offset_y, width, height):
        """충돌체 오프셋 및 크기 설정"""
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height


    def get_bb(self):
        """바운딩 박스 좌표 반환 (left, bottom, right, top)"""
        if not self.active:
            return None

        x = self.owner.x + self.offset_x
        y = self.owner.y + self.offset_y

        left = x - self.width / 2
        bottom = y - self.height / 2
        right = x + self.width / 2
        top = y + self.height / 2

        return left, bottom, right, top

    def collides_with(self, other):
        """다른 충돌체와의 충돌 여부 확인"""
        if not self.active or not other.active:
            return False

        bb1 = self.get_bb()
        bb2 = other.get_bb()

        if bb1 is None or bb2 is None:
            return False

        left_a, bottom_a, right_a, top_a = bb1
        left_b, bottom_b, right_b, top_b = bb2

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

    def draw_debug(self, is_colliding=False):
        """디버그용으로 바운딩 박스 그리기

        Args:
            is_colliding: 충돌 중이면 True (빨간색), 아니면 False (초록색)
        """
        if not self.active:
            return

        bb = self.get_bb()
        if bb is None:
            return

        left, bottom, right, top = bb

        # 월드 좌표를 스크린 좌표로 변환
        screen_left, screen_bottom = game_framework.camera_manager.world_to_screen(left, bottom)
        screen_right, screen_top = game_framework.camera_manager.world_to_screen(right, top)

        # 충돌 상태에 따라 색상 변경
        if is_colliding:
            # 빨간색 (충돌 중)
            draw_rectangle(screen_left, screen_bottom, screen_right, screen_top)
        else:
            # 초록색 (충돌 없음) - pico2d는 색상 설정이 제한적이므로 여러 번 그려서 표현
            # 실제로는 OpenGL 색상을 직접 설정해야 하지만, 간단하게 선 두께로 구분
            for i in range(3):
                draw_rectangle(screen_left - i, screen_bottom - i, screen_right + i, screen_top + i)

from collider import Collider
from pico2d import *
import game_framework
import math
import json


class Door:
    """문 충돌 객체 - 다음 스테이지로 전환"""

    def __init__(self, x, y, width, height, on_enter_callback=None):
        """
        Args:
            x, y: 문의 중심 좌표 (월드 좌표)
            width, height: 문의 크기
            on_enter_callback: 문에 진입했을 때 실행할 콜백 함수
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_enter_callback = on_enter_callback
        self.collision_handled = False  # ✅ 중복 충돌 방지
        self.stage_changed = False
        # 충돌체 생성
        self.collider = Collider(self, offset_x=0, offset_y=0, width=width, height=height)
        self.collider.active = True

    def update(self):
        pass

    def draw(self):
        # 디버그용 문 영역 표시 (선택사항)
        pass

    def on_collision_enter(self, group, other, collision_info):
        """충돌 시작 시 호출"""
        if group == 'player:door' and not self.collision_handled:
            print(f"[Door] 플레이어가 문에 진입 - 모드 전환 예약")
            self.collision_handled = True
            self.stage_changed = True





    def on_collision_exit(self, group, other, collision_info):
        """충돌 종료 시 호출"""
        pass
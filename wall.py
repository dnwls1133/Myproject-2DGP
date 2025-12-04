from collider import Collider
from pico2d import *
import game_framework
import math
import json


class Wall:
    """가상 바닥 충돌 객체 (회전 가능한 사각형)"""

    def __init__(self, x, y, width, height):
        """
        Args:
            x, y: 바닥의 중심 좌표 (월드 좌표)
            width, height: 바닥의 크기
            floor_type: 'ground'(땅), 'wall'(벽), 'ceiling'(천장) 등
            rotation: 회전 각도 (도 단위, 반시계방향)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # 충돌체 생성 (offset 0, 중심 기준)
        self.collider = Collider(self, offset_x=0, offset_y=0, width=width, height=height)
        self.collider.active = True

    def update(self):
        pass
    def draw(self):
        pass
    def on_collision_exit(self,group, other, collision_info):
        """충돌 종료 시 호출"""
        pass
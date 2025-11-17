"""
가상 바닥 객체
- 충돌체만 가지고 있으며 렌더링은 하지 않음
- Collider Manager를 통해 캐릭터와 충돌 체크
- 회전 행렬을 사용한 OBB(Oriented Bounding Box) 충돌 지원
"""
from collider import Collider
from pico2d import *
import game_framework
import math
import json


class FloorObject:
    """가상 바닥 충돌 객체 (회전 가능한 사각형)"""

    def __init__(self, x, y, width, height, floor_type='ground', rotation=0):
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
        self.floor_type = floor_type
        self.rotation = rotation  # 회전 각도 (도 단위)

        # 충돌체 생성 (offset 0, 중심 기준)
        self.collider = Collider(self, offset_x=0, offset_y=0, width=width, height=height)
        self.collider.active = True

    def get_rotated_corners(self):
        """회전된 사각형의 4개 꼭짓점 좌표를 반환 (월드 좌표)

        Returns:
            list: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                  왼쪽 아래부터 반시계방향 순서
        """
        # 회전 전 로컬 좌표 (중심이 원점)
        half_w = self.width / 2
        half_h = self.height / 2

        local_corners = [
            (-half_w, -half_h),  # 왼쪽 아래
            (half_w, -half_h),   # 오른쪽 아래
            (half_w, half_h),    # 오른쪽 위
            (-half_w, half_h)    # 왼쪽 위
        ]

        # 회전 각도를 라디안으로 변환
        angle_rad = math.radians(self.rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # 회전 행렬 적용 후 월드 좌표로 변환
        world_corners = []
        for lx, ly in local_corners:
            # 회전 행렬: [cos -sin] [x]
            #           [sin  cos] [y]
            rotated_x = lx * cos_a - ly * sin_a
            rotated_y = lx * sin_a + ly * cos_a

            # 월드 좌표로 변환
            world_x = self.x + rotated_x
            world_y = self.y + rotated_y
            world_corners.append((world_x, world_y))

        return world_corners

    def is_point_inside(self, world_x, world_y):
        """특정 점이 회전된 사각형 내부에 있는지 확인 (OBB 충돌)

        SAT(Separating Axis Theorem)를 사용한 점-회전사각형 충돌 검사
        """
        # 점을 로컬 좌표계로 변환 (역회전)
        dx = world_x - self.x
        dy = world_y - self.y

        angle_rad = math.radians(-self.rotation)  # 역회전
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        local_x = dx * cos_a - dy * sin_a
        local_y = dx * sin_a + dy * cos_a

        # 로컬 좌표에서 AABB 충돌 검사
        half_w = self.width / 2
        half_h = self.height / 2

        return (-half_w <= local_x <= half_w) and (-half_h <= local_y <= half_h)

    def get_top_surface_y(self, world_x):
        """특정 x 위치에서의 바닥 상단 표면 높이 반환

        회전된 사각형의 상단 모서리 높이를 계산합니다.
        """
        corners = self.get_rotated_corners()

        # 상단 두 점 (인덱스 2, 3)
        top_right = corners[2]
        top_left = corners[3]

        # x 범위 확인
        min_x = min(top_left[0], top_right[0])
        max_x = max(top_left[0], top_right[0])

        if not (min_x <= world_x <= max_x):
            return None

        # 선형 보간으로 높이 계산
        if abs(top_right[0] - top_left[0]) < 0.001:
            # 거의 수직이면 평균 높이 반환
            return (top_left[1] + top_right[1]) / 2

        ratio = (world_x - top_left[0]) / (top_right[0] - top_left[0])
        ratio = max(0, min(1, ratio))  # 0~1 사이로 클램프

        return top_left[1] + (top_right[1] - top_left[1]) * ratio

    def update(self):
        """업데이트 (필요시 구현)"""
        pass

    def draw(self):
        """렌더링 없음 (디버그용으로만 충돌체 그림)"""
        pass

    def draw_debug(self, is_colliding=False, camera_x=0, camera_y=0):
        """디버그용 회전된 사각형 충돌 박스 그리기

        Args:
            is_colliding: 충돌 중이면 True (빨간색), 아니면 False (초록색)
            camera_x, camera_y: 카메라 오프셋
        """
        # 충돌 상태에 따라 색상 설정
        if is_colliding:
            draw_color = (255, 0, 0)  # 빨간색
        else:
            draw_color = (0, 255, 0)  # 초록색

        # 회전된 4개 꼭짓점 가져오기
        corners = self.get_rotated_corners()

        # 스크린 좌표로 변환
        screen_corners = [
            (x - camera_x, y - camera_y)
            for x, y in corners
        ]

        # 4개의 변을 선으로 그리기
        for i in range(4):
            start = screen_corners[i]
            end = screen_corners[(i + 1) % 4]  # 마지막은 첫 번째로 연결

            # 선분을 작은 사각형들로 표현 (pico2d에는 draw_line이 없음)
            distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            steps = max(2, int(distance))

            for j in range(steps):
                ratio = j / steps if steps > 1 else 0
                px = start[0] + (end[0] - start[0]) * ratio
                py = start[1] + (end[1] - start[1]) * ratio
                draw_rectangle(px, py, px + 2, py + 2)


class FloorManager:
    """바닥 객체들을 관리하는 매니저 클래스"""

    def __init__(self):
        self.floors = []  # 바닥 객체 리스트

    def add_floor(self, floor):
        """바닥 추가"""
        self.floors.append(floor)

    def remove_floor(self, floor):
        """바닥 제거"""
        if floor in self.floors:
            self.floors.remove(floor)

    def get_all_floors(self):
        """모든 바닥 객체 리스트 반환"""
        return self.floors

    def get_floor_at(self, world_x, world_y):
        """특정 위치에 있는 바닥 반환"""
        for floor in self.floors:
            if floor.is_point_inside(world_x, world_y):
                return floor
        return None

    def update(self):
        """모든 바닥 업데이트"""
        for floor in self.floors:
            floor.update()

    def draw(self):
        """렌더링 (바닥은 충돌체만 있으므로 기본적으로 아무것도 안 그림)"""
        pass

    def draw_debug(self, camera_x=0, camera_y=0, colliding_floors=None):
        """모든 바닥 디버그 그리기

        Args:
            camera_x, camera_y: 카메라 오프셋
            colliding_floors: 충돌 중인 바닥들의 집합 (빨간색으로 표시)
        """
        if colliding_floors is None:
            colliding_floors = set()

        for floor in self.floors:
            is_colliding = floor in colliding_floors
            floor.draw_debug(is_colliding, camera_x, camera_y)

    def save_to_file(self, filename):
        """바닥 정보를 JSON 파일로 저장"""
        data = {
            'floors': [
                {
                    'x': floor.x,
                    'y': floor.y,
                    'width': floor.width,
                    'height': floor.height,
                    'floor_type': floor.floor_type,
                    'rotation': floor.rotation
                }
                for floor in self.floors
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"바닥 정보 저장 완료: {filename} ({len(self.floors)}개)")

    @staticmethod
    def load_from_file(filename):
        """JSON 파일에서 바닥 정보 로드"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        manager = FloorManager()

        for floor_data in data.get('floors', []):
            floor = FloorObject(
                x=floor_data['x'],
                y=floor_data['y'],
                width=floor_data['width'],
                height=floor_data['height'],
                floor_type=floor_data.get('floor_type', 'ground'),
                rotation=floor_data.get('rotation', 0)
            )
            manager.add_floor(floor)

        print(f"바닥 정보 로드 완료: {filename} ({len(manager.floors)}개)")
        return manager

"""
가상 바닥 객체
- 충돌체만 가지고 있으며 렌더링은 하지 않음
- Collider Manager를 통해 캐릭터와 충돌 체크
"""
from collider import Collider
from pico2d import *
import game_framework
import math


class FloorObject:
    """가상 바닥 충돌 객체"""

    def __init__(self, x, y, width, height, floor_type='ground', slope_angle=0):
        """
        Args:
            x, y: 바닥의 중심 좌표 (월드 좌표)
            width, height: 바닥의 크기
            floor_type: 'ground'(땅), 'wall'(벽), 'ceiling'(천장) 등
            slope_angle: 경사 각도 (도 단위, 0=수평, 양수=오른쪽 상승, 음수=왼쪽 상승)
        """
        self.x = x
        self.y = y
        self.floor_type = floor_type
        self.slope_angle = slope_angle

        # 충돌체 생성 (offset 0, 중심 기준)
        self.collider = Collider(self, offset_x=0, offset_y=0, width=width, height=height)
        self.collider.active = True

    def get_height_at_x(self, world_x):
        """특정 x 위치에서의 바닥 높이 계산 (경사 고려)

        Returns:
            float: 해당 x 위치에서의 바닥 표면 높이 (y 좌표)
            None: 해당 x 위치가 바닥 범위 밖인 경우
        """
        if self.slope_angle == 0:
            # 평지인 경우 바닥 상단 높이 반환
            return self.y + self.collider.height / 2

        # 바닥의 좌우 끝 위치
        left = self.x - self.collider.width / 2
        right = self.x + self.collider.width / 2

        if left <= world_x <= right:
            # 선형 보간으로 높이 계산
            ratio = (world_x - left) / self.collider.width

            # 바닥의 상단 기본 높이 (평지일 때의 높이)
            base_top = self.y + self.collider.height / 2

            # 경사에 의한 높이 변화량 계산
            height_diff = self.collider.width * math.tan(math.radians(self.slope_angle))

            # 왼쪽 끝 높이 (기본 높이)
            left_height = base_top

            # 오른쪽 끝 높이 (경사 적용)
            right_height = base_top + height_diff

            # 보간된 높이
            return left_height + (right_height - left_height) * ratio

        return None

    def is_point_inside(self, world_x, world_y):
        """특정 점이 바닥 내부에 있는지 확인 (경사면 고려)"""
        left = self.x - self.collider.width / 2
        right = self.x + self.collider.width / 2
        bottom = self.y - self.collider.height / 2

        # X 범위 체크
        if not (left <= world_x <= right):
            return False

        if self.slope_angle == 0:
            # 평지인 경우 사각형 충돌
            top = self.y + self.collider.height / 2
            return bottom <= world_y <= top
        else:
            # 경사면인 경우: 사다리꼴 내부 판정
            # 해당 x 위치에서의 표면(상단) 높이 계산
            surface_height = self.get_height_at_x(world_x)
            if surface_height is None:
                return False

            # 사다리꼴 영역: 하단(고정)과 상단(경사) 사이
            # 하단은 항상 bottom
            # 상단은 경사에 따라 변함

            # Y 좌표가 하단보다 위에 있고, 표면 높이보다 아래에 있으면 충돌
            # 표면 위로 약간의 여유 공간 허용 (플레이어가 바닥에 딱 붙어 서있을 수 있도록)
            tolerance = 5  # 표면 위 허용 오차
            return bottom <= world_y <= surface_height + tolerance

    def update(self):
        """업데이트 (필요시 구현)"""
        pass

    def draw(self):
        """렌더링 없음 (디버그용으로만 충돌체 그림)"""
        pass

    def draw_debug(self, is_colliding=False, camera_x=0, camera_y=0):
        """디버그용 충돌 박스 그리기 (경사면 지원)

        Args:
            is_colliding: 충돌 중이면 True (빨간색), 아니면 False (초록색)
            camera_x, camera_y: 카메라 오프셋 (월드 좌표를 스크린 좌표로 변환)
        """
        from pico2d import draw_rectangle

        # 평지와 경사면 모두 동일하게 카메라 오프셋 적용
        left = self.x - self.collider.width / 2
        right = self.x + self.collider.width / 2
        bottom = self.y - self.collider.height / 2

        if self.slope_angle == 0:
            # 평지는 사각형으로 그리기
            top = self.y + self.collider.height / 2

            # 월드 좌표를 스크린 좌표로 변환
            screen_left = left - camera_x
            screen_bottom = bottom - camera_y
            screen_right = right - camera_x
            screen_top = top - camera_y

            # 사각형 그리기
            draw_rectangle(screen_left, screen_bottom, screen_right, screen_top)
        else:
            # 경사면은 사다리꼴 모양으로 그리기
            # 왼쪽과 오른쪽의 높이 계산
            left_height = self.get_height_at_x(left)
            right_height = self.get_height_at_x(right)

            if left_height is None or right_height is None:
                return

            # 월드 좌표를 스크린 좌표로 변환 (카메라 오프셋 적용)
            x1 = left - camera_x  # 왼쪽 아래
            y1 = bottom - camera_y
            x2 = right - camera_x  # 오른쪽 아래
            y2 = bottom - camera_y
            x3 = right - camera_x  # 오른쪽 위
            y3 = right_height - camera_y
            x4 = left - camera_x  # 왼쪽 위
            y4 = left_height - camera_y

            # 사다리꼴의 4개 변을 선으로 그리기
            # 하단 (y1 == y2이므로 수평선)
            draw_rectangle(x1, y1, x2, y1 + 2)

            # 왼쪽 변 (수직 또는 약간 기울어진 선)
            steps = max(2, int(abs(y4 - y1)))
            for i in range(steps):
                ratio = i / steps
                px = x1 + (x4 - x1) * ratio
                py = y1 + (y4 - y1) * ratio
                draw_rectangle(px, py, px + 2, py + 2)

            # 오른쪽 변
            steps = max(2, int(abs(y3 - y2)))
            for i in range(steps):
                ratio = i / steps
                px = x2 + (x3 - x2) * ratio
                py = y2 + (y3 - y2) * ratio
                draw_rectangle(px, py, px + 2, py + 2)

            # 상단 (경사진 선)
            steps = max(2, int(abs(x3 - x4)))
            for i in range(steps):
                ratio = i / steps
                px = x4 + (x3 - x4) * ratio
                py = y4 + (y3 - y4) * ratio
                draw_rectangle(px, py, px + 2, py + 2)

    def on_collision(self, group, other):
        """충돌 콜백 - 바닥은 특별한 반응 없음"""
        pass

    @staticmethod
    def create_from_rect(left, bottom, right, top, floor_type='ground', slope_angle=0):
        """사각형 좌표로 바닥 생성"""
        x = (left + right) / 2
        y = (bottom + top) / 2
        width = right - left
        height = top - bottom
        return FloorObject(x, y, width, height, floor_type, slope_angle)


class FloorManager:
    """바닥 객체들을 관리하는 매니저"""

    def __init__(self):
        self.floors = []  # FloorObject 리스트

    def add_floor(self, floor):
        """바닥 추가"""
        self.floors.append(floor)

    def remove_floor(self, floor):
        """바닥 제거"""
        if floor in self.floors:
            self.floors.remove(floor)

    def clear(self):
        """모든 바닥 제거"""
        self.floors.clear()

    def update(self):
        """모든 바닥 업데이트"""
        for floor in self.floors:
            floor.update()

    def draw(self):
        """렌더링 (실제로는 아무것도 안 그림)"""
        pass

    def draw_debug(self, colliding_floors=None, camera_x=0, camera_y=0):
        """디버그용 모든 바닥 그리기

        Args:
            colliding_floors: 충돌 중인 바닥 객체들의 집합
            camera_x, camera_y: 카메라 오프셋
        """
        if colliding_floors is None:
            colliding_floors = set()

        for floor in self.floors:
            is_colliding = floor in colliding_floors
            floor.draw_debug(is_colliding, camera_x, camera_y)

    def save_to_dict(self):
        """저장용 딕셔너리로 변환"""
        return {
            'floors': [
                {
                    'x': floor.x,
                    'y': floor.y,
                    'width': floor.collider.width,
                    'height': floor.collider.height,
                    'type': floor.floor_type,
                    'slope_angle': floor.slope_angle
                }
                for floor in self.floors
            ]
        }

    def save_to_file(self, filename):
        """파일로 저장"""
        import json
        data = self.save_to_dict()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"바닥 데이터 저장 완료: {filename} ({len(self.floors)}개)")

    def load_from_dict(self, data):
        """딕셔너리에서 복원"""
        self.clear()
        if 'floors' in data:
            for floor_data in data['floors']:
                floor = FloorObject(
                    floor_data['x'],
                    floor_data['y'],
                    floor_data['width'],
                    floor_data['height'],
                    floor_data.get('type', 'ground'),
                    floor_data.get('slope_angle', 0)
                )
                self.add_floor(floor)
        print(f"바닥 {len(self.floors)}개 로드 완료")

    @staticmethod
    def load_from_file(filename):
        """파일에서 로드하여 새 FloorManager 반환"""
        import json
        manager = FloorManager()
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                manager.load_from_dict(data)
        except FileNotFoundError:
            print(f"바닥 파일을 찾을 수 없습니다: {filename}")
        except Exception as e:
            print(f"바닥 로드 실패: {e}")
        return manager

    def get_all_floors(self):
        """모든 바닥 객체 반환"""
        return self.floors

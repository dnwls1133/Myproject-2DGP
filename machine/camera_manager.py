class CameraManager:

    def __init__(self,screen_width,screen_height,world_width = None,world_height = None):
        """
        screen_width/height : 화면의 가로/세로 픽셀 크기
        world_width/height : 게임 월드의 가로/세로 픽셀 크기 (None이면 무제한)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.world_width = world_width
        self.world_height = world_height

        # 카메라 위치 (월드 좌표계)
        self.camera_x = screen_width / 2
        self.camera_y = screen_height / 2

        # 타겟 위치
        self.target_x = self.camera_x
        self.target_y = self.camera_y

        self.lerp_speed = 0.1  # 보간 속도 (0~1)

        # 추가: 타겟 객체 또는 좌표 콜러블
        self._target = None

        # 추가: 경계에서 다시 따라오기 위한 내부 여유(픽셀)
        # 예: 50px 만큼 내부로 들어오면 카메라가 다시 플레이어를 따라옴
        self.follow_margin = 10

        self.window_width = screen_width / 2.0  # 기본값: 화면의 절반 = 2배 확대
        self.window_height = screen_height / 2.0


    def set_target(self, obj_or_callable):
        """객체(속성 x,y) 또는 (-> (x,y)) 콜러블을 타겟으로 설정."""
        self._target = obj_or_callable

    def clear_target(self):
        self._target = None

    def move(self,dx,dy):
        """카메라 타겟 위치를 이동시킵니다."""
        self.camera_x += dx
        self.camera_y += dy
        self.target_x = self.camera_x
        self.target_y = self.camera_y

    def move_smooth(self,dx,dy):
        """카메라 타겟 위치를 부드럽게 이동시킵니다."""
        self.target_x += dx
        self.target_y += dy

    def shake(self,intensity = 10, duration = 0.3):
        """화면 흔들림 효과를 추가합니다."""
        self.shake_intensity = intensity
        self.shake_duration = duration
        self.shake_time = 0.0

    def update(self,dt):
        tx = self.target_x
        ty = self.target_y

        if self._target is not None:
            try:
                if callable(self._target):
                    tx, ty = self._target()
                else:
                    tx = getattr(self._target, 'x')
                    ty = getattr(self._target, 'y')
                tx = float(tx)
                ty = float(ty)
            except Exception:
                pass

        # X축 처리
        if self.world_width is not None:
            half_w = self.window_width / 2
            cam_min = half_w
            cam_max = self.world_width - half_w

            # 현재 카메라가 왼쪽/오른쪽 경계에 있는지 확인
            at_left = abs(self.camera_x - cam_min) < 1.0
            at_right = abs(self.camera_x - cam_max) < 1.0

            if at_left:
                # 왼쪽 경계: 타겟이 경계에서 follow_margin만큼 안쪽에 있으면 추적 재개
                if tx >= cam_min + self.follow_margin:
                    desired_target_x = tx
                else:
                    desired_target_x = cam_min
            elif at_right:
                # 오른쪽 경계: 타겟이 경계에서 follow_margin만큼 안쪽에 있으면 추적 재개
                if tx <= cam_max - self.follow_margin:
                    desired_target_x = tx
                else:
                    desired_target_x = cam_max
            else:
                # 일반 구간: 경계 클램프
                desired_target_x = max(cam_min, min(tx, cam_max))
        else:
            desired_target_x = tx

        # Y축 처리
        if self.world_height is not None:
            half_h = self.window_height / 2
            cam_min_y = half_h
            cam_max_y = self.world_height - half_h

            at_top = abs(self.camera_y - cam_min_y) < 1.0
            at_bottom = abs(self.camera_y - cam_max_y) < 1.0

            if at_top:
                if ty >= cam_min_y + self.follow_margin:
                    desired_target_y = ty
                else:
                    desired_target_y = cam_min_y
            elif at_bottom:
                if ty <= cam_max_y - self.follow_margin:
                    desired_target_y = ty
                else:
                    desired_target_y = cam_max_y
            else:
                desired_target_y = max(cam_min_y, min(ty, cam_max_y))
        else:
            desired_target_y = ty

        self.target_x = desired_target_x
        self.target_y = desired_target_y

        # 보간
        self.camera_x += (self.target_x - self.camera_x) * self.lerp_speed
        self.camera_y += (self.target_y - self.camera_y) * self.lerp_speed

        # 화면 흔들림
        shake_x = 0
        shake_y = 0
        if hasattr(self, 'shake_time') and self.shake_time < self.shake_duration:
            import random
            self.shake_time += dt
            progress = 1.0 - (self.shake_time / self.shake_duration)
            shake_x = random.uniform(-self.shake_intensity, self.shake_intensity) * progress
            shake_y = random.uniform(-self.shake_intensity, self.shake_intensity) * progress

        final_x = self.camera_x + shake_x
        final_y = self.camera_y + shake_y

        # 최종 경계 클램프 (음수 영역 포함)
        if self.world_width is not None:
            half_w = self.window_width / 2
            final_x = max(half_w, min(final_x, self.world_width - half_w))
        if self.world_height is not None:
            half_h = self.window_height / 2
            final_y = max(half_h, min(final_y, self.world_height - half_h))

        self.camera_x = final_x
        self.camera_y = final_y

    def screen_to_world(self, screen_x,screen_y):
        """화면 좌표를 월드 좌표로 변환합니다."""
        world_x = screen_x + self.camera_x - self.screen_width // 2
        world_y = screen_y + self.camera_y - self.screen_height // 2
        return world_x, world_y

    def world_to_screen(self, world_x,world_y):
        """월드 좌표를 화면 좌표로 변환합니다. (윈도우-뷰포트 변환)"""
        # 1. 윈도우 영역 계산 (카메라 중심 기준)
        window_left = self.camera_x - self.window_width / 2
        window_bottom = self.camera_y - self.window_height / 2

        # 2. 월드 좌표를 윈도우 내 상대 좌표로 변환 (0~1)
        rel_x = (world_x - window_left) / self.window_width
        rel_y = (world_y - window_bottom) / self.window_height

        # 3. 뷰포트(화면 전체)에 매핑
        screen_x = rel_x * self.screen_width
        screen_y = rel_y * self.screen_height
        return screen_x, screen_y

    def set_window_size(self,width,height):
        """카메라 윈도우 크기를 설정합니다. (작을수록 확대)"""
        self.window_width = width
        self.window_height = height

    def set_zoom(self,zoom_level):
        """줌 레벨에 따라 윈도우 크기를 조정합니다."""
        self.window_width = self.screen_width / zoom_level
        self.window_height = self.screen_height / zoom_level

    def get_position(self):
        """카메라의 현재 월드 좌표를 반환합니다."""
        return self.camera_x, self.camera_y

    def set_position(self,x,y):
        """카메라의 위치를 설정합니다."""
        self.camera_x = x
        self.camera_y = y

        self.target_x = x
        self.target_y = y
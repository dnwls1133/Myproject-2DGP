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
        """카메라 위치를 타겟 위치로 부드럽게 이동시킵니다."""
        self.camera_x += (self.target_x - self.camera_x) * self.lerp_speed
        self.camera_y += (self.target_y - self.camera_y) * self.lerp_speed

        # 화면 흔딜림 효과
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

        # 월드 경계 내로 카메라 위치 제한
        if self.world_width is not None:
            half_screen_w = self.screen_width / 2
            final_x = max(half_screen, min(final_x, self.world_width - half_screen))

        if self.world_height is not None:
            half_screen_h = self.screen_height / 2
            final_y = max(half_screen, min(final_y, self.world_height - half_screen))

        self.camera_x = final_x
        self.camera_y = final_y

    def screen_to_world(self, screen_x,screen_y):
        """화면 좌표를 월드 좌표로 변환합니다."""
        world_x = screen_x + self.camera_x - self.screen_width // 2
        world_y = screen_y + self.camera_y - self.screen_height // 2
        return world_x, world_y

    def world_to_screen(self, world_x,world_y):
        """월드 좌표를 화면 좌표로 변환합니다."""
        screen_x = world_x - self.camera_x + self.screen_width // 2
        screen_y = world_y - self.camera_y + self.screen_height // 2
        return screen_x, screen_y

    def get_position(self):
        """카메라의 현재 월드 좌표를 반환합니다."""
        return self.camera_x, self.camera_y

    def set_position(self,x,y):
        """카메라의 위치를 설정합니다."""
        self.camera_x = x
        self.camera_y = y

        self.target_x = x
        self.target_y = y
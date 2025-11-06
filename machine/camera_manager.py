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

    def update(self,dt):
        """카메라 위치를 타겟 위치로 부드럽게 이동시킵니다."""
        self.camera_x += (self.target_x - self.camera_x) * self.lerp_speed
        self.camera_y += (self.target_y - self.camera_y) * self.lerp_speed

        # 월드 경계 내로 카메라 위치 제한
        if self.world_width is not None:
            half_screen_w = self.screen_width / 2
            self.camera_x = max(half_screen_w, min(self.camera_x, self.world_width - half_screen_w))

        if self.world_height is not None:
            half_screen_h = self.screen_height / 2
            self.camera_y = max(half_screen_h, min(self.camera_y, self.world_height - half_screen_h))

    def screen_to_world(self, screen_x,screen_y):
        """화면 좌표를 월드 좌표로 변환합니다."""
        world_x = screen_x + self.camera_x - self.screen_width // 2
        world_y = screen_y + self.camera_y - self.screen_height // 2
        return world_x, world_y

    def get_position(self):
        """카메라의 현재 월드 좌표를 반환합니다."""
        return self.camera_x, self.camera_y

    def set_position(self,x,y):
        """카메라의 위치를 설정합니다."""
        self.camera_x = x
        self.camera_y = y

        self.target_x = x
        self.target_y = y
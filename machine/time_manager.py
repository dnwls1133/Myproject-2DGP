import time

class TimeManager:
    def __init__(self,fixed_dt = 1/60.0, max_frame_time =0.25):
        """
        fixed_dt: 고정 업데이트 간격 (초)
        max_frame_time: 프레임 드랍 시 dt 상한선
        """

        self.fixed_dt = float(fixed_dt)
        self.max_frame_time = float(max_frame_time)
        self.prev_time = time.time()
        self.dt = 0.0
        self.accumulator = 0.0

    def update(self):
        """시간을 업데이트하고 dt를 계산합니다."""
        current_time = time.time()
        frame_time = current_time - self.prev_time
        self.prev_time = current_time

        # 음수 방지 및 최대값 제한
        frame_time = max(0.0, min(frame_time, self.max_frame_time))

        self.dt = frame_time
        self.accumulator += frame_time

    def get_dt(self):
        """현재 프레임의 dt를 반환합니다."""
        return self.dt

    def consume_fixed(self):
        """고정 업데이트 간격을 소비하고 남은 시간을 반환합니다."""
        if self.accumulator >= self.fixed_dt:
            self.accumulator -= self.fixed_dt
            return True
        return False

    def get_fixed_dt(self):
        """고정 업데이트 간격을 반환합니다."""
        return self.fixed_dt

    def get_interpolation_alpha(self):
        """보간 알파 값을 반환합니다."""
        return self.accumulator / self.fixed_dt if self.fixed_dt > 0 else 0.0

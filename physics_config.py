# physics_config.py
# 물리 단위 변환 시스템

class PhysicsConfig:
    """
    픽셀과 실제 물리 단위(미터) 간의 변환을 담당하는 클래스
    게임 내에서 실제 물리 법칙을 적용하기 위한 스케일 설정
    """

    # 기본 변환 상수 (1미터 = 100픽셀)
    PIXELS_PER_METER = 100.0
    METERS_PER_PIXEL = 1.0 / PIXELS_PER_METER

    # 실제 물리 상수들 (SI 단위)
    GRAVITY_REAL = -9.81  # m/s^2 (실제 중력가속도)

    # 픽셀 단위로 변환된 물리 상수
    GRAVITY_PIXELS = GRAVITY_REAL * PIXELS_PER_METER  # -981 pixels/s^2

    # 캐릭터 기본 물리 속성 (미터 단위)
    class Character:
        HEIGHT_METERS = 1.8  # 캐릭터 키 1.8m
        WALK_SPEED_MPS = 1.0  # 걷기 속도 2.5m/s
        RUN_SPEED_MPS = 3.0   # 달리기 속도 4m/s
        JUMP_SPEED_MPS = 5.0  # 점프 속도 6m/s
        MAX_FALL_SPEED_MPS = 10.0  # 최대 낙하 속도 10m/s
        SLIDE_SPEED_MPS = 15.0  # 슬라이드 속도 15m/s

    class Boss:
        HEIGHT_METERS = 3.0  # 보스 키 3.0m
        JUMP_SPEED_MPS = 8.0  # 점프 속도 8m/s
        MAX_FALL_SPEED_MPS = 12.0  # 최대 낙하 속도 12m/s

    @classmethod
    def meters_to_pixels(cls, meters):
        """미터를 픽셀로 변환

        Args:
            meters (float): 미터 단위 값

        Returns:
            float: 픽셀 단위 값
        """
        return meters * cls.PIXELS_PER_METER

    @classmethod
    def pixels_to_meters(cls, pixels):
        """픽셀을 미터로 변환

        Args:
            pixels (float): 픽셀 단위 값

        Returns:
            float: 미터 단위 값
        """
        return pixels * cls.METERS_PER_PIXEL

    @classmethod
    def mps_to_pps(cls, meters_per_second):
        """m/s를 pixels/s로 변환

        Args:
            meters_per_second (float): m/s 단위 속도

        Returns:
            float: pixels/s 단위 속도
        """
        return meters_per_second * cls.PIXELS_PER_METER

    @classmethod
    def pps_to_mps(cls, pixels_per_second):
        """pixels/s를 m/s로 변환

        Args:
            pixels_per_second (float): pixels/s 단위 속도

        Returns:
            float: m/s 단위 속도
        """
        return pixels_per_second * cls.METERS_PER_PIXEL

    @classmethod
    def get_character_physics(cls):
        """캐릭터 물리 속성을 픽셀 단위로 반환

        Returns:
            dict: 픽셀 단위로 변환된 물리 속성 딕셔너리
        """
        return {
            'height': cls.meters_to_pixels(cls.Character.HEIGHT_METERS),
            'walk_speed': cls.mps_to_pps(cls.Character.WALK_SPEED_MPS),
            'run_speed': cls.mps_to_pps(cls.Character.RUN_SPEED_MPS),
            'jump_speed': cls.mps_to_pps(cls.Character.JUMP_SPEED_MPS),
            'max_fall_speed': -cls.mps_to_pps(cls.Character.MAX_FALL_SPEED_MPS),
            'slide_speed': cls.mps_to_pps(cls.Character.SLIDE_SPEED_MPS),
            'gravity': cls.GRAVITY_PIXELS
        }

    @classmethod
    def get_boss_physics(cls):
        """보스 물리 속성을 픽셀 단위로 반환

        Returns:
            dict: 픽셀 단위로 변환된 물리 속성 딕셔너리
        """
        return {
            'height': cls.meters_to_pixels(cls.Boss.HEIGHT_METERS),
            'jump_speed': cls.mps_to_pps(cls.Boss.JUMP_SPEED_MPS),
            'max_fall_speed': -cls.mps_to_pps(cls.Boss.MAX_FALL_SPEED_MPS),
            'gravity': cls.GRAVITY_PIXELS
        }


# 전역 함수로도 접근 가능하도록 제공
def meters_to_pixels(meters):
    return PhysicsConfig.meters_to_pixels(meters)

def pixels_to_meters(pixels):
    return PhysicsConfig.pixels_to_meters(pixels)

def mps_to_pps(mps):
    return PhysicsConfig.mps_to_pps(mps)

def pps_to_mps(pps):
    return PhysicsConfig.pps_to_mps(pps)


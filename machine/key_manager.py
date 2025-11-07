from pico2d import *

class KeyManager:
    def __init__(self):
        self._down = set()
        self._pressed = set()
        self._released = set()
        self._pressed_events = []
        self._released_events = []
        self.quit = False

    def update(self):
        """프레임마다 호출: 이벤트를 처리하고 상태 갱신"""
        self._pressed.clear()
        self._released.clear()
        self._pressed_events.clear()
        self._released_events.clear()
        self.quit = False
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.quit = True
            elif event.type == SDL_KEYDOWN:
                key = event.key
                if key not in self._down:
                    self._pressed.add(key)
                    self._pressed_events.append(event)
                self._down.add(key)
            elif event.type == SDL_KEYUP:
                key = event.key
                self._down.discard(key)
                self._released.add(key)
                self._released_events.append(event)



    def is_down(self,key):
        """키가 눌려져 있는지 여부 반환"""
        return key in self._down

    def was_pressed(self,key):
        """키가 이번 프레임에 눌려졌는지 여부 반환"""
        return key in self._pressed
    def was_released(self,key):
        """키가 이번 프레임에 떼어졌는지 여부 반환"""
        return key in self._released

    def get_pressed_events(self):
        """이번 프레임에 눌린 키의 SDL 이벤트 객체 리스트 반환"""
        return self._pressed_events

    def get_released_events(self):
        """이번 프레임에 떼어진 키의 SDL 이벤트 객체 리스트 반환"""
        return self._released_events

    def clear_pressed_events(self):
        """이번 프레임에 눌린 키의 SDL 이벤트 객체 리스트 초기화"""
        self._pressed_events.clear()

    def clear_released_events(self):
        """이번 프레임에 떼어진 키의 SDL 이벤트 객체 리스트 초기화"""
        self._released_events.clear()


    def any_pressed(self):
        """이번 프레임에 눌려진 키가 하나라도 있는지 여부 반환"""
        return bool(self._pressed)

    def clear(self):
        """모든 키 상태 초기화"""
        self._down.clear()
        self._pressed.clear()
        self._released.clear()
        self._pressed_events.clear()
        self._released_events.clear()

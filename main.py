from pico2d import *
from animation import AnimationManager, Animation

# 먼저 canvas를 열어서 pico2d를 완전히 초기화 (픽셀 아트에 적합한 크기)
open_canvas(1024, 768)  # 더 큰 해상도로 설정

# 애니메이션 매니저 초기화
anim_manager = AnimationManager()

try:
    # 애니메이션 등록
    anim_manager.register_animation('idle',
        "sprites/player/texture2d/player_idle/penintent_idle_anim.json",
        "sprites/player/texture2d/player_idle/penintent_idle_anim.png")

    anim_manager.register_animation('attack',
        "sprites/player/texture2d/player_attack/penintent_attack_combo_anim.json",
        "sprites/player/texture2d/player_attack/penintent_attack_combo_anim.png")

    print("애니메이션 등록 완료")
except Exception as e:
    print(f"애니메이션 등록 실패: {e}")


class Penintent:
    def __init__(self):
        self.x, self.y = 400,200

        # None 체크 추가
        idle_data = anim_manager.get_animation('idle')
        attack_data = anim_manager.get_animation('attack')

        if idle_data is None or attack_data is None:
            print("애니메이션 데이터가 없습니다!")
            # 기본값 설정으로 오류 방지
            self.idle_animation = None
            self.attack_animation = None
            self.current_animation = None
            return

        self.idle_animation = Animation(idle_data)
        self.attack_animation = Animation(attack_data)
        self.current_animation = self.idle_animation

    def update(self):
        if self.current_animation:
            self.current_animation.update(0.005)

    def draw(self):
        if self.current_animation:
            self.current_animation.draw(self.x,self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_k:
                if world[0].current_animation != world[0].attack_animation:
                    world[0].current_animation = world[0].attack_animation
                    world[0].current_animation.current_frame = 0
                    world[0].current_animation.frame_time = 0

            elif event.key == SDLK_ESCAPE:
                running = False



def reset_world():
    global running
    global world
    running = True
    world = [] 
    penintent = Penintent()
    world.append(penintent)

def update_world():
    for game_object in world:
        game_object.update()

        if(game_object.current_animation == game_object.attack_animation and
           game_object.current_animation.is_animation_end()):
            game_object.current_animation = game_object.idle_animation
            game_object.current_animation.current_frame = 0
            game_object.current_animation.frame_time = 0


    pass
def render_world():
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()

running = True

reset_world()
while running:
    handle_events()
    # 게임 로직
    update_world()
    render_world()
    #delay(0.05)

close_canvas()

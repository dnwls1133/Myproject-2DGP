# collision_pairs = {} # key: 충돌종류 group. value: [list of a, list of b] 객체들이 리스트로 들어있다.

collision_pairs = {}
collision_states = {} # 충돌 상태 추적용 딕셔너리


def add_collision_pair(group, a, b):
    """ 충돌 페어 등록"""
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
        collision_states[group] = {}

    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    """ 충돌 객체 제거 """
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def clear_collision_pairs():
    """ 모든 충돌 페어 초기화 """
    collision_pairs.clear()
    collision_states.clear()

def check_collisions(group):
    if group not in collision_pairs:
        return

    a_list, b_list = collision_pairs[group]

    # 현재 프레임의 충돌 쌍 저장
    current_collisions = set()

    for a in a_list:
        # a의 공격 충돌체 수집
        a_attack_colliders = []

        if hasattr(a, 'attack_collider') and a.attack_collider.active:
            a_attack_colliders.append(('attack', a.attack_collider))

        if hasattr(a, 'jump_attack_collider') and a.jump_attack_collider.active:
            a_attack_colliders.append(('jump_attack', a.jump_attack_collider))

        # a의 기본 충돌체
        a_base_collider = None
        if hasattr(a, 'collider') and a.collider.active:
            a_base_collider = a.collider

        for b in b_list:
            # b의 공격 충돌체 수집
            b_attack_colliders = []

            if hasattr(b, 'attack_collider') and b.attack_collider.active:
                b_attack_colliders.append(('attack', b.attack_collider))

            if hasattr(b, 'jump_attack_collider') and b.jump_attack_collider.active:
                b_attack_colliders.append(('jump_attack', b.jump_attack_collider))

            # b의 기본 충돌체
            b_base_collider = None
            if hasattr(b, 'collider') and b.collider.active:
                b_base_collider = b.collider

            # 1) a의 공격 충돌체 vs b의 기본 충돌체
            if b_base_collider:
                for collider_type, a_attack in a_attack_colliders:
                    collision_key = (id(a_attack), id(b_base_collider))

                    if a_attack.collides_with(b_base_collider):

                        a_attack.is_colliding = True
                        b_base_collider.is_colliding = True
                        current_collisions.add(collision_key)

                        # 이전 프레임에 충돌 중이었는지 확인
                        if collision_key not in collision_states.get(group, {}):
                            # 충돌 시작 (Enter)
                            if hasattr(a, 'on_collision_enter'):
                                a.on_collision_enter(group, b, collider_type)
                            if hasattr(b, 'on_collision_enter'):
                                b.on_collision_enter(group, a, 'base')
                        else:
                            # 충돌 지속 (On)
                            if hasattr(a, 'on_collision'):
                                a.on_collision(group, b, collider_type)
                            if hasattr(b, 'on_collision'):
                                b.on_collision(group, a, 'base')
                    else:
                        a_attack.is_colliding = False

            # 2) b의 공격 충돌체 vs a의 기본 충돌체
            if a_base_collider:
                for collider_type, b_attack in b_attack_colliders:
                    collision_key = (id(b_attack), id(a_base_collider))

                    if b_attack.collides_with(a_base_collider):

                        b_attack.is_colliding = True
                        a_base_collider.is_colliding = True
                        current_collisions.add(collision_key)

                        if collision_key not in collision_states.get(group, {}):
                            # 충돌 시작 (Enter)
                            if hasattr(b, 'on_collision_enter'):
                                b.on_collision_enter(group, a, collider_type)
                            if hasattr(a, 'on_collision_enter'):
                                a.on_collision_enter(group, b, 'base')
                        else:
                            # 충돌 지속 (On)
                            if hasattr(b, 'on_collision'):
                                b.on_collision(group, a, collider_type)
                            if hasattr(a, 'on_collision'):
                                a.on_collision(group, b, 'base')
                    else:
                        b_attack.is_colliding = False

            # 3) 기본 충돌체 vs 기본 충돌체 (바닥, 벽 등과의 충돌)
            if a_base_collider and b_base_collider :
                collision_key = (id(a_base_collider), id(b_base_collider))

                if a_base_collider.collides_with(b_base_collider):
                    a_base_collider.is_colliding = True
                    b_base_collider.is_colliding = True
                    current_collisions.add(collision_key)

                    if collision_key not in collision_states.get(group, {}):
                        # 충돌 시작 (Enter)
                        if hasattr(a, 'on_collision_enter'):
                            a.on_collision_enter(group, b, 'base1')
                        if hasattr(b, 'on_collision_enter'):
                            b.on_collision_enter(group, a, 'base1')
                    else:
                        # 충돌 지속 (On)
                        if hasattr(a, 'on_collision'):
                            a.on_collision(group, b, 'base1')
                        if hasattr(b, 'on_collision'):
                            b.on_collision(group, a, 'base1')
                else:
                    # 충돌하지 않을 때는 is_colliding을 False로 설정하지 않음
                    # (다른 객체와 충돌 중일 수 있으므로)
                    pass

    # 충돌 종료 감지 (Exit)
    if group in collision_states:
        for collision_key in collision_states[group]:
            if collision_key not in current_collisions:
                # 충돌 종료
                # collision_key는 (collider_id_1, collider_id_2) 형태
                # 실제 객체를 찾아서 on_collision_exit 호출
                # (간단하게 하기 위해 현재는 생략, 필요시 매핑 추가)
                a.on_collision_exit(group, b, 'unknown')
                b.on_collision_exit(group, a, 'unknown')
                pass

    # 현재 프레임 충돌 상태 저장
    collision_states[group] = current_collisions




def check_all_collisions():
    """ 모든 충돌 페어 체크 """
    for group in collision_pairs.keys():
        check_collisions(group)

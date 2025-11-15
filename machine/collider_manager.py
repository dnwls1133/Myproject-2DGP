# collision_pairs = {} # key: 충돌종류 group. value: [list of a, list of b] 객체들이 리스트로 들어있다.

collision_pairs = {}

def add_collision_pair(group, a, b):
    """ 충돌 페어 등록"""
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]

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

def check_collisions(group):
    """ 특정 그룹의 충돌 체크"""
    if group not in collision_pairs:
        return

    a_list, b_list = collision_pairs[group]

    for a in a_list:
        if not hasattr(a, 'collider') or not a.collider.active:
            continue

        for b in b_list:
            if not hasattr(b, 'collider') or not b.collider.active:
                continue

            if a.collider.collides_with(b.collider):
                if hasattr(a, 'on_collision'):
                    a.on_collision(group, b)
                if hasattr(b, 'on_collision'):
                    b.on_collision(group, a)


def check_all_collisions():
    """ 모든 충돌 페어 체크 """
    for group in collision_pairs.keys():
        check_collisions(group)

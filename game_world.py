import machine.collider_manager

world = [[], [], []]  # layers for game objects

def add_object(o, depth):
    world[depth].append(o)

def add_collision_pair(group, a, b=None):
    machine.collider_manager.add_collision_pair(group, a, b)

def add_objects(ol, depth):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            collider_manager.remove_collision_object(o)
            return

    raise Exception("World 에 존재하지 않는 오브젝트를 지우려고 시도함")


def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    for layer in world:
        layer.clear()
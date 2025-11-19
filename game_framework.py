import time
from machine.time_manager import TimeManager
from machine.camera_manager import CameraManager
from machine.key_manager import KeyManager
import machine.collider_manager

frame_time = 0.0
running = None
stack = None
time_manager = None
camera_manager = None
key_manager = None

def change_mode(mode):
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    global stack
    if (len(stack) > 0):
        # execute the current mode's finish function
        stack[-1].finish()
        # remove the current mode
        stack.pop()

    # execute resume function of the previous mode
    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_mode,screen_width=1080,screen_height=500,world_width=None,world_height=None):
    global running, stack, time_manager, camera_manager, key_manager
    running = True
    stack = [start_mode]
    time_manager = TimeManager(fixed_dt=1 / 60.0, max_frame_time=0.25)
    camera_manager = CameraManager(screen_width,screen_height,world_width,world_height)
    key_manager = KeyManager()
    start_mode.init()





    while running:
        time_manager.update()

        stack[-1].handle_events()
        while time_manager.consume_fixed():
            stack[-1].update()
            machine.collider_manager.check_all_collisions()
            camera_manager.update(time_manager.get_fixed_dt())
            key_manager.update()
        stack[-1].draw()

        # 고정 물리 스텝


    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

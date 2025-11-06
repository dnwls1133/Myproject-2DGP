import time
from machine.time_manager import TimeManager

frame_time = 0.0
running = None
stack = None
time_manager = None

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


def run(start_mode):
    global running, stack, time_manager
    running = True
    stack = [start_mode]
    time_manager = TimeManager(fixed_dt=1 / 60.0, max_frame_time=0.25)
    start_mode.init()





    while running:
        time_manager.update()

        stack[-1].handle_events()
        while time_manager.consume_fixed():
            stack[-1].update()
        stack[-1].draw()

        # 고정 물리 스텝


    # repeatedly delete the top of the stack
    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

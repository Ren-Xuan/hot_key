from global_hotkeys import *

import time

from mouse import Mouse

# Flag to indicate the program whether should continue running.
is_alive = True
quit = False

# Our keybinding event handlers.

def exit_application():
    global is_alive
    global quit
    stop_checking_hotkeys()
    is_alive = False
    quit = True


mouse = Mouse()
def move():
    mouse.move_random()
def start():
    global is_alive
    is_alive = True
def pause():
    global is_alive
    is_alive = False

# Declare some key bindings.
# These take the format of [<key list>, <keydown handler callback>, <keyup handler callback>]
bindings = [
    [["control","f10"], None, start],
    [["control","f11"], None, pause],
    [["control","f12"], None, exit_application],
]

# Register all of our keybindings
register_hotkeys(bindings)

# Finally, start listening for keypresses
start_checking_hotkeys()

# Keep waiting until the user presses the exit_application keybinding.
# Note that the hotkey listener will exit when the main thread does.
while not quit:
    time.sleep(0.1)
    time1 = time.time()
    if is_alive:
        move()
    time2 = time.time()
    print(time2-time1)
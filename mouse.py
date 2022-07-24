import ctypes
import random
import time
import win32api
import win32con
class Mouse:
    def __init__(self):
        self.pos = (random.randint(1,120),random.randint(1,120))
    def move(self,pos):
        ctypes.windll.user32.SetCursorPos(pos[0],pos[1])
    def move_random(self):
        x = random.randint(100,520)
        y = random.randint(100,520)
        self.move((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        print(x,y)
        #time.sleep(0.1)
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 ,0, 0, 0)
        
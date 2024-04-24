import pyautogui
import time
import sys
import threading

class VirtualPaintController:
    gc_mode = 0

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.mouse_position = (0, 0)
        self.left_button_pressed = False
        self.right_button_pressed = False

    def start(self):
        self.gc_mode = 1
        while self.gc_mode == 1:
            if self.left_button_pressed:
                pyautogui.click(self.mouse_position)
            if self.right_button_pressed:
                pyautogui.rightClick(self.mouse_position)
            time.sleep(0.1)

    
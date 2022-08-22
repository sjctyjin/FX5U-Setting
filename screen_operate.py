import time

import pyautogui
import threading
from PIL import Image


def enter():
   time.sleep(3)
   pyautogui.hotkey("enter")


im = Image.new("RGBA", (1920, 1080), (0, 255, 0, 255))
threading.Thread(target=enter).start()
im.show()
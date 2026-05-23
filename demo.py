import pyautogui
import time

# 每隔15秒按下数字1
while True:
    pyautogui.press('1')
    print("已按下按键1")
    time.sleep(15)
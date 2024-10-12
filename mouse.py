import pyautogui
import time

try:
    while True:
        # 获取当前鼠标位置
        x, y = pyautogui.position()
        # 打印坐标
        print(f"Mouse position: X={x}, Y={y}")
        # 每隔一秒检测一次
        time.sleep(1)
except KeyboardInterrupt:
    print("Program terminated.")

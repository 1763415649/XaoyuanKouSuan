import pyautogui
import pytesseract
import time
from functools import wraps


# 装饰器：捕获异常并记录日志
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            return None

    return wrapper


# 装饰器：记录函数执行时间
def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f} seconds")
        return result

    return wrapper


# 按照坐标截图并处理图像
@handle_exceptions
@timing
def process_pictures(region):
    img = pyautogui.screenshot(region=region)

    img = img.convert('L')  # 转换为灰度模式
    threshold = 127
    img = img.point(lambda x: 0 if x < threshold else 255)  # 应用阈值
    img = img.convert('1')  # 转换为二值模式
    return img


# 使用Tesseract进行OCR识别
@handle_exceptions
@timing
def identify(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    config = r'--oem 3 --psm 6'
    number = pytesseract.image_to_string(img, config=config)
    return number.strip()


# 比较两个数字并执行相应操作
@handle_exceptions
@timing
def compare(number1, number2):
    pyautogui.moveTo(200, 640)
    if number1 == number2:
        pyautogui.dragTo(360, 640)
        pyautogui.moveTo(200, 720)
        pyautogui.dragTo(360, 720)
    elif number1 < number2:
        pyautogui.dragTo(100, 720)
        pyautogui.dragTo(200, 800)
    else:
        pyautogui.dragTo(350, 720)
        pyautogui.dragTo(200, 800)


if __name__ == "__main__":
    for i in range(100):
        img1 = process_pictures(region=(50, 240, 125, 110))
        img2 = process_pictures(region=(240, 240, 125, 110))

        if img1 and img2:
            number1 = identify(img1)
            number2 = identify(img2)

            if number1 and number2:
                compare(number1.replace(' ', '').replace('\n', ''),
                        number2.replace(' ', '').replace('\n', ''))

                print(f'第{i}题 {number1} {number2}')
                time.sleep(0.5)
        else:
            break

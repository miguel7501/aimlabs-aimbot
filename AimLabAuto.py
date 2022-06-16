from win32gui import GetWindowText, EnumWindows, GetWindowRect
from PIL import ImageGrab
import pydirectinput
import cv2
import numpy as np
from time import sleep
import win32api, win32con
def mouse_move_relative(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0) 


windows_list = []

def enum_win(hwnd, result):
    win_text = GetWindowText(hwnd)
    windows_list.append((hwnd, win_text))

EnumWindows(enum_win, [])

def get_window(window_name):
    for (hwnd, win_text) in windows_list:
        if window_name in win_text.lower():
            game_hwnd = hwnd
            return GetWindowRect(game_hwnd)



def get_center_coordinates():
    image = np.array(ImageGrab.grab(bbox=get_window("_tb")))
    lower = np.array([22, 93, 0], dtype="uint8")
    upper = np.array([45, 255, 255], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
    cv2.imwrite("screenshot.jpg", image)
    cv2.imwrite("screenshot2.jpg", mask)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    centers = []
    for c in cnts:
        center_point, radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            centers.append((int(center_point[0]), int(center_point[1])))

    return centers



def center_window():
    coords = get_window("_tb")
    x_center = int((coords[0]+coords[2])/2)
    y_center = int((coords[1]+coords[3])/2)
    return x_center, y_center

def targets():
    centers = get_center_coordinates()
    centers = np.array(centers)
    coords = center_window()
    coords = np.array(coords)
    distances = np.linalg.norm(centers-coords, axis=1)
    min_index = np.argmin(distances)
    return centers[min_index]

    


def aim():
    target = targets()
    x_center, y_center = center_window() 
    x_travel = x_center - target[0]
    y_travel = y_center - target[1]
    mouse_move_relative(-1*int(x_travel),-1*int(y_travel))
    mouse_click()
    sleep(0.00001)

sleep(3)    
while True:
    aim()

#Y-Axis Sensitivity Force 1:1
#Sensitivity 1
#FOV 50

"""
def aim():
    target = targets()
    x_center, y_center = center_window() 
    x_travel = x_center - target[0]
    y_travel = y_center - target[1]
    print(f"xt={x_travel} yt={y_travel}")
    while x_travel > 15:
        pydirectinput.press("left")
        target = targets()
        x_center, y_center = center_window() 
        x_travel = x_center - target[0]
    while x_travel < -15:
        pydirectinput.press("right")
        target = targets()
        x_center, y_center = center_window() 
        x_travel = x_center - target[0]
    while y_travel > 15:
        pydirectinput.press("up")
        target = targets()
        x_center, y_center = center_window() 
        y_travel = y_center - target[1]
    while y_travel < -15:
        print(y_travel)
        pydirectinput.press("down")
        target = targets()
        x_center, y_center = center_window() 
        y_travel = y_center - target[1]
    pydirectinput.keyDown("space")
    pydirectinput.keyUp("space")



sleep(2)    
while True:
    aim()
"""
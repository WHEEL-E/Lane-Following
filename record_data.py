import datetime
import os
import time

import cv2
import pygame

import control
import keyboard_control


def take_snapshot(frame, path):
    """
    Take a snapshot of the current frame and save it to the given path
    """
    file_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f") + ".jpg"
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(os.path.join(path, file_name), frame)


def record_data(src, delay):
    """
    Record data and save it
    """
    pygame.init()
    win = pygame.display.set_mode((100, 100))
    cap = cv2.VideoCapture(src)
    stop_flag = True
    while True:
        ret, frame = cap.read()
        if keyboard_control.getKey("UP") or keyboard_control.getKey("w"):
            control.forward()
            take_snapshot(frame, "data/raw/forward")
            stop_flag = False
        elif keyboard_control.getKey("LEFT") or keyboard_control.getKey("a"):
            control.left()
            take_snapshot(frame, "data/raw/left")
            stop_flag = False
        elif keyboard_control.getKey("DOWN") or keyboard_control.getKey("s"):
            control.backward()
            stop_flag = False
        elif keyboard_control.getKey("RIGHT") or keyboard_control.getKey("d"):
            control.right()
            take_snapshot(frame, "data/raw/right")
            stop_flag = False
        elif keyboard_control.getKey("SPACE"):
            if not stop_flag:
                control.stop()
            take_snapshot(frame, "data/raw/stop")
        else:
            if not stop_flag:
                control.stop()
                take_snapshot(frame, "data/raw/stop")
                stop_flag = True

        time.sleep(delay)


record_data(src=0, delay=0.5)

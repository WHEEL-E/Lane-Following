import datetime
import os
import time

import cv2
import pygame

import control
import keyboard_control


def take_snapshot(frame, path):
    file_name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    if not os.path.exists(path):
        os.makedirs(path)
    h, w, c = frame.shape
    frame = frame[int(h / 2) :, :, :]
    frame = cv2.resize(frame, (200, 66), cv2.INTER_AREA)
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YUV)
    cv2.imwrite(os.path.join(path, file_name), frame)


def record_data(src, delay):
    pygame.init()
    win = pygame.display.set_mode((100, 100))
    cap = cv2.VideoCapture(src)
    stop_flag = False
    while True:
        ret, frame = cap.read()
        if keyboard_control.getKey("UP") or keyboard_control.getKey("w"):
            control.forward()
            take_snapshot(frame, "data/forward")
            stop_flag = False
        elif keyboard_control.getKey("LEFT") or keyboard_control.getKey("a"):
            control.left()
            take_snapshot(frame, "data/left")
            stop_flag = False
        elif keyboard_control.getKey("DOWN") or keyboard_control.getKey("s"):
            control.backward()
            stop_flag = False
        elif keyboard_control.getKey("RIGHT") or keyboard_control.getKey("d"):
            control.right()
            take_snapshot(frame, "data/right")
            stop_flag = False
        else:
            if not stop_flag:
                control.stop()
                take_snapshot(frame, "data/stop")
                stop_flag = True

        time.sleep(delay)


record_data(src=0, delay=1)

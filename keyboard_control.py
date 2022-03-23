import time

import keyboard

import control


def main(delay):
    stop_flag = True

    while True:
        if keyboard.is_pressed("w") or keyboard.is_pressed("up"):
            control.forward()
            stop_flag = False
        elif keyboard.is_pressed("a") or keyboard.is_pressed("left"):
            control.left()
            stop_flag = False
        elif keyboard.is_pressed("s") or keyboard.is_pressed("down"):
            control.backward()
            stop_flag = False
        elif keyboard.is_pressed("d") or keyboard.is_pressed("right"):
            control.right()
            stop_flag = False
        else:
            if not stop_flag:
                control.stop()
                stop_flag = True

        time.sleep(delay)

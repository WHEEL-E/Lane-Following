import time

import pygame

import control


def getKey(keyName):
    ret = False
    for event in pygame.event.get():
        pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, "K_{}".format(keyName))
    if keyInput[myKey]:
        ret = True
    pygame.display.update()
    return ret


def main(delay):
    pygame.init()
    win = pygame.display.set_mode((100, 100))
    stop_flag = True

    while True:
        if getKey("UP") or getKey("w"):
            control.forward()
            stop_flag = False
        elif getKey("LEFT") or getKey("a"):
            control.left()
            stop_flag = False
        elif getKey("DOWN") or getKey("s"):
            control.backward()
            stop_flag = False
        elif getKey("RIGHT") or getKey("d"):
            control.right()
            stop_flag = False
        else:
            if not stop_flag:
                control.stop()
                stop_flag = True
        time.sleep(delay)

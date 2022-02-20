import pygame

import control


def getKey(keyName):
    ans = False
    for event in pygame.event.get():
        pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame, "K_{}".format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()
    return ans


def main():
    pygame.init()
    win = pygame.display.set_mode((100, 100))

    while True:
        if getKey("UP") or getKey("w"):
            control.forward()
        elif getKey("LEFT") or getKey("a"):
            control.left()
        elif getKey("DOWN") or getKey("s"):
            control.backward()
        elif getKey("RIGHT") or getKey("d"):
            control.right()
        else:
            control.stop()

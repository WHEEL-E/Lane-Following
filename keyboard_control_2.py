from queue import Queue
from time import sleep

from pynput import keyboard

import control

# import sys
# import termios

# termios.tcflush(sys.stdin, termios.TCIOFLUSH)

queue = Queue()


def on_press(key):
    if queue.empty():
        queue.put(key)


def on_release(key):
    if (
        key == keyboard.Key.up
        or str(key) == "'w'"
        or key == keyboard.Key.left
        or str(key) == "'a'"
        or key == keyboard.Key.down
        or str(key) == "'s'"
        or key == keyboard.Key.right
        or str(key) == "'d'"
    ):
        queue.get()
        control.stop()


def main():
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while True:
        key = queue.get()
        if key == keyboard.Key.up or str(key) == "'w'":
            control.forward()
        elif key == keyboard.Key.left or str(key) == "'a'":
            control.left()
        elif key == keyboard.Key.down or str(key) == "'s'":
            control.backward()
        elif key == keyboard.Key.right or str(key) == "'d'":
            control.right()

        sleep(0.5)


main()

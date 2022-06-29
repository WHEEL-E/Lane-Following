import sshkeyboard

import control


def on_press(key):
    if key == "w":
        control.forward()
    elif key == "s":
        control.backward()
    elif key == "a":
        control.left()
    elif key == "d":
        control.right()
    elif key == "o":
        control.stop()


def on_release(key):
    if key == "w" or key == "s" or key == "a" or key == "d" or key == "o":
        control.stop()


def main() -> None:
    try:
        sshkeyboard.listen_keyboard(on_press, on_release, delay_second_char=0.3)
    except KeyboardInterrupt:
        control.uart.close()
        control.stop()


if __name__ == "__main__":
    control.main()
    main()

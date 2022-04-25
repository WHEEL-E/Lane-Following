import sys

import keyboard_control
import lane_follower
import record_data


def main():
    """
    Select the mode of operation from mobile phone
    0: Keyboard control
    1: Mobile control
    2: Lane following
    3: Autonomous driving
    4: Record data
    """
    if len(sys.argv) != 2:
        sys.exit(
            "Usage: python3 main.py {mode}\n 0: Keyboard control\n 1: Mobile control\n 2: Lane following\n 3: Autonomous driving\n 4: Record data"
        )
    mode: str = sys.argv[1]

    if mode == "0":
        keyboard_control.main(0.2)
    elif mode == "1":
        pass
    elif mode == "2":
        lane_follower.main(preview=True, intialize=True)
    elif mode == "3":
        pass
    elif mode == "4":
        record_data.main(delay=0.5)
    else:
        sys.exit(
            "Usage: python3 main.py {mode}\n 0: Keyboard control\n 1: Mobile control\n 2: Lane following\n 3: Autonomous driving\n 4: Record data"
        )


if __name__ == "__main__":
    main()

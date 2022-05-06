import sys

import collect_data
import control
import keyboard_control
import lane_follower


def main():
    """
    Select the mode of operation from mobile phone
    0: Keyboard control
    1: Mobile control
    2: Lane following
    3: Autonomous driving
    4: Collect training data
    """
    control.main()

    if len(sys.argv) != 2:
        sys.exit(
            "\n Usage: python3 main.py {mode}\n 0: Keyboard control\n 1: Mobile control\n 2: Lane following\n 3: Autonomous driving\n 4: Collect training data\n"
        )
    mode: str = sys.argv[1]

    if mode == "0":
        keyboard_control.main(delay=0.25)
    elif mode == "1":
        pass
    elif mode == "2":
        lane_follower.main()
    elif mode == "3":
        pass
    elif mode == "4":
        collect_data.main(delay=0.25)
    else:
        sys.exit(
            "\n Usage: python3 main.py {mode}\n 0: Keyboard control\n 1: Mobile control\n 2: Lane following\n 3: Autonomous driving\n 4: Collect training data\n"
        )


if __name__ == "__main__":
    main()

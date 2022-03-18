import keyboard_control
import lane_follower


def select_mode(mode):
    """
    Select the mode of operation from mobile phone
    0: Keyboard control
    1: Lane following
    2: Autonomous driving
    """
    if mode == 0:
        keyboard_control.main(delay=1)
    elif mode == 1:
        lane_follower.main(src=0, preview=True)
    elif mode == 2:
        pass


select_mode(1)

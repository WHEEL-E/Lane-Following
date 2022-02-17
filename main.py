import keyboard_control
import lane_follower


def select_mode(mode):
    """
    Select the mode of operation from mobile phone
    0: Keyboard control
    1: Bluetooth control
    2: Lane following
    3: Autonomous driving
    """
    if mode == 0:
        keyboard_control.main()
    elif mode == 1:
        pass
    elif mode == 2:
        lane_follower.main(preview=True)
    elif mode == 3:
        pass


select_mode(2)

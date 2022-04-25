import cv2
import numpy as np

import camera
import control
import utils


def take_action(no_lane, curve_value, stop_flag, min_curve) -> bool:
    """
    Take action based on the result of the lane detection
    """
    if no_lane:
        if not stop_flag:
            control.stop()
            stop_flag = True
    elif -min_curve < curve_value < min_curve and not no_lane:
        control.forward()
        stop_flag = False
    elif curve_value > min_curve and not no_lane:
        control.right()
        stop_flag = False
    elif curve_value < -min_curve and not no_lane:
        control.left()
        stop_flag = False

    return stop_flag


def main(preview: bool = False, intialize: bool = False, flip: bool = True):
    stop_flag = False
    w, h = 480, 360

    if intialize:
        utils.create_trackbar(w, h)
    else:
        (
            h_min,
            h_max,
            s_min,
            s_max,
            v_min,
            v_max,
            w_top,
            w_bot,
            h_top,
            h_bot,
        ) = utils.load_values()

    while True:
        frame = camera.capture()
        frame = cv2.resize(frame, (w, h))

        if flip:
            frame = cv2.flip(frame, 1)

        if intialize:
            (
                h_min,
                h_max,
                s_min,
                s_max,
                v_min,
                v_max,
                w_top,
                w_bot,
                h_top,
                h_bot,
            ) = utils.get_trackbar()

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        points = [
            [w_top, h_top],
            [w - w_top, h_top],
            [w_bot, h_bot],
            [w - w_bot, h_bot],
        ]

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_warp = camera.get_warp(frame_hsv, points, w, h)
        mask = cv2.inRange(frame_warp, lower, upper)
        result = cv2.bitwise_and(frame_warp, frame_warp, mask=mask)
        camera.warp_helper(frame_hsv, points)

        base_point, hist_img = utils.get_histogram(mask, 0.5, 8)
        curve_value = base_point - w // 2

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

        if preview:
            stack = np.hstack([mask, result, hist_img])
            cv2.imshow("stack", stack)

        no_lane = utils.no_lane(mask)

        stop_flag = take_action(no_lane, curve_value, stop_flag, min_curve=25)

        if cv2.waitKey(1) & 0xFF == 27:
            control.stop()
            break

    cv2.destroyAllWindows()

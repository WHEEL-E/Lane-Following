import cv2
import numpy as np
import utils
import control


def main(src=0, preview=False):
    w, h = 480, 360
    utils.create_trackbar(w, h)
    capture = cv2.VideoCapture(src)

    while True:
        ret, frame = capture.read()
        if ret == False:
            capture = cv2.VideoCapture(src)
            ret, frame = capture.read()

        frame = cv2.resize(frame, (w, h))

        h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot = utils.get_trackbar()

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        points = [[w_top, h_top], [w - w_top, h_top],
                  [w_bot, h_bot], [w - w_bot, h_bot]]

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_warp = utils.get_warp(frame_hsv, points, w, h)
        mask = cv2.inRange(frame_warp, lower, upper)
        result = cv2.bitwise_and(frame_warp, frame_warp, mask=mask)
        utils.warp_helper(frame_hsv, points)

        base_point, hist_img = utils.get_histogram(mask, 0.5, 5)
        curve_value = base_point - w//2

        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        ros = utils.region_of_interest(mask)

        if preview:
            stack = np.hstack([ros, mask, hist_img])
            cv2.imshow('stack', stack)

        no_lane = utils.no_lane(ros)

        if no_lane:
            control.stop()
        elif -25 < curve_value < 25 and not no_lane:
            control.forward()
        elif curve_value > 25 and not no_lane:
            control.right()
        elif curve_value < -25 and not no_lane:
            control.left()

        if cv2.waitKey(1) & 0xFF == 27:
            control.stop()
            break

    capture.release()
    cv2.destroyAllWindows()

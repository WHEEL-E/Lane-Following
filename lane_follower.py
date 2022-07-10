import cv2
import numpy as np

import camera
import control
import profiling
import utils


def take_action(
    no_lane: bool, curve_value: int, last_action: bool, min_curve: float
) -> bool:
    """
    Take action based on the result of the lane detection
    """
    control.main()

    if no_lane and last_action != "o":
        control.stop()
        last_action = "o"
    elif -min_curve < curve_value < min_curve and not no_lane and last_action != "w":
        control.forward()
        last_action = "w"
    elif curve_value > min_curve and not no_lane and last_action != "d":
        control.right()
        last_action = "d"
    elif curve_value < -min_curve and not no_lane and last_action != "a":
        control.left()
        last_action = "a"

    return last_action


@profiling.profile
def main(preview: bool = 0, intialize: bool = False):
    last_action = "o"

    if intialize:
        utils.create_trackbar(camera.width, camera.height)
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

    try:
        while True:
            frame = camera.capture()
            frame = camera.resize(frame, camera.width, camera.height)

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
                [camera.width - w_top, h_top],
                [w_bot, h_bot],
                [camera.width - w_bot, h_bot],
            ]

            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame_warp = camera.get_warp(frame_hsv, points, camera.width, camera.height)
            mask = cv2.inRange(frame_warp, lower, upper)
            result = cv2.bitwise_and(frame_warp, frame_warp, mask=mask)
            camera.warp_helper(result, points)

            base_point, hist_img = utils.get_histogram(mask, 0.5, 8)
            curve_value = base_point - camera.width // 2

            no_lane = utils.no_lane(mask)

            last_action = take_action(
                no_lane, curve_value, last_action, min_curve=100.0
            )

            if preview:
                mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
                stack = np.hstack([mask, result, hist_img])
                camera.preview(stack)

    except KeyboardInterrupt:
        control.stop()
        camera.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    control.main()
    main(preview=True, intialize=True)

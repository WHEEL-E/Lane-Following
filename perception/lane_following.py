import cv2
import numpy as np
import utils

def main():
    w, h = 480, 360
    utils.create_trackbar(w, h)
    video = 'test.mp4'
    capture = cv2.VideoCapture(video)
    while True:
        ret, frame = capture.read()
        if ret == False:
            capture = cv2.VideoCapture(video)
            ret, frame = capture.read()

        frame = cv2.resize(frame, (w, h))

        h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot = utils.get_trackbar()

        upper = np.array([h_max, s_max, v_max])
        lower = np.array([h_min, s_min, v_min])

        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        points = [[w_top, h_top], [w - w_top, h_top], [w_bot, h_bot], [w - w_bot, h_bot]]

        frame_warp = utils.get_warp(frame_hsv, points, w, h)
        warp_points = utils.warp_helper(frame_hsv, points)

        mask = cv2.inRange(frame_warp, lower, upper)
        result = cv2.bitwise_and(frame_warp, frame_warp, mask=mask)
        
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        stack = np.hstack([frame_hsv, result, frame_warp])
        cv2.imshow('stack', stack)

        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == '__main__':
    main()
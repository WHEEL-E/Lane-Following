import time

import cv2
import numpy as np

import control


class KeyboardInterrupt(Exception):
    """
    Keyboard interrupt exception
    """

    pass


prev_frame_time: float = 0
width, height, fps = 480, 360, 30
cap = cv2.VideoCapture(0)


def set_stream(width, height, fps):
    """
    configure the capture stream
    """
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)


def capture():
    """
    Capture the frame
    """
    ret, frame = cap.read()
    return frame


def no_light(frame):
    """
    Check if there is no light in the frame
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return cv2.countNonZero(thresh)


def resize(frame, width, height):
    """
    Resize the frame
    """
    return cv2.resize(frame, (width, height))


def convert_YUV(frame):
    """
    Convert the frame to YUV color space.
    """
    return cv2.cvtColor(frame, cv2.COLOR_RGB2YUV)


def preview(frame, fps: bool):
    """
    Preview the frame with fps
    """
    if fps:
        global prev_frame_time
        new_frame_time = time.time()
        frame_rate = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        frame_rate = int(frame_rate)
        cv2.putText(
            frame,
            str(frame_rate),
            (7, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (100, 255, 0),
            3,
            cv2.LINE_AA,
        )

    cv2.imshow("Preview", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        control.stop()
        cap.release()
        cv2.destroyAllWindows()
        raise KeyboardInterrupt


def get_warp(frame, points, w, h):
    """
    Get the warp matrix
    """
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(frame, matrix, (w, h))


def warp_helper(frame, points):
    """
    Helper function for warp function to draw the warp points
    """
    for x in range(4):
        cv2.circle(frame, (points[x][0], points[x][1]), 8, (0, 0, 255), cv2.FILLED)
    return frame


def region_of_interest(frame, a=0.917, b=0.57, c=0.125, d=0.43, h=0.62):
    """
    Get region of interest from the frame
    """
    bot_right = np.array([frame.shape[1] * a, frame.shape[0]], dtype="int")
    top_right = np.array([frame.shape[1] * b, frame.shape[0] * h], dtype="int")
    bot_left = np.array([frame.shape[1] * c, frame.shape[0]], dtype="int")
    top_left = np.array([frame.shape[1] * d, frame.shape[0] * h], dtype="int")
    vertices = [np.array([bot_left, top_left, top_right, bot_right])]

    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, vertices, color=(255, 0, 255))

    return cv2.bitwise_and(frame, mask)

import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def capture():
    """
    Capture the frame
    """
    ret, frame = cap.read()
    return frame


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

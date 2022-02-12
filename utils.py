import numpy as np
import cv2


def load_values():
    """
    Load trackbar values from file
    """
    file = open('trackbars.txt', 'r')
    h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot = file.read().splitlines()
    return int(h_min), int(h_max), int(s_min), int(s_max), int(v_min), int(v_max), int(w_top), int(w_bot), int(h_top), int(h_bot)


def save_values(values):
    """
    Save trackbar values to file
    """
    file = open('trackbars.txt', 'w')
    for value in values:
        file.write(str(value) + '\n')
    file.close()


def empty(x):
    """
    Empty function for trackbar
    """
    pass


def create_trackbar(w, h):
    """
    Create trackbars for setting parameters
    """
    cv2.namedWindow('Setting parameters')
    cv2.resizeWindow('Setting parameters', 360, 480)
    h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot = load_values()
    cv2.createTrackbar('h_min', 'Setting parameters', h_min, 255, empty)
    cv2.createTrackbar('h_max', 'Setting parameters', h_max, 255, empty)
    cv2.createTrackbar('s_min', 'Setting parameters', s_min, 255, empty)
    cv2.createTrackbar('s_max', 'Setting parameters', s_max, 255, empty)
    cv2.createTrackbar('v_min', 'Setting parameters', v_min, 255, empty)
    cv2.createTrackbar('v_max', 'Setting parameters', v_max, 255, empty)
    cv2.createTrackbar('w_top', 'Setting parameters', w_top, w//2, empty)
    cv2.createTrackbar('h_top', 'Setting parameters', h_top, h, empty)
    cv2.createTrackbar('w_bot', 'Setting parameters', w_bot, w//2, empty)
    cv2.createTrackbar('h_bot', 'Setting parameters', h_bot, h, empty)


def get_trackbar():
    """
    Get trackbar values
    """
    h_min = cv2.getTrackbarPos('h_min', 'Setting parameters')
    h_max = cv2.getTrackbarPos('h_max', 'Setting parameters')
    s_min = cv2.getTrackbarPos('s_min', 'Setting parameters')
    s_max = cv2.getTrackbarPos('s_max', 'Setting parameters')
    v_min = cv2.getTrackbarPos('v_min', 'Setting parameters')
    v_max = cv2.getTrackbarPos('v_max', 'Setting parameters')
    w_top = cv2.getTrackbarPos('w_top', 'Setting parameters')
    w_bot = cv2.getTrackbarPos('w_bot', 'Setting parameters')
    h_top = cv2.getTrackbarPos('h_top', 'Setting parameters')
    h_bot = cv2.getTrackbarPos('h_bot', 'Setting parameters')

    save_values([h_min, h_max, s_min, s_max, v_min,
                v_max, w_top, w_bot, h_top, h_bot])

    return h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot


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
        cv2.circle(frame, (points[x][0], points[x][1]),
                   8, (0, 0, 255), cv2.FILLED)
    return frame


def get_curve(frame, percent, region, preview=True):
    """
    Get histogram of an image
    """
    hist_values = np.sum(frame, axis=0)
    max_values = np.max(hist_values)
    min_values = percent*max_values

    index = np.where(hist_values >= min_values)
    base_point = int(np.average(index))

    if preview:
        hist_img = np.zeros(
            (frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
        for x, intenisty in enumerate(hist_values):
            cv2.line(
                hist_img, (x, frame.shape[0]), (x, frame.shape[0] - intenisty//255//region), (0, 0, 255), 1)
            cv2.circle(
                hist_img, (base_point, frame.shape[0]), 8, (0, 255, 255), cv2.FILLED)
        return base_point, hist_img

    return base_point
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


def region_of_interest(frame, a=0.917, b=0.57, c=0.125, d=0.43, h=0.62):
    """
    Get region of interest from the frame
    """
    bot_right = np.array([frame.shape[1] * a, frame.shape[0]], dtype='int')
    top_right = np.array([frame.shape[1] * b, frame.shape[0] * h], dtype='int')
    bot_left = np.array([frame.shape[1] * c, frame.shape[0]], dtype='int')
    top_left = np.array([frame.shape[1] * d, frame.shape[0] * h], dtype='int')
    vertices = [np.array([bot_left, top_left, top_right, bot_right])]

    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, vertices, 255)

    return cv2.bitwise_and(frame, mask)


def get_histogram(frame, percent, region):
    """
    Get histogram of an image
    """
    hist_values = np.sum(frame, axis=0)
    max_values = np.max(hist_values)
    min_values = percent*max_values

    index = np.where(hist_values >= min_values)
    base_point = int(np.average(index))

    hist_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    for x, intenisty in enumerate(hist_values):
        cv2.line(
            hist_img, (x, frame.shape[0]), (x, frame.shape[0] - intenisty//255//region), (0, 0, 255), 1)
        cv2.circle(
            hist_img, (base_point, frame.shape[0]), 8, (0, 255, 255), cv2.FILLED)
    return base_point, hist_img


def no_lane(frame, max=8):
    """
    Check if there is no lane in the frame
    """
    hist_values = np.sum(frame, axis=0)
    max_values = round(0.001*np.max(hist_values))

    if max_values < max:
        return True
    return False

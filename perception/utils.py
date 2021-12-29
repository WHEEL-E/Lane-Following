import numpy as np
from cv2 import cv2

def empty(x):
    pass

def create_trackbar(w, h):
    cv2.namedWindow('Setting parameters')
    cv2.resizeWindow('Setting parameters', 360, 480)
    cv2.createTrackbar('h_min', 'Setting parameters', 0, 255, empty)
    cv2.createTrackbar('h_max', 'Setting parameters', 0, 255, empty)
    cv2.createTrackbar('s_min', 'Setting parameters', 0, 255, empty)
    cv2.createTrackbar('s_max', 'Setting parameters', 0, 255, empty)
    cv2.createTrackbar('v_min', 'Setting parameters', 0, 255, empty)
    cv2.createTrackbar('v_max', 'Setting parameters', 0, 255, empty)
    cv2.createTrackbar('w_top', 'Setting parameters', 0, w//2, empty)
    cv2.createTrackbar('h_top', 'Setting parameters', 0, h, empty)
    cv2.createTrackbar('w_bot', 'Setting parameters', 0, w//2, empty)
    cv2.createTrackbar('h_bot', 'Setting parameters', 0, h, empty)

def get_trackbar():
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

    return h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot


def get_warp(frame, points, w, h):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(frame, matrix, (w, h))

def warp_helper(frame, points):
    for x in range(4):
        cv2.circle(frame, (points[x][0], points[x][1]), 15, (0, 0, 255), cv2.FILLED)
    return frame
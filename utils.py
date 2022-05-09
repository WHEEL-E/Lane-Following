import cv2
import numpy as np


def load_values():
    """
    Load trackbar values from file
    """
    file = open("trackbars.txt", "r")
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
    ) = file.read().splitlines()
    return (
        int(h_min),
        int(h_max),
        int(s_min),
        int(s_max),
        int(v_min),
        int(v_max),
        int(w_top),
        int(w_bot),
        int(h_top),
        int(h_bot),
    )


def save_values(values: str):
    """
    Save trackbar values to file
    """
    with open("trackbars.txt", "w") as file:
        for value in values:
            file.write(f"{value}\n")


def empty(x):
    """
    Empty function for trackbar
    """
    pass


def create_trackbar(width, height):
    """
    Create trackbars for setting parameters
    """
    cv2.namedWindow("Setting parameters")
    cv2.resizeWindow("Setting parameters", 360, 480)
    h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot = load_values()
    cv2.createTrackbar("h_min", "Setting parameters", h_min, 255, empty)
    cv2.createTrackbar("h_max", "Setting parameters", h_max, 255, empty)
    cv2.createTrackbar("s_min", "Setting parameters", s_min, 255, empty)
    cv2.createTrackbar("s_max", "Setting parameters", s_max, 255, empty)
    cv2.createTrackbar("v_min", "Setting parameters", v_min, 255, empty)
    cv2.createTrackbar("v_max", "Setting parameters", v_max, 255, empty)
    cv2.createTrackbar("w_top", "Setting parameters", w_top, width // 2, empty)
    cv2.createTrackbar("h_top", "Setting parameters", h_top, height, empty)
    cv2.createTrackbar("w_bot", "Setting parameters", w_bot, width // 2, empty)
    cv2.createTrackbar("h_bot", "Setting parameters", h_bot, height, empty)


def get_trackbar():
    """
    Get trackbar values
    """
    h_min = cv2.getTrackbarPos("h_min", "Setting parameters")
    h_max = cv2.getTrackbarPos("h_max", "Setting parameters")
    s_min = cv2.getTrackbarPos("s_min", "Setting parameters")
    s_max = cv2.getTrackbarPos("s_max", "Setting parameters")
    v_min = cv2.getTrackbarPos("v_min", "Setting parameters")
    v_max = cv2.getTrackbarPos("v_max", "Setting parameters")
    w_top = cv2.getTrackbarPos("w_top", "Setting parameters")
    w_bot = cv2.getTrackbarPos("w_bot", "Setting parameters")
    h_top = cv2.getTrackbarPos("h_top", "Setting parameters")
    h_bot = cv2.getTrackbarPos("h_bot", "Setting parameters")

    save_values([h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot])

    return h_min, h_max, s_min, s_max, v_min, v_max, w_top, w_bot, h_top, h_bot


def get_histogram(frame, percent, region):
    """
    Get histogram of an image
    """
    hist_values = np.sum(frame, axis=0)
    max_values = np.max(hist_values)
    min_values = percent * max_values

    index = np.where(hist_values >= min_values)
    base_point = int(np.average(index))

    hist_img = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)
    for x, intenisty in enumerate(hist_values):
        cv2.line(
            hist_img,
            (x, frame.shape[0]),
            (x, frame.shape[0] - int(intenisty) // 255 // region),
            (0, 0, 255),
            1,
        )
        cv2.circle(hist_img, (base_point, frame.shape[0]), 8, (0, 255, 255), cv2.FILLED)
    return base_point, hist_img


def no_lane(frame, max=8) -> bool:
    """
    Check if there is no lane in the frame
    """
    hist_values = np.sum(frame, axis=0)
    max_values = round(0.001 * np.max(hist_values))

    if max_values < max:
        return True
    return False

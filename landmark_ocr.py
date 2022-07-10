import os
import time

import cv2
import pytesseract

import camera
import control


def main(destination: str):
    if os.name == "nt":
        pytesseract.pytesseract.tesseract_cmd = "C:\\src\\Tesseract-OCR\\tesseract.exe"

    destination = destination.lower().replace(" ", "")

    while True:
        frame = camera.capture()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(
            gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV
        )

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

        contours, hierarchy = cv2.findContours(
            dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
        )

        frame2 = frame.copy()
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            rectangle = cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cropped = frame2[y : y + h, x : x + w]
            landmark: str = pytesseract.image_to_string(cropped)
            landmark = landmark.lower().replace(" ", "").strip()
            print(landmark)
            # camera.preview(rectangle)
            take_action(landmark, destination)


def take_action(landmark: str, destination: str):
    zone1 = ["livingroom", "kitchen", "diningroom"]
    zone2 = ["bedroom1", "bedroom2", "bathroom"]

    if destination in landmark:
        control.stop()

    elif "enterance" in landmark and (destination in zone1 or destination in zone2):
        control.forward()

    elif "hall1" in landmark:
        if destination == "diningroom":
            print("go to diningroom")
            control.left()
            time.sleep(0.2)
            control.stop()
            control.forward()
            time.sleep(0.2)
            print("arrived at diningroom")
        elif destination == "livingroom":
            print("go to livingroom")
            control.right()
            time.sleep(0.2)
            control.stop()
            control.forward()
            print("arrived at livingroom")
        elif destination in zone2:
            control.forward()

    elif "hall2" in landmark:
        if destination == "bedroom1":
            print("go to bedroom1")
            control.left()
            time.sleep(0.2)
            control.stop()
            control.forward()
            print("arrived at bedroom1")
        elif destination == "bedroom2":
            print("go to bedroom2")
            control.right()
            time.sleep(0.2)
            control.stop()
            control.forward()
            print("arrived at bedroom2")
        elif destination == "bathroom":
            print("go to bathroom")
            control.forward()
            print("arrived at bathroom")


if __name__ == "__main__":
    main("bathroom")

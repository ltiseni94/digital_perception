#!usr/bin/env python3

# ANCORA NON FUNZIONANTE!!!!

import cv2
import numpy as np


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to get capture")
        exit(1)

    cv2.namedWindow("camera", cv2.WINDOW_FULLSCREEN)

    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    roi = (100, 100, 200, 200)
    track = roi

    hist0 = cv2.calcHist(hsv[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]], [0], None, [180], [0, 180])

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bp = cv2.calcBackProject(hsv, [0], hist0, [0, 180], 1)
        ret, track = cv2.CamShift(bp, track, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        x, w, y, h = track
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

        cv2.imshow("camera", frame)
        if cv2.waitKey(1) > 0:
            break

    cap.release()

#!usr/bin/env python3

import cv2
import numpy as np
from mss import mss


point = None
sel_point = False
prev_points = None


CAMERA = False


def mouse_callback(event, x, y, flag, params):

    global point, sel_point, prev_points
    if event == cv2.EVENT_LBUTTONDOWN:
        point = np.array([[x, y]], np.float32)
        sel_point = True
        prev_points = point


if __name__ == '__main__':
    if CAMERA:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Unable to get capture")
            exit(1)
    else:
        cap = mss()

    cv2.namedWindow("camera", cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("camera", mouse_callback)
    new_frame = None

    lk_params = {
        "winSize": (15, 15),
        "maxLevel": 4,
        "criteria": (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
    }

    ret = False
    while True:
        if CAMERA:
            ret, frame = cap.read()
        else:
            frame = cap.grab({
                "top": 200,
                "left": 300,
                "width": 640,
                "height": 480,
            })
            frame = np.array(frame)

        if new_frame is not None:
            prev_frame = new_frame
        new_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if CAMERA:
            if not ret:
                break

        if sel_point:
            x, y = point.ravel()
            x, y = int(x), int(y)
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            point, status, error = cv2.calcOpticalFlowPyrLK(prev_frame, new_frame, prev_points, None, **lk_params)
            prev_points = point
            x, y = point.ravel()
            x, y = int(x), int(y)
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        cv2.imshow("camera", frame)
        if cv2.waitKey(1) > 0:
            break

    cap.release()

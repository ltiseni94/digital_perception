import cv2
import numpy as np

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    frame = cv2.resize(frame, (600, 400))
    frame2 = cv2.pyrDown(frame)
    frame4 = cv2.pyrDown(frame2)
    frame8 = cv2.pyrDown(frame4)

    cv2.imshow("Frame 1:1", frame)
    cv2.imshow("Frame 1:2", frame2)
    cv2.imshow("Frame 1:4", frame4)
    cv2.imshow("Frame 1:8", frame8)

    k = cv2.waitKey(1) & 0xff
    if k == ord('q'):
        break

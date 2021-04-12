import cv2
import numpy as np
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('Error opening camera')
    exit(1)

cnt = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cnt += 1
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if cnt < 20:
        frame0 = frame
    mask = cv2.inRange(frame_hsv[:, :, 0], 90, 150)

    if frame0 is not None:
        masked_frame = cv2.bitwise_and(frame, frame, None, 255-mask)
        masked_frame0 = cv2.bitwise_and(frame0, frame0, None, mask)
        frame_final = cv2.add(masked_frame, masked_frame0)
        cv2.imshow('webcam', frame_final)

    key = cv2.waitKey(1) & 0xff
    if key is ord('q'):
        break

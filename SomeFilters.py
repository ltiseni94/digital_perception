import numpy as np
import time
from matplotlib import pyplot as plt
import cv2

cap = cv2.VideoCapture()
cap.open(1)
if not cap.isOpened():
    print("Error opening webcam")
    exit(1)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.6, fy=0.6)
    if not ret:
        break
    t_preshift = time.time()
    # frame_ms = cv2.pyrMeanShiftFiltering(frame, 15, 40)
    # frame_ms = cv2.edgePreservingFilter(frame, None, cv2.RECURS_FILTER, 20, 0.8)
    frame_ms = cv2.stylization(frame, sigma_s=20, sigma_r=0.9)
    # frame_gray, frame_col = cv2.pencilSketch(frame, sigma_s=20, sigma_r=0.09, shade_factor=.05)
    t_postshift = time.time()
    cv2.imshow("ms", np.vstack((frame, frame_ms)))
    t_show = time.time()
    k = cv2.waitKey(1)
    print(f"Tframe= {t_show - t_preshift: 5.4f} Tshift = {t_postshift - t_preshift : 5.4f}")
    t_old = time.time()
    if k == ord('q'):
        break
cap.release()

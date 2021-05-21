# !usr/bin/env python3
# coding: utf-8

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (300, 200))
    frame_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not ret:
        print('Error Acquiring from Camera')
        break
    # Questo GaussianBlur fa insieme il kernel e la convoluzione
    frame_gaus = cv2.GaussianBlur(frame_grey, (9, 9), 3)
    frame_blur = cv2.GaussianBlur(frame, (9, 9), 3)
    sobelx_frame = np.abs(cv2.Sobel(frame_gaus, cv2.CV_16S, 1, 0, None, ksize=5))
    sobely_frame = np.abs(cv2.Sobel(frame_gaus, cv2.CV_16S, 0, 1, None, ksize=5))
    sob_xy = sobelx_frame + sobely_frame
    max_xy = np.max(sob_xy)
    # ddepth, nel caso di immagini a 8 bit, tronca le derivate negative)


    # Canny frame, se uno fa prima il blur gaussiano becca solo i contorni più rilevanti.
    canny_frame = cv2.Canny(frame_blur, 40, 120, (9, 9))

    # cv2.imshow("Translated", sob_xy/max_xy)
    cv2.imshow("Canny", canny_frame)
    k = cv2.waitKey(1) & 0xff
    if k == ord('q'):
        break



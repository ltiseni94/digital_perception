#!/usr/bin/env python

import numpy as np
import cv2
import glob
import os
import sys

img = None
calib_images = []
CHESSBOARD_SIZE = (9, 6)
CELL_SIZE = 0.026
cornersVect = []
interactive = False


# Functions
def test_camera(cap):
    while True:
        is_ok, frame = cap.read()
        if not is_ok:
            print("Error acquiring a frame!")
            exit(1)

        cv2.imshow("frame", frame)
        if cv2.waitKey(10) == ord('q'):
            break

    cv2.destroyWindow("frame")


# mouse callback function
def show_pixel_value(event, x, y, flags, param):
    global img
    if event == cv2.EVENT_MOUSEMOVE:
        if x > img.shape[1]:  # avoid errors when moving cursor on display
            return
        bgr = img[y, x]
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"HUE {hsv[0]}")


def saveImages():
    for i in range(len(calib_images)):
        cv2.imwrite(f"./CalibImages/img_{i}.png", calib_images[i])


def loadImages():
    images = glob.glob("./CalibImages/img_*.png./CalibImages/img_*.png")

    for filename in sorted(images):
        print(f'Sto leggendo {filename}')
        frame = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        store_calib_image(frame)


def store_calib_image(frame):
    # check chessboard
    ret, corners = cv2.findChessboardCorners(frame, CHESSBOARD_SIZE)
    if ret == 0:
        print("No chessboard found")
        return False
    calib_images.append(frame)
    windowSize = (10, 10)  # Around cells intersections

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 0.001)
    corners2 = cv2.cornerSubPix(frame, corners, windowSize, (-1, -1), criteria)
    cornersVect.append(corners2)
    print(f"Found chessboard: {len(calib_images)}")


def get_images(cap, n_images=16):
    global img
    while len(calib_images) < n_images:
        is_ok, frame = cap.read()
        if not is_ok:
            print("Error acquiring a frame!")
            return

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("frame", frame)
        img = frame
        #        cv2.setMouseCallback("frame", show_pixel_value)
        if cv2.waitKey(10) == ord('s'):
            store_calib_image(frame_gray)
        elif cv2.waitKey(10) == ord('q'):
            break

    cv2.destroyWindow("frame")


def calib_camera():
    N = CHESSBOARD_SIZE[0]
    M = CHESSBOARD_SIZE[1]
    size = N * M
    points = np.zeros((size, 3), np.float32)
    points[:, :2] = (CELL_SIZE * np.mgrid[0:N, 0:M]).T.reshape(-1, 2)
    # points = [ np.array(i*CELL_SIZE, j*CELL_SIZE, 0, dtype=np.float32)
    #            for i in range(CHESSBOARD_SIZE[0])
    #            for j in range(CHESSBOARD_SIZE[1])]
    pointsVect = [points for i in range(len(calib_images))]
    image_size = calib_images[0].shape[::-1]

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 150, 0.0001)
    r, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(pointsVect, cornersVect, image_size, None, None, criteria)
    if r:
        print(f"RMS error: {r}")
        print(f"Camera matrix:\n {mtx}")
        print(f"Distortion vector:\n {dist}")
        print(f"tvecs 0: {tvecs[0]}")
        print(f"rvecs 0: {rvecs[0]}")
        # Salviamo i dati a file
        dataFile = cv2.FileStorage()
        dataFile.open("cameraData.yaml", cv2.FILE_STORAGE_WRITE)
        dataFile.write("K", mtx)
        dataFile.write("d", dist)
        dataFile.write("t", tvecs[0])
        dataFile.write("r", rvecs[0])
        dataFile.release()


def find_pendulum(frame, min_h, max_h):
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    ker = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

    # Mask by hue tresholding
    if min_h > max_h:
        mask = cv2.bitwise_not(cv2.inRange(frame_hsv[:, :, 0], max_h, min_h))
    else:
        mask = cv2.inRange(frame_hsv[:, :, 0], min_h, max_h)

    mask = cv2.erode(mask, ker)
#    nonZeroRows = [i for i in range(mask.shape[0]) for j in range(mask.shape[1]) if mask[i, j] != 0]
#    nonZeroCols = [j for i in range(mask.shape[0]) for j in range(mask.shape[1]) if mask[i, j] != 0]
    ball = [[i, j] for i in range(frame.shape[0]) for j in range(frame.shape[1]) if mask[i, j] != 0]
    centerRow = np.median(np.array(ball)[:, 0])
    centerCol = np.median(np.array(ball)[:, 1])
    cv2.circle(mask, (int(centerCol), int(centerRow)), 5, 128)
    cv2.imshow('Mask', mask)
    cv2.waitKey(1)


if __name__ == "__main__":
    cap = cv2.VideoCapture(1)
    if interactive:
        if not cap.isOpened():
            print("Camera not opened")
            exit(1)
        get_images(cap)
        saveImages()
    else:
        if not os.path.isfile('./cameraData.yaml'):
            loadImages()
            calib_camera()
            exit(0)
        else:
            dataFile = cv2.FileStorage()
            dataFile.open('./cameraData.yaml', cv2.FILE_STORAGE_READ)
            mtx = dataFile.getNode('K').mat()
            d = dataFile.getNode('d').mat()
            t = dataFile.getNode('t').mat()
            r = dataFile.getNode('r').mat()
        if mtx is None:
            print('Non ho i dati della matrice camera, esco...')
            exit(0)
        while True:
            ret, frame = cap.read()
            if ret:
                find_pendulum(frame, 170, 10)


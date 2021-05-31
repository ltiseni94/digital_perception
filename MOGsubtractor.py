import numpy as np
import cv2

# Mog2 implements the background as a mixture of Gaussians,
# We may set a series of parameters:
# Number of mixtures
# Variance threshold
# History Length
# Learning Rate

# Operation is performed with clear, apply and empty methods
# Apply uses learning rate to know if apply or nly store

cap = cv2.VideoCapture(1)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=100,
    detectShadows=False
)
lr = 1
step = 0
while True:
    ret, frame = cap.read()
    gm = np.mean(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    gain = 100.0/gm
    frame = frame * gain
    fgmask = fgbg.apply(frame, learningRate=lr)
    step += 1
    if step > 50:
        lr = 0
    fgmask = cv2.erode(fgmask, kernel)
    fgmask = cv2.erode(fgmask, kernel)
    r, fgmask = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)
    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

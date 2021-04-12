import cv2
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    img = cv2.imread("resources/banana.jfif")
    img_bgr = cv2.resize(img, None, fx=0.4, fy=0.4)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    img_h, img_s, img_v = cv2.split(img_hsv)
    img_b, img_r, img_g = cv2.split(img_bgr)

    filler = np.zeros(img_h.shape, dtype=np.uint8)

    img_h3 = cv2.merge((img_h, filler, filler))
    img_s3 = cv2.merge((filler, img_s, filler))
    img_v3 = cv2.merge((filler, filler, img_v))

    img_b3 = cv2.merge((img_b, filler, filler))
    img_g3 = cv2.merge((filler, img_g, filler))
    img_r3 = cv2.merge((filler, filler, img_r))

    mask = cv2.inRange(img_h, 0, 40)

    img_banana = cv2.bitwise_and(img_bgr, img_bgr, None, mask)

    row_1 = np.hstack((img_banana, img_b3))
    row_2 = np.hstack((img_g3, img_r3))
    img4x4 = np.vstack((row_1, row_2))

    cv2.imshow("banana", img4x4)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''
    nmp_hist = np.histogram(img_b, 256)

    plt.hist(img_b.ravel() , [0,256])
    plt.show()

    plt.plot(nmp_hist[1], nmp_hist[0])
    plt.show()
'''


import cv2
import numpy as np


def wb_grayworld(img):
    b, g, r = cv2.split(img)
    avg_b, avg_g, avg_r = (cv2.mean(b)[0], cv2.mean(g)[0], cv2.mean(r)[0])
    avg = (avg_b + avg_g + avg_r)/3
    k_b, k_g, k_r = (avg_b/avg, avg_g/avg, avg_r/avg)
    b_wb = cv2.addWeighted(src1=b, alpha=k_r, src2=0, beta=0, gamma=0)
    g_wb = cv2.addWeighted(src1=g, alpha=k_g, src2=0, beta=0, gamma=0)
    r_wb = cv2.addWeighted(src1=r, alpha=k_b, src2=0, beta=0, gamma=0)
    img_wb = cv2.merge([b_wb, g_wb, r_wb])
    return img_wb


def crop_mouse_callback(event, x, y, para)
    return None


def wb_brightestpixel(img):
    img = cv2.imread('resources/TooMuchBlue.JPG')
    b, g, r = cv2.split(img)

    img_b2 = cv2.addWeighted(b, 255 / b.max(), 0, 0, 0)
    img_g2 = cv2.addWeighted(g, 255 / g.max(), 0, 0, 0)
    img_r2 = cv2.addWeighted(r, 255 / r.max(), 0, 0, 0)

    img2 = cv2.merge((img_b2, img_g2, img_r2))
    return img2


def wb_stretch(img):
    return None


def wb_crop(img, crop_cbk):
    return None


if __name__ == '__main__':
    dim = (960, 639)
    images_path = ['resources/TooMuchBlue.JPG',
                   'resources/TooMuchYellow.JPG',
                   'resources/amsterdam1.JPG',
                   'resources/amsterdam2.JPG',
                   'resources/sfondo.jpg',
                   'resources/scuola.jfif',
                   ]
    images = []
    images_wb = []
    for x in images_path:
        image = cv2.imread(x)
        image = cv2.resize(image, dim)
        image_wb = wb_grayworld(image)
        images.append(image)
        images_wb.append(image_wb)
        cv2.namedWindow('original')
        cv2.moveWindow('original', 0, 0)
        cv2.imshow('original', image)
        cv2.namedWindow('balanced')
        cv2.moveWindow('balanced', 960, 0)
        cv2.imshow('balanced', image_wb)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

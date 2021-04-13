import cv2
import numpy as np


def crop_mouse_callback(event, x, y, params):
    return None


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


def wb_whitemax(img):
    b, g, r = cv2.split(img)
    b_wb = cv2.addWeighted(src1=b, alpha=(255/b.max()), src2=0, beta=0, gamma=0)
    g_wb = cv2.addWeighted(src1=g, alpha=(255/g.max()), src2=0, beta=0, gamma=0)
    r_wb = cv2.addWeighted(src1=r, alpha=(255/r.max()), src2=0, beta=0, gamma=0)
    img_wb = cv2.merge((b_wb, g_wb, r_wb))
    return img_wb


def wb_stretch(img):
    return None


def wb_crop(img, crop_cbk):
    return None


if __name__ == '__main__':
    dim = (640, 426)
    images_path = ['resources/TooMuchBlue.JPG',
                   'resources/TooMuchYellow.JPG',
                   'resources/amsterdam1.JPG',
                   'resources/amsterdam2.JPG',
                   'resources/sfondo.jpg',
                   'resources/scuola.jfif',
                   ]
    images = []
    images_wb_grayworld = []
    images_wb_whitemax = []
    for x in images_path:
        image = cv2.imread(x)
        image = cv2.resize(image, dim)

        image_wb_grayworld = wb_grayworld(image)
        image_wb_whitemax = wb_whitemax(image)

        images.append(image)
        images_wb_grayworld.append(image_wb_grayworld)
        images_wb_whitemax.append(image_wb_whitemax)
        cv2.namedWindow('original')
        cv2.moveWindow('original', 0, 0)
        cv2.imshow('original', image)

        cv2.namedWindow('grayworld')
        cv2.moveWindow('grayworld', dim[0], 0)
        cv2.imshow('grayworld', image_wb_grayworld)

        cv2.namedWindow('whitemax')
        cv2.moveWindow('whitemax', 0, dim[1])
        cv2.imshow('whitemax', image_wb_whitemax)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

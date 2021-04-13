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


def wb_whitemax(img):
    b, g, r = cv2.split(img)
    b_wb = cv2.addWeighted(src1=b, alpha=(255/b.max()), src2=0, beta=0, gamma=0)
    g_wb = cv2.addWeighted(src1=g, alpha=(255/g.max()), src2=0, beta=0, gamma=0)
    r_wb = cv2.addWeighted(src1=r, alpha=(255/r.max()), src2=0, beta=0, gamma=0)
    img_wb = cv2.merge((b_wb, g_wb, r_wb))
    return img_wb


def wb_stretch(img):
    return None


def wb_crop(img):
    img_copy = img.copy()
    x_in, y_in, x_fin, y_fin = 0, 0, 0, 0
    cropping = False
    cropped = False
    started = False
    def mouse_callback(event, x, y, flags, param):
        nonlocal x_in, y_in, x_fin, y_fin, cropping, cropped, started
        if event == cv2.EVENT_LBUTTONDOWN:
            x_in, y_in = x, y
            started = True
        elif event == cv2.EVENT_MOUSEMOVE and started is True:
            x_fin, y_fin = x, y
            cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            x_fin, y_fin = x, y
            cropping = False
            cropped = True

    cv2.namedWindow('Draw a rectangle to crop the white')
    cv2.setMouseCallback('Draw a rectangle to crop the white', mouse_callback)
    while True:
        if cropping is True:
            cv2.rectangle(img_copy, (x_in, y_in), (x_fin, y_fin), (0, 255, 0), 2)
        cv2.imshow('Draw a rectangle to crop the white', img_copy)
        cv2.waitKey(1)
        img_copy = img.copy()
        if cropped is True:
            cv2.destroyWindow('Draw a rectangle to crop the white')
            break
    white_img = img[x_in:x_fin, y_in:y_fin]
    b_white, g_white, r_white, _ = cv2.mean(white_img)
    b, g, r = cv2.split(img)
    b_wb = cv2.addWeighted(src1=b, alpha=(255/b_white), src2=0, beta=0, gamma=0)
    g_wb = cv2.addWeighted(src1=g, alpha=(255/g_white), src2=0, beta=0, gamma=0)
    r_wb = cv2.addWeighted(src1=r, alpha=(255/r_white), src2=0, beta=0, gamma=0)
    img_wb = cv2.merge((b_wb, g_wb, r_wb))
    return img_wb


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
    images_wb_ref = []

    for x in images_path:
        image = cv2.imread(x)
        image = cv2.resize(image, dim)

        image_wb_grayworld = wb_grayworld(image)
        image_wb_whitemax = wb_whitemax(image)
        image_wb_ref = wb_crop(image)

        images.append(image)
        images_wb_grayworld.append(image_wb_grayworld)
        images_wb_whitemax.append(image_wb_whitemax)
        images_wb_ref.append(image_wb_ref)

        cv2.namedWindow('original')
        cv2.moveWindow('original', 0, 0)
        cv2.imshow('original', image)

        cv2.namedWindow('grayworld')
        cv2.moveWindow('grayworld', dim[0], 0)
        cv2.imshow('grayworld', image_wb_grayworld)

        cv2.namedWindow('whitemax')
        cv2.moveWindow('whitemax', 0, dim[1])
        cv2.imshow('whitemax', image_wb_whitemax)

        cv2.namedWindow('whiteref')
        cv2.moveWindow('whiteref', dim[0], dim[1])
        cv2.imshow('whiteref', image_wb_ref)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

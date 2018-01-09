import cv2


def SobelX(image, size):
    # size: the kernel size
    return cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=size)


def SobelY(image, size):
    # size: the kernel size
    return cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=size)

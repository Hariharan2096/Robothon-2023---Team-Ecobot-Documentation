import cv2 as cv
import numpy as np
from realsense_camera1 import *
import Triangle_Class as triangle
import time

## M5 LED screen capturing

def CaptureSlider():
    time.sleep(3)
    rs = RealsenseCamera()

    for i in range(20):
        Rit, bgr, depth = rs.get_frame_stream()
        image = bgr
    return image

## Measurement of distance between Red triangle and Yellow triangle

def R2Y_dist(image):
    t_angle = triangle.Triangle(image=image)

    imgCropped = t_angle.blue_color(image=image)
    if imgCropped is not None:
        cv.imshow('cropped', imgCropped)
        print("Shape of M5 screen", imgCropped.shape)
        width_pixel = imgCropped.shape[1]
        print("width of M5 screen", width_pixel)
        centre_R = t_angle.red_color(image=imgCropped)
        if (centre_R[0], centre_R[1]) == (0, 0):
            print("Centre of Red Triangle not detected")
            distance_Y = 0
        else:
            print("centre_R", centre_R)
        centre_Y = t_angle.yellow_color(image=imgCropped)
        if (centre_Y[0], centre_Y[1]) == (0, 0) or (centre_R[0], centre_R[1]) == (0, 0):
            print("Centre of Yelloe Triangle not detected")
            print("Hence No Measurement of Distance between R and Y Triangle ")
            distance_Y = 0
        else:
            print("Centre_Y", centre_Y)
            distance_Y = t_angle.red_to_yellow(R=centre_R, Y=centre_Y, w_p=width_pixel)

    else:
        print("No Cropped Blue Screen detected")
    cv.imshow("Image", image)

    return distance_Y

## Measurement of distance between Red triangle and Green triangle

def R2G_dist(image):
    t_angle = triangle.Triangle(image=image)

    imgCropped = t_angle.blue_color(image=image)
    if imgCropped is not None:
        cv.imshow('cropped', imgCropped)
        print("Shape of M5 screen", imgCropped.shape)
        width_pixel = imgCropped.shape[1]
        centre_R = t_angle.red_color(image=imgCropped)
        if (centre_R[0], centre_R[1]) == (0, 0):
            print("Centre of Red Triangle not detected")
            distance_G = 0
        else:
            print("centre_R", centre_R)

        centre_G = t_angle.green_color(image=imgCropped)
        if (centre_G[0], centre_G[1]) == (0, 0) or (centre_R[0], centre_R[1]) == (0, 0):
            print("Centre of Green Triangle not detected")
            print("Hence No Measurement of Distance between R and G Triangle ")
            distance_G = 0
        else:
            print("Centre_G", centre_G)
            distance_G = t_angle.red_to_green(R=centre_R, G=centre_G, w_p=width_pixel)


    else:
        print("No Cropped Blue Screen detected")
    cv.imshow("Image", image)

    return distance_G


cv.waitKey(0)

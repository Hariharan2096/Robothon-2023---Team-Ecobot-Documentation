import cv2 as cv
import numpy as np
import math
from realsense_camera1 import *

## Identifying Blue button Feature

def blue_color(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_blue = np.array([78, 158, 124])
    upper_blue = np.array([138, 255, 255])
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    contour, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contour, key=lambda x: cv.contourArea(x))
    centre_B = (0, 0)
    cv.imshow("Mask", mask)
    for cnt in cntsSorted:
        area = cv.contourArea(cnt)
        print("Area:",area)
        perimeter = cv.arcLength(cnt,True)
        approx = cv.approxPolyDP(cnt,0.02*perimeter,True)
        objlen = len(approx)
        print(objlen)

        if 1000 < area <4000 and objlen > 7  :
            
            M = cv.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv.circle(image, (cX, cY), 2, (0, 255, 0), 2)

            centre_B = (cX, cY)
    return centre_B

## Identifying Red button Feature


def red_color(image):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 245, 245])
    mask2 = cv.inRange(hsv, lower_red, upper_red)

    mask = mask1 | mask2

    contour, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contour, key=lambda x: cv.contourArea(x))
    cv.imshow("Red_Mask", mask)
    centre_R = (0, 0)
    for cnt in cntsSorted:
        area = cv.contourArea(cnt)
        perimeter = cv.arcLength(cnt, True)
        if 2000 < area < 4900 and perimeter < 250:
            M = cv.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv.circle(image, (cX, cY), 2, (0, 255, 0), 2)
            centre_R = (cX, cY)
    return centre_R

## Calculation of orientation angle using Red button and Blue button centre

def find_angle(centreR, centreB):
    (x1, y1) = centreR
    (x2, y2) = centreB
    b_angle = math.atan2(y2 - y1, x2 - x1) * (180 / math.pi)

    if b_angle < 0:
        b_angle += 360

    b_angle = 360 - b_angle
    print(b_angle)
    return b_angle

## Execution of Orientation angle identification script

def GetRotationAngle():

    rs = RealsenseCamera()

    for i in range():
        Rit, bgr, depth = rs.get_frame_stream()
        image = bgr
    centre_B = blue_color(image=image)
    print("Centre_B:", centre_B)
    centre_R = red_color(image=image)
    print("Centre_R:", centre_R)
    b_angle = find_angle(centreR=centre_R, centreB=centre_B)
    print("b_angle:", b_angle)
    cv.imshow("Image", image)
    cv2.waitKey(5)

    return b_angle


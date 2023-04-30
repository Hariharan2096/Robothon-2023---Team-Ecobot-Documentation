import cv2
import numpy as np
from realsense_camera import *

center_R = (0, 0)
center_B = (0, 0)

## Detection of Red button in Micro Pose

def red_center(input_image):
    img = input_image.copy()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 70, 50])
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 70, 50])
    upper_red = np.array([180, 245, 245])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    mask = mask1 | mask2
    
    contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cntsSorted = sorted(contour, key=lambda x: cv2.contourArea(x))

    blank = img.copy()  

    center = (0,0)

    for cnt in cntsSorted:
        area = cv2.contourArea(cnt)
        if 1000 < area < 1600:
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center = (cx, cy)
            cv2.drawContours(img, [cnt], -1, (255, 0, 0), 2)
            cv2.circle(img,center,2,(0,255,0),2)

    cv2.imshow("contours_image", img)
    return center

## Detection of Blue button in MicroPose

def blue_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([78, 158, 124])
    upper_blue = np.array([138, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contour, key=lambda x: cv2.contourArea(x))
    centre_B = (0, 0)
    cv2.imshow("Mask", mask)
    for cnt in cntsSorted:
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.02*perimeter,True)
        objlen = len(approx)

        if 900 < area <3000 and objlen > 7  :
            
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(image, (cX, cY), 2, (0, 255, 0), 2)

            centre_B = (cX, cY)
    return centre_B

## Execution of Micro vision code to find the Red and Blue button's coordinates

def StartMicroPose():

    rs = RealsenseCamera()
    
    for i in range(30):
        ret, bgr, depth = rs.get_frame_stream()
        image = bgr
        center_R = red_center(image)
        center_B = blue_color(image)
        if i == 60:
            break
    
    print("centre R:", center_R)
    print("center B:",center_B)
    return center_R, center_B
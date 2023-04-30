import cv2
import numpy as np
from realsense_camera import *

## Calculation of Taskboard Orientation

def overall_angle(center_R, center_m5, m5_angle, m5_wh):
    w, h = m5_wh
    rotation_angle = 0
    if w > h:
        if center_m5[0] < center_R[0] and center_m5[1] < center_R[1]:
            rotation_angle = 360 - m5_angle
        elif center_m5[0] > center_R[0] and center_m5[1] > center_R[1]:
            if m5_angle == 90:
                rotation_angle = 90
            elif m5_angle < 90:
                rotation_angle = 180 - m5_angle

    elif w < h:
        if center_R[0] < center_m5[0] and center_R[1] > center_m5[1]:
            if m5_angle <= 90:
                rotation_angle = 270- m5_angle
            
        elif center_R[0] > center_m5[0] and center_R[1] < center_m5[1]:
            # if m5_angle == 90:
            rotation_angle = 90 - m5_angle
            # elif m5_angle < 90:
            #     rotation_angle = 180 - m5_angle
        elif center_m5[0] > center_R[0] and center_m5[1] > center_R[1]:
            rotation_angle = 90 - m5_angle
    return rotation_angle

## Detection of M5 button and Red button 

def findRotationAngle(input_image):
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
    rotation_angle = 0
    center_R = (0, 0)
    center_m5 = (0, 0)
    m5_angle = 0
    m5_wh = (0, 0)

    for cnt in cntsSorted:
        area = cv2.contourArea(cnt)
    
        if 100 < area < 250:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center_R = (cx, cy)
            cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
            cv2.circle(blank, (cx,cy) , 2, (0 ,255 , 0), 3)
            cv2.drawContours(blank, [cnt], -1, (255, 0, 0), 2)
        if 1800 < area < 4000:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.intp(box)
            center_m5 = rect[0]
            m5_wh = rect[1]
            w, h = rect[1]
            m5_angle = rect[-1]
            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
            cv2.drawContours(blank, [cnt], -1, (0, 255, 0), 2)

    cv2.imshow("contours_image", blank)

    return center_R,m5_angle, center_m5, m5_wh

## Execution of Macro vision code to find the Red button coordinates

def StartMacroPose():

    rs = RealsenseCamera()

    for i in range(120):
        ret, bgr, depth = rs.get_frame_stream()
        cam = bgr
        center_R, m5_angle, center_m5, m5_wh = findRotationAngle(cam)
        rotation_angle = overall_angle(center_R, center_m5, m5_angle, m5_wh)
        if i == 120:
            break
    
    print(f"Pixel coordinates of red  button : {center_R}")
    print(f"Orientation of Taskboard : {rotation_angle}")

    return center_R
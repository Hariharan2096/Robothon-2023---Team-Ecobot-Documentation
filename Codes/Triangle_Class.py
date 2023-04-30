import cv2 as cv
import numpy as np
from realsense_camera import *

## Class to Detect Triangles for slider task


class Triangle:

    def __init__(self, image):
        self.image = image

    def blue_color(self, image):
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])
        mask = cv.inRange(hsv, lower_blue, upper_blue)

        contour, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cntsSorted = sorted(contour, key=lambda x: cv.contourArea(x))

        cv.imshow("Mask", mask)
        for cnt in cntsSorted:
            area = cv.contourArea(cnt)

            perimeter = cv.arcLength(cnt, True)

            epsilon = 0.1 * perimeter

            approx = cv.approxPolyDP(cnt, epsilon, True)

            rect = cv.minAreaRect(cnt)
            box = cv.boxPoints(rect)
            bounding = cv.boundingRect(cnt)
            box = np.intp(box)
            if area > 2700:
                rect = cv.minAreaRect(cnt)
                box = cv.boxPoints(rect)
                bounding = cv.boundingRect(cnt)
                x, y, w, h = bounding
                box = np.intp(box)
         
                if box[0][1] > box[1][1] and box[2][1] < box[3][1]:
                    y1 = box[1][1]
                    y2 = box[3][1]

                elif box[0][1] == box[1][1] and box[2][1] == box[3][1]:
                    y1 = box[0][1]
                    y2 = box[2][1]

                else:
                    y1 = box[0][1]
                    y2 = box[2][1]
                print(y1, y2)

                if box[0][0] < box[1][0] and box[2][0] < box[3][0]:
                    x1 = box[1][0]
                    x2 = box[3][0]

                elif box[0][0] == box[1][0] and box[2][0] == box[3][0]:
                    x1 = box[0][0]
                    x2 = box[2][0]

                else:
                    x1 = box[0][0]
                    x2 = box[2][0]
                print(x1, x2)
                imgCrop = image[y1:y2, x1:x2]
                cv.imshow('Cropp', imgCrop)

        return imgCrop

    def yellow_color(self, image):
        grey_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        _, thresh = cv.threshold(grey_image, 150, 255, cv.THRESH_TOZERO)
        contour, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cntsSorted = sorted(contour, key=lambda x: cv.contourArea(x))
        centre_Y = (0, 0)
        for cnt in cntsSorted:
            area = cv.contourArea(cnt)
            print("Area",area)

            perimeter = cv.arcLength(cnt, True)
            print("peri",perimeter)

            epsilon = 0.1 * perimeter

            approx = cv.approxPolyDP(cnt, epsilon, True)
            print(len(approx))

            if area > 30 and perimeter > 25:
        
                rect = cv.minAreaRect(cnt)
                print(f"Centre of Yellow Triangle:", rect[0])
 
                centre_Y = rect[0]         
                cv.drawContours(image, [approx], -1, (0, 0, 250), 2)
                cv.imshow("Yellow", image)
        return centre_Y

    def green_color(self, image):
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

        lower_green = np.array([65, 60, 60])
        upper_green = np.array([80, 255, 255])
        

        mask = cv.inRange(hsv, lower_green, upper_green)

        contour, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cntsSorted = sorted(contour, key=lambda x: cv.contourArea(x))
        cv.imshow("Mask",mask)
        centre_G = (0, 0)
        for cnt in cntsSorted:
            area = cv.contourArea(cnt)
            print("Area G",area)
            perimeter = cv.arcLength(cnt, True)

            epsilon = 0.1 * perimeter

            approx = cv.approxPolyDP(cnt, epsilon, True)
            print("Len G",len(approx))

            if 2 < len(approx) < 4 or area > 0:
                rect = cv.minAreaRect(cnt)
                print(f"Centre of Green Triangle:", rect[0])
  
                centre_G = rect[0]
    
        return centre_G

    def red_color(self, image):
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

        centre_R = (0, 0)
        for cnt in cntsSorted:
            area = cv.contourArea(cnt)

            perimeter = cv.arcLength(cnt, True)

            epsilon = 0.1 * perimeter

            approx = cv.approxPolyDP(cnt, epsilon, True)

            if len(approx) >= 3 and area > 30 and perimeter > 25:
               
                rect = cv.minAreaRect(cnt)
                print(f"Centre of Red triangle:", rect[0])              
                centre_R = rect[0]

            cv.imshow('Red', image)
        return centre_R

    def red_to_yellow(self, R, Y, w_p):
        slider_len = 37  # mm
        screen_len = 27  # mm
        slider_screen_ratio = slider_len / screen_len
        red_center = R
        yellow_center = Y
        screen_width_pixel = w_p
        dist = red_center[0] - yellow_center[0]
        screen_real_pixel_ratio = screen_width_pixel / screen_len
        slider_displacement = (dist / screen_real_pixel_ratio) * slider_screen_ratio  # mm

        print("Red To Yellow", slider_displacement)

        return slider_displacement

    def red_to_green(self, R, G, w_p):
        slider_len = 37  # mm
        screen_len = 27  # mm
        slider_screen_ratio = slider_len / screen_len
        red_center = R
        green_center = G
        screen_width_pixel = w_p
        dist = red_center[0] - green_center[0]
        screen_real_pixel_ratio = screen_width_pixel / screen_len
        slider_displacement = (dist / screen_real_pixel_ratio) * slider_screen_ratio  # mm

        print("Red To Green", slider_displacement)

        return slider_displacement

cv.waitKey(0)
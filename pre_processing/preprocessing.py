import numpy as np
import cv2

class Preprocessing:

    def __init__(self):
        self.LOWER_RED = np.array([0, 105, 155])
        self.UPPER_RED = np.array([32, 237, 255])
        self.LOWER_GRAY = np.array([100, 15, 0])
        self.UPPER_GRAY = np.array([255, 255, 255])

    def cut_out_backgound(self, image):
        mask = self.enhance_color(self.LOWER_RED, self.UPPER_RED, image)
        image_no_backgrund = cv2.bitwise_and(image, image, mask=mask)
        return mask, image#image_no_backgrund

    def enhance_color(self, lower, upper, image):
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, lower, upper)
        return mask

    def get_layer(self, image, nlayer):
        b, g, r = cv2.split(image)
        layers = [b, g, r]
        layer = None
        if nlayer >= 0 and nlayer < 3:
            layer = layers[nlayer]
        return layer

    def apply_threshold(self, layer, thresh_min, thresh_max):
        _, image_binary = cv2.threshold(layer, thresh_min, thresh_max, cv2.THRESH_BINARY)
        return image_binary

    def get_mask_brightness(self, image):
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(image_hsv)
        image_bin_v = self.apply_threshold(v, 180, 255)
        return image_bin_v

    def draw_image(self, image, type, data, color):
        #if type = 1 is an rectangle
        if(type == 1):
            [(x_min, y_min), (x_max, y_max)] = data
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
        #if type = 2 is an polygon
        elif(type == 2):
            approx = cv2.approxPolyDP(data, 0.05 * cv2.arcLength(data, True), True)
            if len(approx) == 3:
                cv2.drawContours(image, [data], 0, color, 2)
        #if type = 3 is an text
        else:
            cv2.putText(image, data,(20,20), cv2.FONT_HERSHEY_COMPLEX, 1.5, color)
        return image

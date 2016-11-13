import cv2
from pre_processing.hog_descriptor import HogDescriptor
from pre_processing.segmentation import Segmentation

class Detector:

    def __init__(self):
        self.hog = HogDescriptor()
        self.segmentation = Segmentation()
        self.model = cv2.SVM()
        self.path_train_fire_segmented_2 = "resources/training/fire/train_10.5769230769%.xml"
        self.LABEL_FIRE = 1
        self.COLOR_FIRE = (0,255,0)
        self.j = 0

    def load_train(self, path_train):
        self.model.load(path_train)

    def detect_fire_segment(self, image, load_train=True):
        mat_points, image_no_background = self.segmentation.segment(image)
        if load_train:
            path_train = self.path_train_fire_segmented_2
            self.load_train(path_train)
        detected_image = self.get_submats(mat_points, image_no_background, image, self.LABEL_FIRE, self.COLOR_FIRE)
        return detected_image

    def get_submats(self, mat_points, image_no_background, image, label, color):
        i = 0
        for (x, y, w, h) in mat_points:
            (x, w) = self.swap_points(x, w)
            (y, h) = self.swap_points(y, h)
            if (x is not None and y is not None):
                subMat = image_no_background[y:h, x:w]
                subMat = cv2.resize(subMat, (64, 64))
                [descriptors] = self.hog.get_list_hog_descriptors([subMat])
                result = self.model.predict(descriptors)
                if result == label:
                    cv2.rectangle(image, (x,y), (w,h), color,1)
                i +=1
                self.j += 1
        return image

    def swap_points(self, x1, x2):
        if x2 < x1:
            aux_x1 = x1
            x1 = x2
            x2 = aux_x1
            res = (x1, x2)
        elif x2 == x1:
            res = (None, None)
        else:
            res = (x1, x2)
        return res


if __name__ == '__main__':
    detector = Detector()

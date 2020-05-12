import os
import math
from scipy.spatial import distance
import cv2
aDATADIR = "abnormal5"
nDATADIR = "normal5"
def Average(lst):
    return sum(lst) / len(lst)
class kmeans:

    def __init__(self):
        self.normalc = 0
        self.abnormalc = 0
        ablack_pixels = []
        apath = os.path.join(aDATADIR)
        for img in os.listdir(apath):
            count = []
            image = cv2.imread(os.path.join(apath, img), 0)
            cnt = image.size - cv2.countNonZero(image)
            count.append(cnt)
            ablack_pixels.append(cnt)
            self.abnormalc = Average(ablack_pixels)
        nblack_pixels = []
        npath = os.path.join(nDATADIR)
        for img in os.listdir(npath):
            count = []
            image = cv2.imread(os.path.join(npath, img), 0)
            cnt = image.size - cv2.countNonZero(image)
            count.append(cnt)
            nblack_pixels.append(cnt)

            self.normalc = Average(nblack_pixels)
    def classify(self,image):
        image= cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        black_pixels_count = image.size - cv2.countNonZero(image)

        d = distance.euclidean(self.normalc, black_pixels_count)
        ad = distance.euclidean(self.abnormalc, black_pixels_count)
        if (d < ad):
           return 0
        else:
           return 1
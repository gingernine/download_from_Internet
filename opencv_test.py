#!/usr/bin/env python3
# coding: utf-8

import cv2
import numpy as np


class OpenCVTest(object):
    """openCV画像処理テストクラス"""

    def __init__(self, showwindow, image_file):
        self.image_file=image_file
        self.showwindow=showwindow
        cv2.namedWindow(self.showwindow)

    def show_image(self, img):
        cv2.imshow(self.showwindow, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def testshow(self, show=False):
        img=cv2.imread(self.image_file)
        if not show:
            return img
        if show:
            return self.show_image(img)

    def gray(self, show=False):
        """グレースケール化"""        
        img=self.testshow()
        gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if not show:
            return gray
        if show:
            return self.show_image(gray)

    def blurred(self):
        """平滑化フィルタ:単純平均"""
        gray=self.gray()
        blurred=cv2.blur(gray, (5,5))
        return self.show_image(blurred)
    
    def gaussianBlurred(self):
        """平滑化フィルタ:Gaussian"""
        gray=self.gray()
        gaussianBlurred=cv2.GaussianBlur(gray, (5,5), 0)
        return self.show_image(gaussianBlurred)

    def canny(self):
        """キャニーフィルタ"""
        gray=self.gray()
        thrs1=1000
        thrs2=10
        edge=cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        return self.show_image(edge)

    def binary(self):
        """二極化"""
        gray=self.gray()
        ret, binImg=cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        return self.show_image(binImg)


if __name__=='__main__':
    test=OpenCVTest('test', 'C:\\Users\\User\\Pictures\\gintama\\gintama0.jpg')
    test.testshow(show=True)







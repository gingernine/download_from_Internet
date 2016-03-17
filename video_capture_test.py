#!/usr/bin/env python3
# coding: utf-8

import cv2
import numpy as np


cap=cv2.VideoCapture('input.avi')
ret, fname=cap.read()
cv2.imwrite('first_fname.png', fname)
while(cap.isOpened()):
    ret, fname=cap.read()
    gray=cv2.cvtColor(fname, cv2.COLOR_BGR2GRAY)
    cv2.imshow('fname', gray)
    if cv2.waitKey(1) &amp 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



















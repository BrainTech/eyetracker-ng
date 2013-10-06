# -*- coding: utf-8 -*-

#    This file is part of eyetracker-ng.
#
#    eyetracker-ng is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    eyetracker-ng is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with eyetracker-ng. If not, see <http://www.gnu.org/licenses/>.

# author: Sasza Kijek
# e-mail: saszasasha@gmail.com
# University of Warsaw 2013

import cv2
from sys import argv
import numpy as np

cap = cv2.VideoCapture(int(argv[1]))

def nothing(x):
    pass

def glint(image):
    where = cv2.goodFeaturesToTrack(image, 2, 0.0001, 30)
    if where != None:
        where = np.array([where[i][0] for i in xrange(where.shape[0])])
    return where

def pupil(image):
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, 1, 100, 
                               param1=50, param2=10, minRadius=10, maxRadius=100)
    if circles != None:
        circles = np.uint16(np.around(circles))
        return circles[0] #lista x-ów,y-ów i promieni

cv2.namedWindow('b&w1')
cv2.namedWindow('b&w2')

cv2.createTrackbar('maxValue', 'b&w1', 0, 255, nothing)
cv2.createTrackbar('thresh_type', 'b&w1', 0, 3, nothing)
cv2.createTrackbar('thresh', 'b&w1', 0, 255, nothing)

cv2.createTrackbar('maxValue', 'b&w2', 0, 255, nothing)
cv2.createTrackbar('blockSize', 'b&w2', 1, 107, nothing)
cv2.createTrackbar('C', 'b&w2', 0, 255, nothing)

thresholds = [cv2.THRESH_OTSU, cv2.THRESH_BINARY, 
              cv2.THRESH_TOZERO, cv2.THRESH_TRUNC]

while(1):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    max1 = cv2.getTrackbarPos('maxValue', 'b&w1')
    thresh_index = cv2.getTrackbarPos('thresh_type', 'b&w1')
    thresh = cv2.getTrackbarPos('thresh', 'b&w1')

    max2 = cv2.getTrackbarPos('maxValue', 'b&w2')
    block2 = 2*cv2.getTrackbarPos('blockSize', 'b&w2')+1
    c2 = cv2.getTrackbarPos('C', 'b&w2')

    ret, black1 = cv2.threshold(gray, thresh, max1, thresholds[thresh_index])

    black2 = cv2.adaptiveThreshold(gray, max2, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, block2, c2)


    for i in (gray, black1, black2):
        where_pupil = pupil(i)
        where_glint = glint(i)

        if where_glint != None:
            for cor in where_glint:
                cv2.circle(i, tuple(cor), 10, (255, 0, 0), 3)
        if where_pupil != None:
            for cor in where_pupil:
                cv2.circle(i, tuple(cor[:2]), cor[2], (0, 0, 255), 3)
            


    cv2.imshow('true', frame)
    cv2.imshow('gray', gray)
    cv2.imshow('b&w1', black1)
    cv2.imshow('b&w2', black2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

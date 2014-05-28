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

# authors: Sasza Kijek, Karol Augustin, Tomasz Spustek
# e-mail: saszasasha@gmail.com
# University of Warsaw 2013

import cv2
import numpy as np

def eye(image):
    #should return a mask
    pass

def blink():
    #should return bin
    pass

def findBestGlints(shape , where_glint , where_pupil , algorithm = 'pupil'):
    try:
        if len(where_glint) < 3:
            return where_glint
        elif len(where_glint) > 2 and algorithm == 'centered':
            result = np.zeros(len(where_glint))
            center_x = shape[1] / 2.
            center_y = shape[0] / 2.
            
            for ind , value in enumerate(where_glint):
                result[ind] = np.sqrt( (value[0] - center_x)**2 + (value[1] - center_y)**2 )
        
            ind_1 = np.argmin(result)
            result[ind_1] = shape[1]
            ind_2 = np.argmin(result)
            
            return np.array( [where_glint[ind_1] , where_glint[ind_2]] )
                        
        elif len(where_glint) > 2 and algorithm == 'closest':
            result = []
            for ind_1 , value_1 in enumerate(where_glint):
                for ind_2 in range(ind_1+1 , len(where_glint)):
                    value_2 = where_glint[ind_2]
                    
                    result.append( np.sqrt( (value_1[0] - value_2[0])**2 + (value_1[1] - value_2[1])**2 ) )
            
            result.sort()
            return np.array(result[0] , result[1])
            
        elif len(where_glint) > 2 and algorithm == 'pupil':
            if where_pupil == None:
                return where_glint
            else:
                result = np.zeros(len(where_glint))
                
                for ind , value in enumerate(where_glint):
                    result[ind] = np.sqrt( (value[0] - where_pupil[0][0])**2 + (value[1] - where_pupil[0][1])**2 )
                
                ind_1 = np.argmin(result)
                result[ind_1] = shape[1]
                ind_2 = np.argmin(result)
                
                return np.array( [where_glint[ind_1] , where_glint[ind_2]] )
                
    except TypeError:       # means that there is less than 1 glint detected (possibly 0)
        return where_glint
            
def glint(image, maxCorners=2, quality=0.0001, minDist=20, mask=None,
          blockSize=3):
    ''' Function detects glint on the retina.

    Based on the funccv2.goodFeaturesToTrack.
    For more info on parameters check the docs for opencv and
    goofFeaturesToTrack.

    Parameters
    -----------
    image : np.array
        image of the eye where the glints are supposed to be detected
    maxCorners : int
        how many glints should it detect, default is 2
    quality : 
        minimal accepted quality of image corners
    minDist :
        minimum distance between the detected glints, default is 20
    mask :
        area of the image that should be used for glint detection
        default is None so it looks through the whole picture
    blockSize :
        size of an average block for computing a derivative
    covariation :
        matrix over each pixel neighborhood

    Returns
    --------
    where : array
        ccoordinates(a list [x, y]) for found glints
    '''
    where = cv2.goodFeaturesToTrack(image, maxCorners=maxCorners,
                                    qualityLevel=quality, minDistance=minDist,
                                    mask=mask, blockSize=blockSize)
    if where != None:
        where = np.array([where[i][0] for i in xrange(where.shape[0])])
    return where

def pupil(image, dp=1, minDist=100, param1=50, param2=10, minRadius=20,
          maxRadius=70):
    ''' Function detects pupil on the image of an eye.
    
    Based on the funccv2.HoughCircles. for more info on
    parameters check the docs for opencv and HoughCircles.

    Parameters
    -----------
    image - np.array
        image of the eye where the pupil is supposed to be detected
    dp : int
        inverse ratio of the accumulator resolution to the image's,
    minDist : int
        minimum distance between found circles
    param1 : int
        higher threshold for the Canny edge detector
    param2 : int
        accumulator threshold for the circles centers, smaller it is,
        more false positives
    minRadius : int
        minimal radius of the detected circle
    maxRadius : int
        maximal radius of the detected circle

    Returns
    --------
    where : array
        coordinates and the radius of the circle (a list
        [x, y, z]) for found pupils
    '''
    circles = cv2.HoughCircles(image, cv2.cv.CV_HOUGH_GRADIENT, dp, minDist,
                               param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)
    if circles != None:
        circles = np.uint16(np.around(circles))[0]
        circles = removeArtificialCircles(circles)
    return circles

def removeArtificialCircles(circles):
    new_circles = []
    for circle in circles:
        if circle[0] <  320 * 0.35 or circle[0] >  320 * 0.65:
            pass
        else:
            if circle[1] <  240 * 0.35 or circle[1] >  240 * 0.65:
                pass
            else:
                new_circles.append(circle)
    
    if not new_circles:
        return None
    else:
        new_circles = np.array(new_circles)
        return new_circles

if __name__ == '__main__':
    from processing import threshold, gray2bgr, bgr2gray, mark

    im_gray = cv2.imread('../../pictures/eyeIR.png', 0)

    where_glint = glint(im_gray)

    im_bw = threshold(im_gray, thresh_v=73)
    where_pupil = pupil(im_bw)

    im = gray2bgr(im_gray)

    mark(im, where_glint)

    mark(im, where_pupil, color='blue')

    while(1):
        cv2.imshow('Pupil(blue) and glint(red) detection, exit with "q" or "esc"', im)
        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):
            break

    cv2.destroyAllWindows()

#!/usr/bin/env python
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
# e-mails: saszasasha@gmail.com karol@augustin.pl tomasz@spustek.pl
# University of Warsaw 2013

import cv2
import numpy as np

thresholds = {'otsu' : cv2.THRESH_OTSU, 'bin' : cv2.THRESH_BINARY,
              'bin_inv' : cv2.THRESH_BINARY_INV,
              'zero' : cv2.THRESH_TOZERO, 'zero_inv' : cv2.THRESH_TOZERO_INV,
              'trunc' : cv2.THRESH_TRUNC}

adaptiveMethods = {'gaussian' : cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                   'mean' : cv2.ADAPTIVE_THRESH_MEAN_C}

colors = {'blue' : (255, 0, 0), 'green' : (0, 255, 0), 'red' : (0, 0, 255)}

def bgr2gray(imageBGR):
    ''' Convert color image(BGR) to gray image.

    Parameters
    -----------
    image : np.array
        2d 24-bit array depicting an image in three-channel color:
        Blue,Green,Red

    Returns
    -----------
    image : np.array
        2d 8-bit array depicting a given image converted to gray scale.
    '''
    return cv2.cvtColor(imageBGR, cv2.COLOR_BGR2GRAY)

def gray2bgr(imageGRAY):
    ''' Convert gray image to color image(BGR).

    Parameters
    -----------
    image : np.array
        2d 8-bit array depicting an image in one-channel color (greyscale)

    Returns
    -----------
    image : np.array
        2d 24-bit array depicting a given image converted to three-channel
        color scale: Blue,Green,Red.
    '''
    return cv2.cvtColor(imageGRAY, cv2.COLOR_GRAY2BGR)

def threshold(image, thresh_v=30, max_v=255, thresh_type='trunc'):  #zero_inv
    ''' Threshold the image.

    For corresponding threshold types description see docs.opencv.org:
    {'otsu' : cv2.THRESH_OTSU,
    'bin' : cv2.THRESH_BINARY, 'bin_inv' : cv2.THRESH_BINARY_INV,
    'zero' : cv2.THRESH_TOZERO, 'zero_inv' : cv2.THRESH_TOZERO_INV,
    'trunc' : cv2.THRESH_TRUNC}

    Parameters
    -----------
    image : np.array
        2d 8-bit array depicting an image in one-channel color(ex. grayscale)
    thresh_v : int
        value of threshold cut-off
    max_v : int
        maximal value when thresholding, relevant only if thresh_type is 'bin' or 'bin_inv'
    thresh_type : string
        type of thresholding, possible 'otsu', 'bin', 'bin_inv', 'zero', 'zero_inv', 'trunc'

    Returns
    -----------
    thresholded_image : np.array
        given image after aplication of a given threshold.
    '''
    thresh_v = int(thresh_v)
    max_v = int(max_v)

    ret, thresholded_image = cv2.threshold(image, thresh_v, max_v,
                                           thresholds[thresh_type])
    return thresholded_image

def imageFlipMirror(im, mirrored,flipped):
    ''' Flip and/or mirror the given image.

    Parameters
    -----------
    im : np.array
        2D array depicting an image as an numpy array
    mirrored : np.array
        self explanatory boolean parameter (left - right)
    fliped np.array
        self explanatory boolean parameter (top - bottom)

    Returns
    -----------
    im : np.array
        image array processed accordingly.
    '''

    if mirrored == 1 and flipped == 0:
        im = cv2.flip(im, 1)
    elif mirrored == 0 and flipped == 1:
        im = cv2.flip(im, 0)
    elif mirrored == 1 and flipped == 1:
        im = cv2.flip(im, -1)
    return im

def adaptiveThreshold(image, max_v=255, adaptiveMethod='gaussian',
                      thresh_type='bin', blockSize=33,
                      subtConstant=10):
    ''' Threshold the image using adaptive methods.

    For corresponding adaptive methods see docs.opencv.org:
    {'gaussian' : cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    'mean' : cv2.ADAPTIVE_THRESH_MEAN_C}

    Parameters
    -----------
    image : np.array
        2D array depicting an image in one-scale color(ex. grayscale)
    max_v : int
        maximal value to be used in threshold
    adaptiveMethod : string
        method used for thresholding, possible 'gaussian' or 'mean'
    thresh_type : string
        prethresholding, possible thresholds 'bin'(binary) or 'bin_inv'(inversed binary)
    blockSize : int
        Size of a pixel neighborhood that is used to calculate a threshold value,
        the size must be an odd number.
    subtConstant : int
        a constant that will be subtracted from mean or weighted mean 
        (depending on adaptiveMethod chosen)

    Returns
    -----------
    thresholded : np.array
        image array processed accordingly.
    '''

    max_v = int(max_v)
    blockSize = int(blockSize)
    subtConstant = int(subtConstant)

    if thresh_type is not 'bin' and thresh_type is not 'bin_inv':
        raise AttributeError('thresh_type may be "bin" or "bin_inv" here.')

    thresholded = cv2.adaptiveThreshold(image, max_v,
                                  adaptiveMethods[adaptiveMethod],
                                  thresholds[thresh_type], blockSize,
                                  subtConstant)
    return thresholded

def mark(image, where, radius=10, color='red', thickness=3):
    ''' Mark object with a circle.

    Parameters
    -----------
    image : np.array
        3d array depicting the original image that is to be marked,
        needs to be in three scale color
    where : np.array
        array of sets of coordinates (x, y or x, y, radius) of the object
    radius : int
        set same radius for all objects, if a set of coordinates has
        a third value this will be overruled
    color : string
        color of circles marking the object, possible: 'blue', 'green' or 'red'
    thickness : int
        thickness of the circle

    Returns
    -----------
    true : True
    '''
    if where != None:
        if len(where.shape) == 1:
            y = where[1]
            x = where[0]
            cv2.circle(image, (x, y), radius, colors[color], thickness)
        else:
            for coordinates in where:
                y = coordinates[1]
                x = coordinates[0]
                if len(coordinates) == 3:
                    radius = coordinates[2]
                cv2.circle(image, (x, y), radius, colors[color], thickness)

    return True

def find_purkinje(purkinje1, purkinje2):
    ''' Find virtual purkinje image in a two IR LED setting.

    Simple finding of the middle between two points.

    Parameters
    -----------
    purkinje1 : tuple of (int, int)
        the coordinates of first purkinje image
    purkinje2 : tuple of (int, int)
        the coordinates of second purkinje image

    Returns
    --------
    middle : tuple of (int, int)
        which are the coordinates of the middle between purkinje1 and purkinje2.
    '''
    purkinje = tuple(sum(coord)/2 for coord in zip(purkinje1, purkinje2))
    return purkinje

def runningAverage(image, average, alpha):
    ''' Calculates running average of given pictures stream.

    Using cv2.accumulateWeighted.

    Parameters
    -----------
    image : np.array
        new image to be averaged along with past image stream,
    average : np.array
        past averaged image,
    alpha : int
        control parameter of the running average, it describes
        how fast previous images would be forgotten, 1 - no average,
        0 - never forget anything.

    Returns
    --------
    image : np.array
        averaged image as numpy array.
    '''
    average = np.float32(average)
    cv2.accumulateWeighted(image, average, alpha)
    #print 'Alpha value is {}.'.format(alpha)
    image = cv2.convertScaleAbs(average)

    return image

def averageGlints(where_glint , glints_stack):
    return where_glint , glints_stack

def averagePupils(where_pupil , pupils_stack):
    return where_pupil
    try:
        if where_pupil.shape[0] == 1:
            #print '!!!'
            #print pupils_stack.shape
            #print where_pupil.shape
            pupils_stack = np.vstack((pupils_stack , where_pupil))[1:,:]
            #print pupils_stack
            
            where_pupil[0,0] = pupils_stack[:,0].mean()
            where_pupil[0,1] = pupils_stack[:,1].mean()
            where_pupil[0,2] = pupils_stack[:,2].mean()
        else:
            pass
            
    except AttributeError:      # it means no pupil was found
        pass
    
    return where_pupil , pupils_stack

if __name__ == '__main__':
    from numpy import array

    im = cv2.imread('../../pictures/eyeIR.png', -1)

    marked = im.copy()

    im_fliped = imageFlipMirror(im,0,1)

    im_gray = bgr2gray(im)

    im_back = gray2bgr(im_gray)

    #for depicting that there are 3 color channels
    im_back[0:10, :] = colors['blue']
    im_back[-10:-1, :] = colors['green']
    im_back[:, 0:10] = colors['red']
    im_back[:, -10:-1] = colors['red']

    im_thresh = threshold(im_gray)

    im_thresh_adapt = adaptiveThreshold(im_gray)

    mark(marked, array([[marked.shape[1]/2, marked.shape[0]/2]]), radius=30)

    pics = {'original image' : im, 'one-channel gray image' : im_gray,
            'converted back to 3 channel' : im_back,
            'thresholded' : im_thresh,
            'thresholded adaptively' : im_thresh_adapt,
            'Marked center of image' : marked,
            'Fliped image' : im_fliped}

    while(1):
        [cv2.imshow(descp, pic) for descp, pic in pics.iteritems()]

        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):
            break

    cv2.destroyAllWindows()

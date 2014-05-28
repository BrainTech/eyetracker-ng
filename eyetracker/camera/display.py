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

from cv2 import namedWindow, CV_WINDOW_AUTOSIZE, imshow, waitKey

from ..analysis.detect import pupil, glint, findBestGlints
from ..analysis.processing import threshold, mark, gray2bgr, bgr2gray, averageGlints , averagePupils

def drawGlint(image , where_pupil , numberOfGlints , glints_stack):
    ''' Find and draw glint on image.

    Function takes an image, converts it to grayscale if it is not,
    detects glint and draws it on a new image.

    Parameters
    -----------
    image : np.array
        image where the glint is to be detected
    where_pupil : np.array
        coordinates of pupil on a given image
    numberOfGlints : int
        number of points to find on an image

    Returns
    --------
    color image : np.array
        returns a numpy array in a bgr scale with the glint
        marked in blue
    '''
    if len(image.shape) == 3:
        image = bgr2gray(image)
        
    where_glint = glint(image , numberOfGlints)
    
    where_glint = findBestGlints(image.shape , where_glint , where_pupil)
    
    
    where_glint , glints_stack = averageGlints(where_glint , glints_stack)
    
    
    bgr = gray2bgr(image)
    mark(bgr, where_glint)
    return bgr, where_glint , glints_stack

def drawPupil(image, thres , pupils_stack , numberOfPupils):
    ''' Find and draw pupil on image.

    Function takes an image, applies 'trunc' threshold(cv2.THRESH_TRUNC),
    detects pupil and draws it on a new image.

    Parameters
    -----------
    image : np.array
        image where the pupil is to be detected
    thres : int
        value of the threshold

    Returns
    --------
    cimage : np.array
        returns a numpy array in a bgr scale with the pupil
        marked in red
    '''
    if len(image.shape) == 3:
        image = bgr2gray(image)
    thresholded = threshold(image, thresh_v=thres)
    where_pupil = pupil(thresholded)
    
    where_pupil , pupils_stack = averagePupils(where_pupil , pupils_stack)
    
    bgr = gray2bgr(thresholded)
    mark(bgr, where_pupil, color='blue')
    return bgr, where_pupil , pupils_stack

def displayImage(image, where='new'):
    ''' Display image in new or existing window.

    Function displays the image in a new window or in the pointed window.
    Returns the displayed image as a numpy array.

    Parameters
    -----------
    image : np.array
        numpy array being an image to be displayed
    where : string
        name of the window as string in which the image is to be
        displayed, not providing the name will create a new one

    Returns
    -----------
    key: int
        number representation of the key that was pressed during
        the image display
    '''
    if where == 'new':
        namedWindow('new', flags=CV_WINDOW_AUTOSIZE)
    imshow(where, image)
    key = waitKey(1) & 0xFF
    return key

if __name__ == '__main__':
    from cv2 import imread, waitKey

    im = imread('../../pictures/eyeIR.png', 0)

    pupil = drawPupil(im, 35)
    glint = drawGlint(im)

    displayImage(pupil, where='Pupil detection.')
    displayImage(glint, where='Glint detection.')
    waitKey(0)

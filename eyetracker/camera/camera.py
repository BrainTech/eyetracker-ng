#!/usr/bin/python
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

from cv2 import VideoCapture
from glob import iglob
from platform import system

def lookForCameras():
    ''' Function looks for cameras available cameras.

    Returns
    --------
    dic : {Camera_i , index}
        where i is the 1,2,3 etc. and index
        is an int corresponding to the camera that should be passed on
        to cv2.VideoCapture or to class Camera from eyetracker.camera.camera.
    '''
    
    if system() == 'Windows':
        listOfCameras = {}
        listOfCameras['Camera_1'] = 0
        listOfCameras['Camera_2'] = 1
        # FUU!
    else:
        listOfCameras = {''.join(['Camera_', str(i+1)]) : int(i)
                     for i, cam in enumerate(iglob('/dev/video*'))}
    return listOfCameras

class Camera(object):
    ''' Communicate with the camera.

    Class governing the communication with the camera.

    Parameters
    -----------
    camera : int
        the index of the camera, best taken from func lookForCameras,
        from eyetracker.camera.capture
    dic : dic{propID  value}
        to check corresponding propIDs check
        opencv documentation under the term VideoCapture. 
        They will be set in the moment of object creation.

    Defines
    --------
    self.camera : index of the camera
    self.cap : capturing object
    self.frame : returns a frame from camera
    self.close : closes cap
    self.reOpen : reopens cap
    '''
    def __init__(self, camera, dic=None):
        self.camera = int(camera)
        self.cap = VideoCapture(self.camera)
        if dic:
            for propID, value in dic.iteritems():
                self.cap.set(propID, value)
        first_frame = self.frame()

    def frame(self):
        ''' Read frame from camera.

        Returns
        --------
        frame : np.array
            frame from camera
        '''
        if self.cap.isOpened:
            return self.cap.read()[1]
        else:
            print 'Cap is not opened.'
            return None

    def set(self, **kwargs):
        ''' Set camera parameters.

        Parameters
        -----------
        kwargs : {propID : value}
        '''
        for propID, value in kwargs.iteritems():
            self.cap.set(propID, value)

    def close(self):
        ''' Closes cap, you can reopen it with self.reOpen.
        '''
        self.cap.release()

    def reOpen(self, cameraIndex):
        ''' Reopens cap.
        '''
        self.cap.open(self.camera)
        first_frame = self.frame()

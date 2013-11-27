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

from itertools import izip
from PyQt4 import QtCore, QtGui

from ..analysis.processing import imageFlipMirror, runningAverage

from ..camera.display import drawPupil, drawGlint
from ..camera.capture import lookForCameras
from ..camera.camera import Camera

from .graphical import Ui_StartingWindow

########################################################################

class MyForm(QtGui.QMainWindow):
    '''
    Class governing the functional part of the default graphical user interface.

    Parameters:
    -----------
    No parameters needed.

    Defines:
    --------
    self.cameras - list containing all camera devices connected to the computer,
    self.algorithms - list of all implemented algorithms for eyetracker programm,
    self.resolutions - list of all possible image resolutions for eyetracer to operate on,
    self.w - selected width of an image to start an eyetracker,
    self.h - selected height of an image to start an eyetracker,
    self.selectedCamera - selected camera name as chosen by the user (default is a name of the first avalaible device),
    self.mirrored - boolean variable wether to mirror an image,
    self.flipped - boolean variable wether to flip an image,
    self.sampling - sampling rate of a camera (default 30 Hz),
    self.timer_on - flag showing wether timer is ticking or not,
    
    self.config - to be written,
    self.configFileName - to be written,
    
    self.alpha - control parameter of the running average, it describes
    how fast previous images would be forgotten, 1 - no average,
    0 - never forget anything.
    
    self.ui - class encapsulating graphical part of an interface, as described
    in eyetracker/gui/graphical.py file,
    
    self.camera - class encapsulating a camera device as described in
    eyetracker/camera/camera.py.
    
    Returns:
    --------
    Class does not return anything.
    '''
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)
        
        ############################# PARAMETERS INITIALIZATION
        self.cameras = lookForCameras()
        for i in self.cameras.iterkeys():
            self.ui.cmb_setCamera.addItem(i)
        
        self.algorithms = ['NESW']
        for algorithm in self.algorithms:
            self.ui.cmb_setAlgorithm.addItem(algorithm)
        
        self.resolutions_w = [160,320,640,1280]
        self.resolutions_h = [120,240,480,720]
        for w, h in izip(self.resolutions_w, self.resolutions_h):
            self.ui.cmb_setResolution.addItem(''.join([str(w), 'x', str(h)]))
            
        self.ui.cmb_setResolution.setCurrentIndex(1)
        self.w = 320
        self.h = 240
        self.mirrored = 0
        self.flipped = 0
        self.sampling = 30.0
        self.alpha = 0.1
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())
        self.configFileName = '.config/eyetracker-ng/configFile.txt'

        try:
            self.camera  = Camera(self.cameras['Camera_1'], {3 : self.w, 4 : self.h})
            #self.average = float32(self.camera.frame())
        except KeyError:
            print 'No camera device detected.'
        
        self.config = []
        try:
            with open(self.configFileName , 'r') as configFile:
                for line in configFile:
                    tmp = line.split()
                    self.config.append(tmp[1])
        except IOError:
            pass
        
        
        
        
        self.ui.lbl_pupil.setText(str(self.ui.hsb_pupil.value()))
        self.ui.lbl_glint.setText(str(self.ui.hsb_glint.value()))
        
        self.ui.timer.start(1000/self.sampling, self)
        self.timer_on = False # it starts above, but timer_on says if it already ticked at least once.
        

        ################################### EVENTS BINDINGS
        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.cmb_setAlgorithm.currentIndexChanged.connect(self.algorithmChange)
        #self.ui.btn_start.clicked.connect(self.startEyetracker)
        #self.ui.btn_settings.clicked.connect(self.startAdvancedSettings)
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.hsb_pupil.valueChanged[int].connect(self.hsbPupil_Change)
        self.ui.hsb_glint.valueChanged[int].connect(self.hsbGlint_Change)

########################################### CLOCK TICKS
    def timerEvent(self, event):
        '''
        Function controlling the main flow of the programm. It fires periodically
        (sampling rate), grabs frames from a camera, starts image processing
        and displays changes in the gui.
        
        Parameters:
        -----------
        event - standard event handler as described in QT4 documentation.
        
        Returns:
        --------
        Function does not return anything.
        '''
        im = self.camera.frame()
        
        im = runningAverage(im , im , self.alpha)
        
        im = imageFlipMirror(im, self.mirrored, self.flipped)

        self.pupilUpdate(im)
        self.glintUpdate(im)
        
        if self.timer_on == False:
            self.timer_on = True
        
        self.update()

############################## ALGORITHM CHANGING METHOD
    def algorithmChange(self):
        '''
        Function changing algorithm for eyetracker. Since there is only one
        possible algorithm for now, this function does nothing and is never
        used.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.    
        '''
        
        pass
################################ CAMERA CHANGING METHOD
    def cameraChange(self):
        '''
        Function changing camera between avalaible devices.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.            
        '''
        
        self.ui.timer.stop()
        self.camera.close()
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())
        self.camera = Camera(self.cameras[self.selectedCamera], 
                             {3 : 320, 4 : 240})
        self.ui.timer.start(100, self)

######################### MIRROR METHON
    def imageMirror(self):
        '''
        Function sets a variable telling the gui to mirror incomming frames from a camera.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        if self.mirrored == 0:
            self.mirrored = 1
        else:
            self.mirrored = 0

####################### FLIP METHOD
    def imageFlip(self):
        '''
        Function sets a variable telling the gui to flip incomming frames from a camera.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''        
        
        if self.flipped == 0:
            self.flipped = 1
        else:
            self.flipped = 0

######################### RESOLUTION CHANGING METHOD
    def resolutionChange(self):
        '''
        Function sets a chosen resolution of a camera. It does not change
        an image displayed in the gui, but sets variable for eyetracker programm.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        index  = self.ui.cmb_setResolution.currentIndex()
        self.h = self.resolutions_h[index]
        self.w = self.resolutions_w[index]
        
######### CHANGING PARAMETERS ACCORDING TO SCROLLBARS
    def hsbPupil_Change(self, value):
        '''
        Function sets a text in a gui according to the possition of a slider.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        self.ui.lbl_pupil.setText(str(value))

    def hsbGlint_Change(self, value):
        '''
        Function sets a text in a gui according to the possition of a slider.
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        self.ui.lbl_glint.setText(str(value))

############## UPDATE OBRAZU
    def pupilUpdate(self, image):
        '''

        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        pupilThreshold = self.ui.hsb_pupil.value()
        self.pupil = drawPupil(image, pupilThreshold)
            
    def glintUpdate(self, image):
        '''
        
        Parameters:
        -----------
        No parameters needed.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        glintThreshold = self.ui.hsb_glint.value()
        self.glint = drawGlint(image)#, glintThreshold

##########################################################
    def paintEvent(self, event):
        '''
        
        Parameters:
        -----------
        event - standard event handler as described in QT4 documentation.
        
        Returns:
        --------
        Function does not return anything.          
        '''
        
        painter = QtGui.QPainter(self)
        
        if self.timer_on:
            result_pupil = QtGui.QImage(self.pupil, 320, 240, QtGui.QImage.Format_RGB888)#.rgbSwapped()
            result_glint = QtGui.QImage(self.glint, 320, 240, QtGui.QImage.Format_RGB888)
        
            painter.drawImage(QtCore.QPoint(5, 35), result_pupil)
            painter.drawImage(QtCore.QPoint(5, 300), result_glint)

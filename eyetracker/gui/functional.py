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



###################################################################################################################################################

from ..analysis.processing import imageFlipMirror, runningAverage
from ..camera.display import drawPupil, drawGlint
from ..camera.camera import lookForCameras
from ..camera.camera import Camera
from eyetracker.analysis.processing import gray2bgr, bgr2gray, mark, threshold, thresholds
from .graphical import Ui_StartingWindow, Ui_CursorCalibrationWindow, Ui_NeswCalibrationWindow, Ui_NeswSpellerWindow

###################################################################################################################################################

from itertools import izip
from PyQt4 import QtCore, QtGui
import numpy as np
import os
from scipy.optimize import curve_fit
import subprocess
from functools import partial
from platform import system

###################################################################################################################################################

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

###################################################################################################################################################


def f_for_fitting((x,y) , a , b , c , d , e , f):
    return a*x**2 + b*x + c*y**2 + d*y + e*x*y + f



class MyForm(QtGui.QMainWindow):
    ''' Functional part of GUI interface.

    Class governing the functional part of the default graphical user interface.

    Defines
    -------
    self.cameras : list
        all camera devices connected to the computer,
    self.algorithms : list
        all implemented algorithms for eyetracker programm,
    self.resolutions : list
        all possible image resolutions for eyetracer to operate on,
    self.w : int
        selected width of an image to start an eyetracker,
    self.h : int
        selected height of an image to start an eyetracker,
    self.selectedCamera : string
        selected camera name as chosen by the user (default is a name of the first avalaible device),
    self.timer_on : boolean
        flag showing wether timer is ticking or not,
    self.config : path
        dictionary with all configuration variables,
    self.configFileName : path
        path to the configuration file,
    self.ui : class
        encapsulating graphical part of an interface, as described
        in eyetracker/gui/graphical.py file,
    self.camera : class
        encapsulating a camera device as described in
        eyetracker/camera/camera.py.
    '''

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)
        self.defaults                                = {}
        self.defaults['Mirrored']                    = 0
        self.defaults['Fliped']                      = 0
        self.defaults['ResolutionIndex']             = 2
        self.defaults['PupilBar']                    = 0
        self.defaults['NumberOfGlints']              = 2
        self.defaults['UseKalman']                   = 0
        self.defaults['Sampling']                    = 30.0
        self.defaults['ApplicationAlgorithmIndex']   = 0
        self.defaults['CalibrationAlgorithmIndex']   = 0
        self.defaults['CursorApplicationSmoothness'] = 0
        self.defaults['CalibrationSpeed']            = 10
        self.defaults['Averaging']                   = 5
        self.defaults['NeswThreshold']               = 3
        self.defaults['NeswQueueLength']             = 30
        self.defaults['NeswDeadTime']                = 60

        self.initializeFlags()
        
        self.cameras = lookForCameras()
        for i in self.cameras.iterkeys():
            self.ui.cmb_setCamera.addItem(i)
            
        self.calibrationAlgorithms = {}
        self.calibrationAlgorithms['No calibration']     = self.calibrationModule_raw
        self.calibrationAlgorithms['Cursor calibration'] = self.calibrationModule_cursor
        self.calibrationAlgorithms['NESW calibration']   = self.calibrationModule_nesw
        for algorithm in self.calibrationAlgorithms.keys():
            self.ui.cmb_setCalibrationAlgorithm.addItem(algorithm)
                    
        self.applicationAlgorithms = {}
        self.applicationAlgorithms['Raw output']   = self.module_raw
        self.applicationAlgorithms['Speller']      = self.module_speller
        #self.applicationAlgorithms['Speller']  = self.module_after_cal        
        for algorithm in self.applicationAlgorithms.keys():
            self.ui.cmb_setApplicationAlgorithm.addItem(algorithm)
            
        self.resolutions = [(160,120),(320,240),(640,480),(1280,720)]
        for w,h in self.resolutions:
            self.ui.cmb_setResolution.addItem(''.join([str(w), 'x', str(h)]))

        self.setVariablesState(2)
                    
        self.loadSettings()
        
        self.setVariablesState(0)
        
        self.setWidgetsState()

        try:
            self.camera  = Camera(self.cameras['Camera_1'], {3 : self.w, 4 : self.h})
        except KeyError:
            print 'No camera device detected.'

        self.ui.timer.start(1000/self.config['Sampling'], self)
        self.timer_on = False

        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.cmb_setApplicationAlgorithm.currentIndexChanged.connect(self.applicationAlgorithmChange)
        self.ui.cmb_setCalibrationAlgorithm.currentIndexChanged.connect(self.calibrationAlgorithmChange)
        
        self.ui.btn_start.clicked.connect(self.startButtonClicked)
        self.ui.btn_clear.clicked.connect(self.clearSettings)
        self.ui.btn_save.clicked.connect(self.saveSettings)
        
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.chb_useKalmanFiltration.stateChanged.connect(self.swichKalman)
        
        self.ui.hsb_pupil.valueChanged[int].connect(self.hsbPupil_Change)
        self.ui.hsb_glint.valueChanged[int].connect(self.hsbGlint_Change)
        
        self.ui.hsb_averaging.valueChanged[int].connect(self.hsbAveraging_Change)
        self.ui.hsb_calibrationSpeed.valueChanged[int].connect(self.hsbCalibrationSpeed_Change)
        self.ui.hsb_applicationSmoothness.valueChanged[int].connect(self.hsbApplicationSmoothness_Change)
        
        self.ui.hsb_neswThreshold.valueChanged[int].connect(self.hsbNeswThreshold_Change)
        self.ui.hsb_neswQueueLength.valueChanged[int].connect(self.hsbNeswQueueLength_Change)
        self.ui.hsb_neswDeadTime.valueChanged[int].connect(self.hsbNeswDeadTime_Change)



##################################################################################
##################################################################################
##################################################################################
### TIMER FIRING ###
##################################################################################
    def timerEvent(self, event):
        ''' Function controlling the main flow of this gui.

        Function fires periodically (sampling rate),
        grabs frames from a camera, starts image processing
        and displays changes in the gui.

        Parameters
        -----------
        event : object
            standard event handler as described in QT4 documentation.
       '''
        im = self.camera.frame()
        self.im = imageFlipMirror(im, self.config['Mirrored'], self.config['Fliped'])

        if self.timer_on == False:
            self.timer_on = True

        self.pupilUpdate(self.im)
        self.glintUpdate(self.im)
        
        self.runEyetracker()
        
        self.update()



##################################################################################
##################################################################################
##################################################################################
### STATE SETTING: ###
##################################################################################

    def setVariablesState(self , flag):
        
        if flag == 2:
            if system() == 'Windows':
                self.configFileName = os.path.expanduser("~") + '/_config/eyetracker-ng/configFile.txt'
            else:
                self.configFileName = os.path.expanduser("~") + '/.config/eyetracker-ng/configFile.txt'             
        else:
            self.pupilsQueueDepth = self.config['Averaging']
            self.pupilsQueue = np.zeros((self.pupilsQueueDepth,2))     
            
            self.glints_stack = np.zeros([self.pupilsQueueDepth,3])
            self.pupils_stack = np.zeros([self.pupilsQueueDepth,3])
            
            self.lastKnownPupilParameters = [self.ui.trueScreen.width() / 2. , self.ui.trueScreen.height() / 2.]
            self.last_screen_x = 0
            self.last_screen_y = 0
        
            if flag == 0:
                # might be usefull
                #self.pupilsFromCalibration = []
                #self.meanPupilRadius       = 0           
                
                # Application smoothing
                self.screen_x_list = []
                self.screen_y_list = []
                
                #self.mean_x = 0
                #self.mean_y = 0
    
    
                # for cursor calibration
                self.circlePositionX = []
                self.circlePositionY = []    
                self.eyePositionX    = []
                self.eyePositionY    = []
                
                # for nesw calibration
                self.rectanglePositionX = []
                self.rectanglePositionY = []
                # nesw uĹĽywa rĂłwnieĹĽ self.eyePositionX, self.eyePositionY 
                
    
                # well known variables
                self.w = 640
                self.h = 480
                self.selectedCamera = str(self.ui.cmb_setCamera.currentText())

        
    def initializeFlags(self):
        # czy ktoĹ› wcisnÄ…Ĺ‚ start
        self.startFlag              = 0
        
        # flagi zwiÄ…zane z kalibracjÄ… (cursor i nesw)
        self.afterCalibrationFlag   = 0
        self.calibrationStartedFlag = 0
        self.calibrationEndedFlag   = 0
        
        # flagi zwiÄ…zane ze spellerem (cursor)
        self.spellerStartedFlag = 0
        self.spellerEndedFlag   = 0
        
        # flagi zwiÄ…zane ze spellerem (nesw)
        self.NeswSpellerStartedFlag = 0
        self.NeswSpellerEndedFlag   = 0    
        self.neswDecisionMadeFlag   = 0
        
        # old flags
        #self.spellerFlag            = 0
        #self.spellerCalibrationFlag = 0
        #self.afterFlag              = 0
        
        #self.afterCalibration7      = 0
        #self.afterCalibration8      = 0

    def setDefaultSettings(self):
        ''' Set GUI defaul configuration.

        Function sets all gui parameters to its default values.

        '''
        self.config['Mirrored']                    = self.defaults['Mirrored']
        self.config['Fliped']                      = self.defaults['Fliped']
        self.config['ResolutionIndex']             = self.defaults['ResolutionIndex']
        self.config['PupilBar']                    = self.defaults['PupilBar']
        self.config['NumberOfGlints']              = self.defaults['NumberOfGlints']
        self.config['Sampling']                    = self.defaults['Sampling']
        self.config['ApplicationAlgorithmIndex']   = self.defaults['ApplicationAlgorithmIndex']
        self.config['CalibrationAlgorithmIndex']   = self.defaults['CalibrationAlgorithmIndex']
        
        self.config['UseKalman']                   = self.defaults['UseKalman']
        
        self.config['CursorApplicationSmoothness'] = self.defaults['CursorApplicationSmoothness']
        self.config['CalibrationSpeed']            = self.defaults['CalibrationSpeed']
        self.config['Averaging']                   = self.defaults['Averaging']

        self.config['NeswThreshold']               = self.defaults['NeswThreshold']
        self.config['NeswQueueLength']             = self.defaults['NeswQueueLength']
        self.config['NeswDeadTime']                = self.defaults['NeswDeadTime']

    def setWidgetsState(self):
        ''' Set state of gui widgets according to self.config variable.
        '''
        warningFlag = False
        
        try:
            self.ui.cmb_setCalibrationAlgorithm.setCurrentIndex(self.config['CalibrationAlgorithmIndex'] )
        except KeyError:
            self.config['CalibrationAlgorithmIndex']  = self.defaults['CalibrationAlgorithmIndex']
            self.ui.cmb_setCalibrationAlgorithm.setCurrentIndex(self.defaults['CalibrationAlgorithmIndex'])
            print 'No CalibrationAlgorithmIndex in configuration file present -- loading default value.'
            warningFlag = True
            
        try:
            self.ui.cmb_setApplicationAlgorithm.setCurrentIndex(self.config['ApplicationAlgorithmIndex'] )
        except KeyError:
            self.config['ApplicationAlgorithmIndex']  = self.defaults['ApplicationAlgorithmIndex']
            self.ui.cmb_setApplicationAlgorithm.setCurrentIndex(self.defaults['ApplicationAlgorithmIndex'])
            print 'No ApplicationAlgorithmIndex in configuration file present -- loading default value.'
            warningFlag = True
            
        try:
            self.ui.cmb_setResolution.setCurrentIndex(self.config['ResolutionIndex'] )       
        except KeyError:
            self.config['ResolutionIndex']  = self.defaults['ResolutionIndex']
            self.ui.cmb_setResolution.setCurrentIndex(self.defaults['ResolutionIndex'])
            print 'No ResolutionIndex in configuration file present -- loading default value.'
            warningFlag = True
            
        try:
            self.ui.hsb_pupil.setValue(self.config['PupilBar'])
            self.ui.hsb_glint.setValue(self.config['NumberOfGlints'])
            self.ui.hsb_calibrationSpeed.setValue(self.config['CalibrationSpeed'])
            self.ui.hsb_applicationSmoothness.setValue(self.config['CursorApplicationSmoothness'] * 100)
            self.ui.hsb_averaging.setValue(self.config['Averaging'])
            
        except KeyError:
            self.config['PupilBar']                     = self.defaults['PupilBar']
            self.config['NumberOfGlints']               = self.defaults['NumberOfGlints']
            self.config['CursorApplicationSmoothness']  = self.defaults['CursorApplicationSmoothness']
            self.config['CalibrationSpeed']             = self.defaults['CalibrationSpeed']
            self.config['Averaging']                    = self.defaults['Averaging']
            
            self.ui.hsb_pupil.setValue(self.defaults['PupilBar'])
            self.ui.hsb_glint.setValue(self.defaults['NumberOfGlints'])
            self.ui.hsb_calibrationSpeed.setValue(self.defaults['CalibrationSpeed'])
            self.ui.hsb_applicationSmoothness.setValue(self.defaults['CursorApplicationSmoothness'])
            self.ui.hsb_averaging.setValue(self.defaults['Averaging'])
                        
            print 'Either NumberOfGlints, Averaging, CalibrationSpeed, ApplicationSmoothness or PupilBar (or any combination of them) not present in configuration file -- loading default values.'
            warningFlag = True

        try:
            self.ui.hsb_neswThreshold.setValue(self.config['NeswThreshold'])
            self.ui.hsb_neswQueueLength.setValue(self.config['NeswQueueLength'])
            self.ui.hsb_neswDeadTime.setValue(self.config['NeswDeadTime'])
            
        except KeyError:
            self.config['NeswThreshold']               = self.defaults['NeswThreshold']
            self.config['NeswQueueLength']             = self.defaults['NeswQueueLength']
            self.config['NeswDeadTime']                = self.defaults['NeswDeadTime']
            
            self.ui.hsb_neswThreshold.setValue(self.config['NeswThreshold'])
            self.ui.hsb_neswQueueLength.setValue(self.config['NeswQueueLength'])
            self.ui.hsb_neswDeadTime.setValue(self.config['NeswDeadTime'])

                        
            print 'Either NeswThreshold, NeswQueueLength or NeswDeadTime (or any combination of them) not present in configuration file -- loading default values.'
            warningFlag = True
                    
        self.ui.lbl_pupil.setText(str(self.ui.hsb_pupil.value()))
        self.ui.lbl_glint.setText(str(self.ui.hsb_glint.value()))
        self.ui.lbl_averagingN.setText(str(self.ui.hsb_averaging.value()))
        self.ui.lbl_applicationSmoothnessN.setText(str(self.ui.hsb_applicationSmoothness.value()/100.))
        self.ui.lbl_calibrationSpeedN.setText(str(self.ui.hsb_calibrationSpeed.value()))
        self.ui.lbl_neswThresholdN.setText(str(self.ui.hsb_neswThreshold.value()))
        self.ui.lbl_neswQueueLengthN.setText(str(self.ui.hsb_neswQueueLength.value()))
        self.ui.lbl_neswDeadTimeN.setText(str(self.ui.hsb_neswDeadTime.value()))
        
        try:
            if self.config['Mirrored'] == 1:
                self.ui.chb_mirror.toggle()
            if self.config['Fliped'] == 1:
                self.ui.chb_flip.toggle()
            if self.config['UseKalman'] == 1:
                self.ui.chb__useKalmanFiltration.toggle()
        except KeyError:
            self.config['Mirrored']  = self.defaults['Mirrored']
            self.config['Fliped']    = self.defaults['Fliped']
            self.config['UseKalman'] = self.defaults['UseKalman']
            
            if self.config['Mirrored'] == 1:
                self.ui.chb_mirror.toggle()
            if self.config['Fliped'] == 1:
                self.ui.chb_flip.toggle()
            if self.config['UseKalman'] == 1:
                self.ui.chb__useKalmanFiltration.toggle()

            print 'Either Mirrored, Fliped or UseKalman (or any combination of them) not present in configuration file -- loading default values.'
            warningFlag = True
            
            
        if warningFlag == True:
            print 'Some variables were not present in configuration file. Saving current settings should solve this issue.'


##################################################################################
##################################################################################
##################################################################################
### SETTINGS MODULE: ###
##################################################################################

    def clearSettings(self):
        ''' Restore GUI default configuration.

        Function clears all parameters saved previously in a config file
        and set gui to a default state.
        '''

        self.setDefaultSettings()
        self.saveSettings()
        self.setWidgetsState()

    def saveSettings(self):
        ''' Save GUI settings.

        Saves GUI parameters specified file.
        '''

        with open(self.configFileName , 'w') as f:

            for key in self.config.keys():
                stringToWrite = key + ' ' + str(self.config[key]) + '\n'
                f.write(stringToWrite)

    def loadSettings(self):
        ''' Load GUI settings from file.

        Loads parameters of a programm from a specified file. If
        file is not present, default parameters would be loaded.
        '''

        self.config = {}

        directory = self.configFileName[0 : self.configFileName.find('configFile')]
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            with open(self.configFileName , 'r') as configFile:
                for line in configFile:
                    tmp = line.split()
                    try:
                        self.config[str(tmp[0])] = int(tmp[1])
                    except ValueError:
                        self.config[str(tmp[0])] = float(tmp[1])

        except IOError:
            print 'No config file yet -- using defaults'
            self.setDefaultSettings()


##################################################################################
##################################################################################
##################################################################################
### WIDGET BEHAVIOUR: ###
##################################################################################

    def swichKalman(self):
        if self.config['UseKalman'] == 0:
            self.config['UseKalman'] = 1
        else:
            self.config['UseKalman'] = 0
            

    def applicationAlgorithmChange(self):
        ''' Change eyetracker algorithm.

        Function changing algorithm for eyetracker.
        '''

        ind = self.ui.cmb_setApplicationAlgorithm.currentIndex()

        self.config['ApplicationAlgorithmIndex']  = ind
    
    
    def calibrationAlgorithmChange(self):
        ''' Change eyetracker algorithm.

        Function changing algorithm for eyetracker.
        '''

        ind = self.ui.cmb_setCalibrationAlgorithm.currentIndex()

        self.config['CalibrationAlgorithmIndex']  = ind        


    def hsbNeswThreshold_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''
        self.ui.lbl_neswThresholdN.setText(str(value))
        self.config['NeswThreshold'] = value
        
    def hsbNeswQueueLength_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''
        self.ui.lbl_neswQueueLengthN.setText(str(value))
        self.config['NeswQueueLength'] = value    

    def hsbNeswDeadTime_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''
        self.ui.lbl_neswDeadTimeN.setText(str(value))
        self.config['NeswDeadTime'] = value 

    def hsbAveraging_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''
        self.ui.lbl_averagingN.setText(str(value))
        self.config['Averaging'] = value
        self.setVariablesState(1)

    def hsbCalibrationSpeed_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''
        self.ui.lbl_calibrationSpeedN.setText(str(value))
        self.config['CalibrationSpeed'] = value

    def hsbApplicationSmoothness_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''
        self.ui.lbl_applicationSmoothnessN.setText(str(value / 100.))
        self.config['CursorApplicationSmoothness'] = value / 100.


    def cameraChange(self):
        ''' Change camera between avalaible devices.
        '''

        self.ui.timer.stop()
        self.camera.close()
        #self.glints_stack = np.zeros([self.config['Alpha'],3])
        #self.pupils_stack = np.zeros([self.config['Alpha'],3])
        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())
        self.camera = Camera(self.cameras[self.selectedCamera], 
                             {3 : self.w, 4 : self.h})
        self.ui.timer.start(1000/self.config['Sampling'], self)

    def imageMirror(self):
        ''' Set a variable telling the gui to mirror incomming frames from a camera.
        '''

        if self.config['Mirrored'] == 0:
            self.config['Mirrored'] = 1
        else:
            self.config['Mirrored'] = 0

    def imageFlip(self):
        ''' Set a variable telling the gui to flip incomming frames from a camera.
        '''

        if self.config['Fliped'] == 0:
            self.config['Fliped'] = 1
        else:
            self.config['Fliped'] = 0

    def resolutionChange(self):
        ''' Set a chosen resolution of a camera.

        It does not change an image displayed in the gui,
        but sets variable for eyetracker programm.
        '''
        ind = self.ui.cmb_setResolution.currentIndex()
        self.config['ResolutionIndex']  = ind

    def hsbPupil_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''
        self.ui.lbl_pupil.setText(str(value))
        self.config['PupilBar'] = value

#     def hsbPupilNumber_Change(self, value):
#         ''' Set a text in a gui according to the possition of a slider.
# 
#         Parameters
#         -----------
#         value : int
#             value to be displayed in an apriopriate label
#         '''
# 
#         self.ui.lbl_pupil2.setText(str(value))
#         self.config['NumberOfPupils'] = value

    def hsbGlint_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''

        self.ui.lbl_glint.setText(str(value))
        self.config['NumberOfGlints'] = value

##################################################################################
##################################################################################
##################################################################################
### FINDING & DRAWING PUPILS & GLINTS: ###
##################################################################################

    def findBestPupil(self):
        """It finds right pupil values from glint *where_glint* 
        and pupils positions *where_pupil*"""
         
        #xsr,ysr = np.mean(self.where_glint,axis=0)   # liczy Ĺ›redni glint
        
        # najlepszy = najbliĹĽszy poprzedniemu 
        xsr = self.lastKnownPupilParameters[0]
        ysr = self.lastKnownPupilParameters[1]
        ls  = []
        #r   = 0.0
         
        try:                                    # wyznacza pupil najbliĹĽszy xsr ysr
            for wsp in self.where_pupil:
                #print 'xsr={}, wsp0={}, ysr={}, wsp1={}'.format(xsr,wsp[0],ysr,wsp[1])
                r = np.sqrt( (xsr-wsp[0])**2 + (ysr-wsp[1])**2 )
                ls.append([r,wsp[0],wsp[1]])
        except TypeError:
            return np.array([np.NaN,np.NaN])
        
        self.lastKnownPupilParameters = min(ls)[1:] # podstawia nowy poprzedni pupil
        
        return np.array(min(ls)[1:]) , min(ls)[0]



    def mean_pupfinder(self):
        """It averages *pupilsQueueDepth* positions of the best finded pupil"""
        fp , self.pupilRadius = self.findBestPupil()

        if not np.any(np.isnan(fp)):
            self.pupilsQueue[:self.pupilsQueueDepth-1,:] = self.pupilsQueue[1:,:]
            self.pupilsQueue[self.pupilsQueueDepth-1,:] = fp
        else:
            fp = None 
            
        #self.ddd = np.mean(self.pupilsQueue,axis=0).astype(np.uint)
        return np.mean(self.pupilsQueue,axis=0).astype(np.uint)
    
    def pupilUpdate(self, image):
        '''

        Parameters
        -----------
        image : np.array
            image on which pupil should be find and marked.

        '''
        tmp_pupil = []
        
        self.pupil , self.where_pupil , self.pupils_stack = drawPupil(image , self.config['PupilBar'] , self.pupils_stack)
        
        try:
            mx,my =  self.mean_pupfinder()
        except TypeError:
            mx,my = [0,0]
        
        self.mx = mx
        self.my = my
        

    def glintUpdate(self, image):
        '''

        Parameters
        -----------
        image : np.array
            image on which glints should be find and marked.
        '''
        #if self.afterCalibration8 == 0:
        
        self.glint , self.where_glint , self.glints_stack = drawGlint(image , self.where_pupil , self.config['NumberOfGlints'] , self.glints_stack , 0 )

    def paintEvent(self, event):
        '''

        Parameters
        -----------
        event : object
            standard event handler as described in QT4 documentation.

        '''
        painter = QtGui.QPainter(self)

        if self.timer_on:
            
            mark(self.glint, np.array([self.mx,self.my]),radius=20, color='green')
            mark(self.glint, self.where_pupil , color='blue')
            
            mark(self.pupil, np.array([self.mx,self.my]),radius=20, color='green')
            mark(self.pupil, self.where_pupil , color='blue')
            mark(self.pupil, self.where_glint , color='red')
            
            
            result_pupil = QtGui.QImage(self.pupil, self.w, self.h, QtGui.QImage.Format_RGB888).rgbSwapped()
            
            result_glint = QtGui.QImage(self.glint, self.w, self.h, QtGui.QImage.Format_RGB888).rgbSwapped()
            
            painter.drawImage(QtCore.QPoint(20, 50), result_pupil)
            
            #painter.drawImage(QtCore.QPoint(20, 50), result_glint)

##################################################################################
##################################################################################
##################################################################################
### CALIBRATION & APPLICATION HANDLING: ###
##################################################################################
             
    def startButtonClicked(self):
        ''' Handles the behavior of the start/stop button, based on parameters picked from gui.
        '''
        
        if self.startFlag == 0:
            self.startFlag = 1
            self.ui.btn_start.setText('Stop')
            
        else:
            self.startFlag              = 0
            self.afterCalibrationFlag   = 0
            self.calibrationEndedFlag   = 0
            self.calibrationStartedFlag = 0
            self.spellerEndedFlag       = 0
            self.spellerStartedFlag     = 0
            self.neswSpellerStartedFlag = 0
            self.neswSpellerEndedFlag   = 0
            self.ui.btn_start.setText('Start')
            
            if self.get_algorithm('app') == 'Speller' and self.get_algorithm('calib') == 'Cursor calibration':
                self.procHandler.terminate()
                
            if self.get_algorithm('app') == 'Speller' and self.get_algorithm('calib') == 'NESW calibration':
                self.neswSpellerWindowHandler.close()

    def get_algorithm(self , where):
        if where == 'calib':
            return str(self.ui.cmb_setCalibrationAlgorithm.currentText())
        elif where == 'app':
            return str(self.ui.cmb_setApplicationAlgorithm.currentText())


    def runEyetracker(self):
        ''' Starts eyetracker with parameters picked from gui.
        '''
        if self.startFlag == 1 and self.afterCalibrationFlag == 1:
            self.applicationAlgorithms[self.get_algorithm('app')]()
            
        elif self.startFlag == 1 and self.afterCalibrationFlag == 0:
            self.calibrationAlgorithms[self.get_algorithm('calib')]()
        else:
            pass


       
    def module_raw(self):
        print 'Original pupil coordinates: {}.'.format(self.where_pupil)
        print 'Chosen pupil position: x={}, y={}'.format(self.mx , self.my)
        print 'Glint coordinates: {}.'.format(self.where_glint)
        
    def module_speller(self):
        if str(self.ui.cmb_setCalibrationAlgorithm.currentText()) == 'Cursor calibration':
            if self.spellerStartedFlag == 0 and self.spellerEndedFlag == 0:
                app_args = ['python3' , '-m', 'pisak.viewer.photo_edit']
                #app_args = ['python3' , '-m', 'pisak.speller.application']
                #app_args = ['python3' , '-m', 'pisak.pisak_speller']
                self.procHandler = subprocess.Popen(app_args , stdin=subprocess.PIPE , stdout=subprocess.PIPE , stderr=subprocess.PIPE)
                self.spellerStartedFlag = 1
                
            elif self.spellerStartedFlag == 1 and self.spellerEndedFlag == 0:
                data2send = self.fixationPointAfterCursorCalibration()
                self.procHandler.stdin.write(data2send)
                
        elif str(self.ui.cmb_setCalibrationAlgorithm.currentText()) == 'NESW calibration':
            if self.spellerStartedFlag == 0 and self.spellerEndedFlag == 0:
                greeness_time        = int(self.config['NeswDeadTime'] / 3.)
                self.neswStopniownik = self.config['NeswThreshold']
                self.neswTmpStop     = 0
                self.neswStop        = 0
                self.neswTmpField    = -1
                
                self.neswSpellerWindowHandler = NeswSpellerForm(greeness_time)
                self.neswSpellerWindowHandler.showMaximized()
                
                self.neswDecisionQueueLength = self.config['NeswQueueLength']
                self.neswDecisionQueue       = []
                
                self.neswDecisionMadeFlag       = 0   # poczÄ…tkowo jest dopychanie kolejki
                self.neswDecisionAlmostMadeFlag = 0
                self.neswDeadTimeCounter        = 0
                self.neswDeadTimeLength         = self.config['NeswDeadTime']
                self.neswThreshold              = self.config['NeswThreshold']
                
                self.spellerStartedFlag = 1
                
            elif self.spellerStartedFlag == 1 and self.spellerEndedFlag == 0:
                
                if self.neswDecisionMadeFlag == 1 and self.neswDeadTimeCounter < self.neswDeadTimeLength:        # trwa czas martwy
                    #print 'czas martwy'
                    
                    self.neswDecisionQueue.pop(0)
                    self.neswDecisionQueue.append([self.mx - self.center_x , self.my - self.center_y])
                    
                    xsr , ysr       = np.array(self.neswDecisionQueue).mean(0)
                    form_x , form_y = self.neswPrepareVector(xsr , ysr)
                    
                    self.neswDeadTimeCounter += 1
                    
                elif self.neswDecisionMadeFlag == 1 and self.neswDeadTimeCounter == self.neswDeadTimeLength:     # koĹ„czy siÄ™ czas martwy
                    #print 'koniec czasu martwego'
                    self.neswDecisionMadeFlag = 0
                    self.neswDeadTimeCounter  = 0
                elif self.neswDecisionMadeFlag == 0 and len(self.neswDecisionQueue) < self.neswDecisionQueueLength:     # mam niepeĹ‚nÄ… kolejkÄ™
                    #print 'dopeĹ‚nianie kolejki'
                    self.neswDecisionQueue.append([self.mx - self.center_x , self.my - self.center_y])
                elif self.neswDecisionMadeFlag == 0 and len(self.neswDecisionQueue) == self.neswDecisionQueueLength:     # mam peĹ‚nÄ… kolejkÄ™
                    #print 'tryb standardowy'
                    self.neswDecisionQueue.pop(0)
                    self.neswDecisionQueue.append([self.mx - self.center_x , self.my - self.center_y])
                                     
                    xsr , ysr = np.array(self.neswDecisionQueue).mean(0)
                    
                    form_x , form_y = self.neswPrepareVector(xsr , ysr)
                    
                    w_1 = self.neswSpellerWindowHandler.ui.btn_1.width()
                    h_1 = self.neswSpellerWindowHandler.ui.btn_1.height()
                    x_1 = self.neswSpellerWindowHandler.ui.btn_1.x()
                    y_1 = self.neswSpellerWindowHandler.ui.btn_1.y()

                    w_2 = self.neswSpellerWindowHandler.ui.btn_2.width()
                    h_2 = self.neswSpellerWindowHandler.ui.btn_2.height()
                    x_2 = self.neswSpellerWindowHandler.ui.btn_2.x()
                    y_2 = self.neswSpellerWindowHandler.ui.btn_2.y()

                    w_3 = self.neswSpellerWindowHandler.ui.btn_3.width()
                    h_3 = self.neswSpellerWindowHandler.ui.btn_3.height()
                    x_3 = self.neswSpellerWindowHandler.ui.btn_3.x()
                    y_3 = self.neswSpellerWindowHandler.ui.btn_3.y()

                    w_4 = self.neswSpellerWindowHandler.ui.btn_4.width()
                    h_4 = self.neswSpellerWindowHandler.ui.btn_4.height()
                    x_4 = self.neswSpellerWindowHandler.ui.btn_4.x()
                    y_4 = self.neswSpellerWindowHandler.ui.btn_4.y()
                    
                    w_5 = self.neswSpellerWindowHandler.ui.btn_5.width()
                    h_5 = self.neswSpellerWindowHandler.ui.btn_5.height()
                    x_5 = self.neswSpellerWindowHandler.ui.btn_5.x()
                    y_5 = self.neswSpellerWindowHandler.ui.btn_5.y()
                    
                    w_6 = self.neswSpellerWindowHandler.ui.btn_6.width()
                    h_6 = self.neswSpellerWindowHandler.ui.btn_6.height()
                    x_6 = self.neswSpellerWindowHandler.ui.btn_6.x()
                    y_6 = self.neswSpellerWindowHandler.ui.btn_6.y()
                    
                    w_7 = self.neswSpellerWindowHandler.ui.btn_7.width()
                    h_7 = self.neswSpellerWindowHandler.ui.btn_7.height()
                    x_7 = self.neswSpellerWindowHandler.ui.btn_7.x()
                    y_7 = self.neswSpellerWindowHandler.ui.btn_7.y()
                    
                    w_8 = self.neswSpellerWindowHandler.ui.btn_8.width()
                    h_8 = self.neswSpellerWindowHandler.ui.btn_8.height()
                    x_8 = self.neswSpellerWindowHandler.ui.btn_8.x()
                    y_8 = self.neswSpellerWindowHandler.ui.btn_8.y()
                                        
                    if form_x < x_1 + w_1 and form_y < y_1 + h_1:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(1)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 1:
                            self.neswSpellerWindowHandler.benz(1,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 1:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 1
                            self.neswDecisionAlmostMadeFlag = 1

                        
                    elif form_x < x_2 + w_2 and form_y < y_2 + h_2 and form_y > y_2:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(2)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 2:
                            self.neswSpellerWindowHandler.benz(2,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 2:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 2
                            self.neswDecisionAlmostMadeFlag = 1
                                                
                    elif form_x < x_3 + w_3 and form_y > y_3:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(3)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 3:
                            self.neswSpellerWindowHandler.benz(3,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 3:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 3
                            self.neswDecisionAlmostMadeFlag = 1

                    elif form_x > x_4 and form_y < y_4 + h_4:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(4)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 4:
                            self.neswSpellerWindowHandler.benz(4,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 4:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 4
                            self.neswDecisionAlmostMadeFlag = 1

                    elif form_x > x_5 and form_y < y_5 + h_5 and form_y > y_5:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(5)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 5:
                            self.neswSpellerWindowHandler.benz(5,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 5:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 5
                            self.neswDecisionAlmostMadeFlag = 1
                        
                    elif form_x > x_6 and form_y > y_6:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(6)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 6:
                            self.neswSpellerWindowHandler.benz(6,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 6:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 6
                            self.neswDecisionAlmostMadeFlag = 1
                        
                    elif form_x < x_7 + w_7 and form_x > x_7 and form_y < y_7 + h_7:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(7)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 7:
                            self.neswSpellerWindowHandler.benz(7,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 7:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 7
                            self.neswDecisionAlmostMadeFlag = 1
                        
                    elif form_x < x_8 + w_8 and form_x > x_8 and form_y > y_8:
                        if self.neswStop == self.neswStopniownik:
                            self.neswStop = 0
                            self.addZerosToDecisionQueue()
                            self.neswSpellerWindowHandler.buttonPressed(8)
                            self.neswDecisionMadeFlag = 1
                            
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField == 8:
                            self.neswSpellerWindowHandler.benz(8,self.neswStop)
                            self.neswDecisionAlmostMadeFlag = 1
                        
                        elif self.neswStop < self.neswStopniownik and self.neswTmpField != 8:
                            self.neswSpellerWindowHandler.benz(-1)
                            self.neswTmpStop  = 0
                            self.neswStop     = 0
                            self.neswTmpField = 8
                            self.neswDecisionAlmostMadeFlag = 1                  

                    else:
                        pass
                        #print 'No decision'
                    
                    
                    if self.neswDecisionAlmostMadeFlag == 1:
                        if self.neswTmpStop < 10:
                            self.neswTmpStop += 1
                            self.neswDecisionAlmostMadeFlag = 0
                        elif self.neswTmpStop == 10:
                            self.neswTmpStop = 0
                            self.neswDecisionAlmostMadeFlag = 0
                            self.neswStop += 1
      
        else:
            pass


    def addZerosToDecisionQueue(self):
        for ind1 in range(0,len(self.neswDecisionQueue),1):
            self.neswDecisionQueue[ind1] = [5,5]

    def neswPrepareVector(self, xsr , ysr):
        
        formWidth  = self.neswSpellerWindowHandler.ui.trueScreen.width()
        formHeight = self.neswSpellerWindowHandler.ui.trueScreen.height()
        
        VectorEndX = int(formWidth * (xsr-self.neswLeft) / float(self.neswRight - self.neswLeft))
        VectorEndY = int(formHeight * (ysr-self.neswTop) / float(self.neswBottom - self.neswTop))
        
        self.neswSpellerWindowHandler.plotVector(VectorEndX , VectorEndY)
        
        return(VectorEndX , VectorEndY)
    
        
    def calibrationModule_raw(self):
        '''In fact - no calibration'''
        self.afterCalibrationFlag = 1
        # Needs to be changed !!!
        
        
    def calibrationModule_cursor(self):
        if self.calibrationStartedFlag == 0 and self.calibrationEndedFlag == 0:
            self.calibrationWindowHandler = CursorCalibrationForm( self.config['CalibrationSpeed'] )
            self.calibrationWindowHandler.showMaximized()
            self.calibrationStartedFlag = 1
            
        elif self.calibrationStartedFlag == 1 and self.calibrationEndedFlag == 0:
            if self.calibrationWindowHandler.done == 1:
                self.calibrationEndedFlag = 1
                self.calibrationWindowHandler.close()
                
            elif self.calibrationWindowHandler.now == 1:
                self.circlePositionX.append( self.calibrationWindowHandler.pos_x )
                self.circlePositionY.append( self.calibrationWindowHandler.pos_y )
                
                self.eyePositionX.append(self.mx)
                self.eyePositionY.append(self.my)
                
            else:
                pass
        
        
        elif self.calibrationEndedFlag == 1 and self.calibrationStartedFlag == 1:
            self.x_true = np.array(self.circlePositionX)
            self.y_true = np.array(self.circlePositionY)
            self.x_esti = np.array(self.eyePositionX)
            self.y_esti = np.array(self.eyePositionY)
            
            #print 'x_true: {}.'.format(self.x_true)
            #print 'y_true: {}.'.format(self.y_true)
            #print 'x_esti: {}.'.format(self.x_esti)
            #print 'y_esti: {}.'.format(self.y_esti)
            
            self.x_opt, self.x_pcov = curve_fit(f_for_fitting , (self.x_esti , self.y_esti) , self.x_true)
            self.y_opt, self.y_pcov = curve_fit(f_for_fitting , (self.x_esti , self.y_esti) , self.y_true)
            
            self.calibrationStartedFlag = 0
            self.afterCalibrationFlag   = 1
        else:
            pass
    
    
    
    
    
    
    
    def calibrationModule_nesw(self):
        if self.calibrationStartedFlag == 0 and self.calibrationEndedFlag == 0:
            self.calibrationWindowHandler = NeswCalibrationForm( self.config['CalibrationSpeed'] )
            self.calibrationWindowHandler.showMaximized()
            self.calibrationStartedFlag = 1
            
        elif self.calibrationStartedFlag == 1 and self.calibrationEndedFlag == 0:
            if self.calibrationWindowHandler.done == 1:
                self.calibrationEndedFlag = 1
                self.calibrationWindowHandler.close()
                
                #print self.eyePositionX
                #print self.eyePositionY
                
            elif self.calibrationWindowHandler.now == 1:
                
                self.eyePositionX.append(self.mx)
                self.eyePositionY.append(self.my)
                
            else:
                pass
        
        
        elif self.calibrationEndedFlag == 1 and self.calibrationStartedFlag == 1:
            #self.x_true = np.array(self.rectanglePositionX)
            #self.y_true = np.array(self.rectanglePositionY)
            
            #print self.eyePositionX , self.eyePositionY
            
            self.eyePositionX.sort()
            self.eyePositionY.sort()
            
            self.eyePositionX_min = np.array(self.eyePositionX[1:20]).mean()
            self.eyePositionX_max = np.array(self.eyePositionX[-20:]).mean()
            self.eyePositionY_min = np.array(self.eyePositionY[1:20]).mean()
            self.eyePositionY_max = np.array(self.eyePositionY[-20:]).mean()
            
            self.center_x = int((self.eyePositionX_max + self.eyePositionX_min ) / 2.)
            self.center_y = int((self.eyePositionY_max + self.eyePositionY_min ) / 2.)            
            
            self.neswRight  = int(self.eyePositionX_max - self.center_x)
            self.neswTop    = int(self.eyePositionY_min - self.center_y)
            self.neswLeft   = int(self.eyePositionX_min - self.center_x)
            self.neswBottom = int(self.eyePositionY_max - self.center_y)
            
            #print 'Left = {}, Right = {}, Top = {}, Bottom = {}'.format(self.neswLeft, self.neswRight, self.neswTop, self.neswBottom ) 
            
            self.calibrationStartedFlag = 0
            self.afterCalibrationFlag   = 1
        else:
            pass





    def fixationPointAfterCursorCalibration(self):
        
        [a1,b1,c1,d1,e1,f1] = self.x_opt
        [a2,b2,c2,d2,e2,f2] = self.y_opt
        
        screen_y = f_for_fitting((self.mx,self.my) , a1,b1,c1,d1,e1,f1)
        screen_x = f_for_fitting((self.mx,self.my) , a2,b2,c2,d2,e2,f2)
                
        # uĹĽycie wiedzy o poprzednim poĹ‚oĹĽeniu  
        screen_x = (1-self.config['CursorApplicationSmoothness']) * screen_x + self.config['CursorApplicationSmoothness']*self.last_screen_x
        screen_y = (1-self.config['CursorApplicationSmoothness']) * screen_y + self.config['CursorApplicationSmoothness']*self.last_screen_y
        
        # update poprzedniego poĹ‚oĹĽenia
        self.last_screen_x = screen_x
        self.last_screen_y = screen_y
        
        if screen_x > self.ui.trueScreen.width():
            screen_x = self.ui.trueScreen.width() - 10
        elif screen_x < 0:
            screen_x = 10
        
        if screen_y > self.ui.trueScreen.height():
            screen_y = self.ui.trueScreen.height() - 10
        elif screen_y < 0:
            screen_y = 10        
        
        
        result_string = str(int(screen_x)) + ' ' + str(int(screen_y)) + '\n'
        #print result_string
        return result_string










  




###################################################################################################################################################


class CursorCalibrationForm(QtGui.QMainWindow):

    def __init__(self, calibrationSpeed , parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_CursorCalibrationWindow()
        self.ui.setupUi(self)
        
        self.calibrationSpeed = calibrationSpeed
        self.done = 0
        self.now  = 0
        
        self.width  = self.ui.trueScreen.width()
        self.height = self.ui.trueScreen.height()
        
        self.boost_x = int( self.width / 5. )
        self.boost_y = int( self.height / 5. )
        

        self.circles = []
        for x in range(self.boost_x , self.boost_x*5 , self.boost_x):
            for y in range(self.boost_y , self.boost_y*5 , self.boost_y):
                for r in range(calibrationSpeed , 0 , -1):
                    if calibrationSpeed > 20:
                        self.circles.append((x,y,r))
                    else:
                        self.circles.append((x,y,2*r))
                        
        self.counter = 0
        self.ui.timer.start(1000./30, self)

        
    
    def timerEvent(self, event):
        
        if self.counter == len(self.circles):
            self.done = 1
            self.ui.timer.stop()
            return
            #self.close()
        else:
            self.pos_x = self.circles[self.counter][0]
            self.pos_y = self.circles[self.counter][1]
            self.r_x   = self.circles[self.counter][2]
            self.r_y   = self.r_x
            if self.counter % self.calibrationSpeed == 0:
                self.now = 1
            else:
                self.now = 0
            
            self.update()
            
            self.counter += 1
        
    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)

        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.setPen(QtGui.QColor(0,255,0))
        paint.setBrush(QtGui.QColor(0,0,255))
         
        center = QtCore.QPoint(self.pos_x, self.pos_y)
        paint.drawEllipse(center, self.r_x, self.r_y)
        
        paint.end()
        



###################################################################################################################################################

class NeswCalibrationForm(QtGui.QMainWindow):

    def __init__(self, calibrationSpeed , parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_NeswCalibrationWindow()
        self.ui.setupUi(self)
        
        self.calibrationSpeed = calibrationSpeed
        
        self.done = 0
        self.now  = 0
        
        self.width  = self.ui.trueScreen.width()
        self.height = self.ui.trueScreen.height()  
        
        self.baseRectangles = [[0 , 0 , 40 , 40] , [self.width/2.-20 , 0 , 40 , 40] , [self.width-40 , 0 , 40 , 40] , [self.width-40 , self.height/2.-60 , 40 , 40] , [self.width-40 , self.height-95 , 40 , 40] , [self.width/2.-20 , self.height-95 , 40 , 40] , [0 , self.height-95 , 40 , 40] , [0 , self.height/2.-60 , 40 , 40] ]
        self.iter           = 0
        self.tmp_iter       = 0
        
        self.rectangle = self.baseRectangles[self.iter]
        self.tmp_iter += 1
        
        self.ui.timer.start(1000./30, self)
        
    def timerEvent(self, event):
        self.rectangle = self.baseRectangles[self.iter]
        self.update()
        self.now = 1
        
        self.tmp_iter += 1
        
        if self.tmp_iter == self.calibrationSpeed:
            self.iter     += 1
            self.tmp_iter = 0
            self.now      = 0
        
        if self.iter == len(self.baseRectangles):
            self.done = 1
            self.ui.timer.stop()
            return
        
    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
 
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.setPen(QtGui.QColor(255,0,0))
        paint.setBrush(QtGui.QColor(255,0,0))
        
        x,y,w,h = self.rectangle
        
        paint.drawRect(x,y,w,h)
         
        paint.end()
        
###################################################################################################################################################

class NeswSpellerForm(QtGui.QMainWindow):

    def __init__(self, greeness_time , parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.btn_labels = ["A Ä„ B C Ä† D","E Ä� F G H I","J K L Ĺ� M N","Ĺ� O Ă“ P R Q","S Ĺš T U W V","X Y Z Ĺ» Ĺą ~"]
        
        self.ui = Ui_NeswSpellerWindow()
        self.ui.setupUi(self , self.btn_labels)
        
        self.width  = self.ui.trueScreen.width()
        self.height = self.ui.trueScreen.height()
        
        self.buttons = [self.ui.btn_1 , self.ui.btn_2 , self.ui.btn_3 , self.ui.btn_4 , self.ui.btn_5 , self.ui.btn_6]
        
        self.spellerLevelFlag  = 0   # 0 - gĹ‚Ăłwne drzewo, 1 - dolna gaĹ‚Ä…Ĺş
        self.greeness_iterator = 0
        self.buttonFlag        = 0
        self.greeness_time     = greeness_time
        
        self.xx = 0
        self.yy = 0
        
        self.connect(self.ui.btn_1 , QtCore.SIGNAL("released()") , partial(self.buttonClicked, 1))
        self.connect(self.ui.btn_2 , QtCore.SIGNAL("released()") , partial(self.buttonClicked, 2))
        self.connect(self.ui.btn_3 , QtCore.SIGNAL("released()") , partial(self.buttonClicked, 3))
        self.connect(self.ui.btn_4 , QtCore.SIGNAL("released()") , partial(self.buttonClicked, 4))
        self.connect(self.ui.btn_5 , QtCore.SIGNAL("released()") , partial(self.buttonClicked, 5))
        self.connect(self.ui.btn_6 , QtCore.SIGNAL("released()") , partial(self.buttonClicked, 6))
        self.ui.btn_7.released.connect(self.deleteButtonClicked)
        self.ui.btn_8.released.connect(self.spaceButtonClicked)


        self.connect(self.ui.btn_1 , QtCore.SIGNAL("pressed()") , partial(self.buttonPressed, 1))
        self.connect(self.ui.btn_2 , QtCore.SIGNAL("pressed()") , partial(self.buttonPressed, 2))
        self.connect(self.ui.btn_3 , QtCore.SIGNAL("pressed()") , partial(self.buttonPressed, 3))
        self.connect(self.ui.btn_4 , QtCore.SIGNAL("pressed()") , partial(self.buttonPressed, 4))
        self.connect(self.ui.btn_5 , QtCore.SIGNAL("pressed()") , partial(self.buttonPressed, 5))
        self.connect(self.ui.btn_6 , QtCore.SIGNAL("pressed()") , partial(self.buttonPressed, 6))
        self.ui.btn_7.pressed.connect(self.deleteButtonPressed)
        self.ui.btn_8.pressed.connect(self.spaceButtonPressed)       

        #self.ui.timer.start(1000./30, self)
        
    def benz(self , field_id , level=1):
        
        if field_id == -1:
            color = QtGui.QColor(212 , 208 , 200 )
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Button, color)
            
            for number in range(0,6):
                pass
                self.buttons[number-1].setPalette(palette)
            self.ui.btn_7.setPalette(palette)
            self.ui.btn_8.setPalette(palette)
        else:
            #print int((level+1)*(254/6.))
            color = QtGui.QColor(0, int((level)*(254/5.)), 0 )
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Button, color)
            
            if field_id < 7:
                self.buttons[field_id-1].setPalette(palette)                 # assign new palette
                self.buttons[field_id-1].setAutoFillBackground(1)
            elif field_id == 7:
                self.ui.btn_7.setPalette(palette)                 # assign new palette
                self.ui.btn_7.setAutoFillBackground(1)            
            elif field_id == 8:
                self.ui.btn_8.setPalette(palette)                 # assign new palette
                self.ui.btn_8.setAutoFillBackground(1)
                
            
        #.backgroundRole()
        

    def paintEvent(self , event):
        
        painter = QtGui.QPainter()
        pen     = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        
        painter.begin(self)
        
        painter.setPen(pen)
        painter.drawLine(int(self.width/2.) , int(self.height/2.) , self.xx , self.yy)
        
        painter.end()

    def plotVector(self , x , y):
        self.xx = x
        self.yy = y
        self.update()

    def timerEvent(self, event):
        if self.greeness_iterator < self.greeness_time:
            self.greeness_iterator += 1
        else:
            if self.buttonFlag < 7:
                self.buttonClicked(self.buttonFlag)
            elif self.buttonFlag == 7:
                self.deleteButtonClicked()
            elif self.buttonFlag == 8:
                self.spaceButtonClicked()
            self.greeness_iterator = 0
        

    def buttonPressed(self , number):
        color = QtGui.QColor(0 , 255 , 0 )
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, color)
        if number < 7:
            self.buttons[number-1].setPalette(palette)
        elif number == 7:
            self.ui.btn_7.setPalette(palette)
        elif number == 8:
            self.ui.btn_8.setPalette(palette)
        
        self.ui.timer.start(1000./30, self)
        self.buttonFlag = number
    
    def spaceButtonPressed(self):
        color = QtGui.QColor(0 , 255 , 0 )
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, color)
        self.ui.btn_8.setPalette(palette)
        
        self.ui.timer.start(1000./30, self)
        self.buttonFlag = 8
    
    def deleteButtonPressed(self):
        color = QtGui.QColor(0 , 255 , 0 )
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, color)
        self.ui.btn_7.setPalette(palette)
        
        self.ui.timer.start(1000./30, self)
        self.buttonFlag = 7


    def buttonClicked(self , number):
        self.ui.timer.stop()
        
        color = QtGui.QColor(212 , 208 , 200 )
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, color)
        self.buttons[number-1].setPalette(palette)
            
        if self.spellerLevelFlag == 0:
            labelki = self.btn_labels[number-1].split()
            
            self.ui.btn_1.setText(_fromUtf8(labelki[0]))
            self.ui.btn_2.setText(_fromUtf8(labelki[1]))
            self.ui.btn_3.setText(_fromUtf8(labelki[2]))
            self.ui.btn_4.setText(_fromUtf8(labelki[3]))
            self.ui.btn_5.setText(_fromUtf8(labelki[4]))
            self.ui.btn_6.setText(_fromUtf8(labelki[5]))
            
            self.ui.btn_8.setText('< BACK')
            
            self.spellerLevelFlag = 1
            
            
        elif self.spellerLevelFlag == 1:
            
            letter2write = self.buttons[number-1].text()
            #self.ui.ted_text.insertPlainText(letter2write)
            textWritten  = self.ui.ted_text.text()
            
            if len(textWritten) < 30:
                text2write   = textWritten + letter2write
            else:
                text2write   = textWritten[1:] + letter2write
            
            self.ui.ted_text.setText(text2write)
            
            self.ui.retranslateUi(self , self.btn_labels)
            self.spellerLevelFlag = 0
            
    def spaceButtonClicked(self):
        self.ui.timer.stop()
        color = QtGui.QColor(212 , 208 , 200 )
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, color)
        self.ui.btn_8.setPalette(palette)
        
        if self.spellerLevelFlag == 0:              # faktyczna spacjÄ…
            letter2write = ' '
            textWritten  = self.ui.ted_text.text()
            text2write   = textWritten + letter2write
            self.ui.ted_text.setText(text2write)
            self.ui.retranslateUi(self , self.btn_labels)
            
        elif self.spellerLevelFlag == 1:            # tym razem powrĂłt do gĹ‚Ăłwnego drzewa liter
            self.ui.retranslateUi(self , self.btn_labels)
            self.spellerLevelFlag = 0
            self.ui.btn_8.setText('SPACE')
            
    
    def deleteButtonClicked(self):
        self.ui.timer.stop()
        color = QtGui.QColor(212 , 208 , 200 )
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, color)
        self.ui.btn_7.setPalette(palette)
        
        text2write = self.ui.ted_text.text()[:-1]
        self.ui.ted_text.setText(text2write)
        
        if self.spellerLevelFlag == 1:
            self.spellerLevelFlag = 0
        self.ui.retranslateUi(self , self.btn_labels)

###################################################################################################################################################

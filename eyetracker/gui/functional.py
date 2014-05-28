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


from itertools import izip
from PyQt4 import QtCore, QtGui

import numpy as np

from ..analysis.processing import imageFlipMirror, runningAverage

from ..camera.display import drawPupil, drawGlint
from ..camera.camera import lookForCameras
from ..camera.camera import Camera

from .graphical import Ui_StartingWindow, Ui_MusicPlayerWindow

import os
from functools import partial


class MyTextViewer(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MusicPlayerWindow()
        self.ui.setupUi(self)
        
    def closeEvent(self, event):
        event.accept()
        

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
        self.defaults                    = {}
        self.defaults['Mirrored']        = 0
        self.defaults['Fliped']          = 0
        self.defaults['Alpha']           = 0.6
        self.defaults['ResolutionIndex'] = 1
        self.defaults['PupilBar']        = 0
        self.defaults['NumberOfGlints']  = 2
        self.defaults['NumberOfPupils']  = 1
        self.defaults['Sampling']        = 30.0
        self.defaults['AlgorithmIndex']  = 0
        self.defaults['PupilStackDeph']  = 100.
        self.defaults['DecisionStackDeph'] = 6.
        
        self.initializeFlags()
        
        self.cameras = lookForCameras()
        for i in self.cameras.iterkeys():
            self.ui.cmb_setCamera.addItem(i)
            
        self.algorithms = {}
        self.algorithms['Raw output']   = self.module_raw
        self.algorithms['Music player'] = self.module_music
        self.algorithms['Text viewer']  = self.module_text
        self.algorithms['Keyboard']  = self.module_speller
        
        for algorithm in self.algorithms.keys():
            self.ui.cmb_setAlgorithm.addItem(algorithm)
            
        
        self.resolutions_w = [160,320,640,1280]
        self.resolutions_h = [120,240,480,720]
        for w, h in izip(self.resolutions_w, self.resolutions_h):
            self.ui.cmb_setResolution.addItem(''.join([str(w), 'x', str(h)]))
            
        self.loadSettings()
        self.setWidgetsState()

        self.w = 320
        self.h = 240

        self.selectedCamera = str(self.ui.cmb_setCamera.currentText())

        try:
            self.camera  = Camera(self.cameras['Camera_1'], {3 : self.w, 4 : self.h})
        except KeyError:
            print 'No camera device detected.'

        self.glints_stack = np.zeros([self.config['Alpha'],3])
        self.pupils_stack = np.zeros([self.config['Alpha'],3])
        #print self.pupils_stack.shape
        
        self.pupilPositionsStack = []
        self.DecisionPupilPositionsStack = []

        self.ui.timer.start(1000/self.config['Sampling'], self)
        self.timer_on = False

        self.ui.cmb_setCamera.currentIndexChanged.connect(self.cameraChange)
        self.ui.cmb_setResolution.currentIndexChanged.connect(self.resolutionChange)
        self.ui.cmb_setAlgorithm.currentIndexChanged.connect(self.algorithmChange)
        self.ui.btn_start.clicked.connect(self.startButtonClicked)
        self.ui.btn_clear.clicked.connect(self.clearSettings)
        self.ui.btn_save.clicked.connect(self.saveSettings)
        self.ui.chb_flip.stateChanged.connect(self.imageFlip)
        self.ui.chb_mirror.stateChanged.connect(self.imageMirror)
        self.ui.hsb_pupil.valueChanged[int].connect(self.hsbPupil_Change)
        self.ui.hsb_pupil2.valueChanged[int].connect(self.hsbPupilNumber_Change)
        self.ui.hsb_glint.valueChanged[int].connect(self.hsbGlint_Change)
        self.ui.led_alpha.editingFinished.connect(self.alphaChange)
        self.ui.led_pupilStackDeph.editingFinished.connect(self.pupilStackDephChange)
        self.ui.led_decisionStackDeph.editingFinished.connect(self.decisionStackDephChange)
        
        for buttonNo in range(1,7):
            self.ui.keys[buttonNo].clicked.connect(partial(self.keyButtonClicked, clickedButtonNo = buttonNo))

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
        im = imageFlipMirror(im, self.config['Mirrored'], self.config['Fliped'])

        if self.timer_on == False:
            self.im = im
            self.timer_on = True

        #self.im = runningAverage(im, self.im, self.config['Alpha'])
        self.im = im
        self.pupilUpdate(self.im)
        self.glintUpdate(self.im)
        
        ######
        if self.startFlag == 1 and self.where_pupil != None:
            if len(self.pupilPositionsStack) == self.config['PupilStackDeph']:
                self.pupilPositionsStack.pop(0)
            self.pupilPositionsStack.append(self.where_pupil)
        ######
            if len(self.DecisionPupilPositionsStack) == self.config['DecisionStackDeph']:
                self.DecisionPupilPositionsStack.pop(0)
            self.DecisionPupilPositionsStack.append(self.where_pupil)
        ######
        
        self.runEyetracker()
        
        self.update()
        
    def initializeFlags(self):
        self.musicPlayerFlag = 0
        self.startFlag       = 0
        
        self.textViewerFlag  = 0
        
        self.spellerFlag    = 0
        self.spellerLvl     = 0

    def setDefaultSettings(self):
        ''' Set GUI defaul configuration.

        Function sets all gui parameters to its default values.

        '''
        self.config['Mirrored']        = self.defaults['Mirrored']
        self.config['Fliped']          = self.defaults['Fliped']
        self.config['Alpha']           = self.defaults['Alpha']
        self.config['ResolutionIndex'] = self.defaults['ResolutionIndex']
        self.config['PupilBar']        = self.defaults['PupilBar']
        self.config['NumberOfGlints']  = self.defaults['NumberOfGlints']
        self.config['NumberOfPupils']  = self.defaults['NumberOfPupils']
        self.config['Sampling']        = self.defaults['Sampling']
        self.config['AlgorithmIndex']  = self.defaults['AlgorithmIndex']
        self.config['PupilStackDeph']    = self.defaults['PupilStackDeph']
        self.config['DecisionStackDeph']    = self.defaults['DecisionStackDeph']

    def setWidgetsState(self):
        ''' Set state of gui widgets according to self.config variable.
        '''
        warningFlag = False
        
        try:
            self.ui.cmb_setAlgorithm.setCurrentIndex(self.config['AlgorithmIndex'] )
        except KeyError:
            self.config['AlgorithmIndex']  = self.defaults['AlgorithmIndex']
            self.ui.cmb_setAlgorithm.setCurrentIndex(self.defaults['AlgorithmIndex'])
            print 'No AlgorithmIndex in configuration file present -- loading default value.'
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
            self.ui.hsb_pupil2.setValue(self.config['NumberOfPupils'])
            self.ui.hsb_glint.setValue(self.config['NumberOfGlints'])
        except KeyError:
            self.config['PupilBar'] = self.defaults['PupilBar']
            self.config['NumberOfGlints'] = self.defaults['NumberOfGlints']
            self.config['NumberOfPupils'] = self.defaults['NumberOfPupils']
            self.ui.hsb_pupil.setValue(self.defaults['PupilBar'])
            self.ui.hsb_glint.setValue(self.defaults['NumberOfGlints'])
            self.ui.hsb_pupil2.setValue(self.defaults['NumberOfPupils'])
            print 'Either NumberOfGlints, NumberOfPupils or PupilBar (or any combination of them) not present in configuration file -- loading default values.'
            warningFlag = True
                    
        self.ui.lbl_pupil.setText(str(self.ui.hsb_pupil.value()))
        self.ui.lbl_pupil2.setText(str(self.ui.hsb_pupil2.value()))
        self.ui.lbl_glint.setText(str(self.ui.hsb_glint.value()))

        try:
            if self.config['Mirrored'] == 1:
                self.ui.chb_mirror.toggle()
            if self.config['Fliped'] == 1:
                self.ui.chb_flip.toggle()
        except KeyError:
            self.config['Mirrored'] == self.defaults['Mirrored']
            self.config['Fliped'] == self.defaults['Fliped']
            
            if self.config['Mirrored'] == 1:
                self.ui.chb_mirror.toggle()
            if self.config['Fliped'] == 1:
                self.ui.chb_flip.toggle()

            print 'Either Mirrored or Fliped (or both) not present in configuration file -- loading default values.'
            warningFlag = True
            
        try:
            self.ui.led_alpha.setText(str(self.config['Alpha']))
        except KeyError:
            self.config['Alpha'] = self.defaults['Alpha']
            self.ui.led_alpha.setText(str(self.config['Alpha']))
            print 'Parameter for alpha smoothing not present in configuration file -- loading default values.'
            warningFlag = True
        
        try:
            self.ui.led_pupilStackDeph.setText(str(self.config['PupilStackDeph']))
        except KeyError:
            self.config['PupilStackDeph'] = self.defaults['PupilStackDeph']
            self.ui.led_pupilStackDeph.setText(str(self.config['PupilStackDeph']))
            print 'PupilStackDeph parameter not present in configuration file -- loading default values.'
            warningFlag = True
            
        try:
            self.ui.led_decisionStackDeph.setText(str(self.config['DecisionStackDeph']))
        except KeyError:
            self.config['DecisionStackDeph'] = self.defaults['DecisionStackDeph']
            self.ui.led_decisionStackDeph.setText(str(self.config['DecisionStackDeph']))
            print 'DecisionStackDeph parameter not present in configuration file -- loading default values.'
            warningFlag = True
            
        if warningFlag == True:
            print 'Some variables were not present in configuration file. Saving current settings should solve this issue.'

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

        self.configFileName = os.path.expanduser("~") + '/.config/eyetracker-ng/configFile.txt'

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

    def algorithmChange(self):
        ''' Change eyetracker algorithm.

        Function changing algorithm for eyetracker.
        '''

        ind = self.ui.cmb_setAlgorithm.currentIndex()

        self.config['AlgorithmIndex']  = ind

    def cameraChange(self):
        ''' Change camera between avalaible devices.
        '''

        self.ui.timer.stop()
        self.camera.close()
        self.glints_stack = np.zeros([self.config['Alpha'],3])
        self.pupils_stack = np.zeros([self.config['Alpha'],3])
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
            
        #self.glints_stack = np.zeros([self.config['Alpha'],3])
        #self.pupils_stack = np.zeros([self.config['Alpha'],3])

    def imageFlip(self):
        ''' Set a variable telling the gui to flip incomming frames from a camera.
        '''

        if self.config['Fliped'] == 0:
            self.config['Fliped'] = 1
        else:
            self.config['Fliped'] = 0
            
        #self.glints_stack = np.zeros([self.config['Alpha'],3])
        #self.pupils_stack = np.zeros([self.config['Alpha'],3])

    def resolutionChange(self):
        ''' Set a chosen resolution of a camera.

        It does not change an image displayed in the gui,
        but sets variable for eyetracker programm.
        '''

        ind = self.ui.cmb_setResolution.currentIndex()

        self.config['ResolutionIndex']  = ind
        
    def alphaChange(self):
        '''
        Set a chosen alpha parameter for smoothing purposes.
        
        Alpha is a control parameter of the running average. It describes
        how many previous glint and pupil positions should be averaged.
        By arbitrary alpha should not exceed 10 and could not be a negative
        number.
        
        value : string
            value to be assigned to alpha parameter. It would be converted
            to np.float32
        '''
        try:
            alpha = float(self.ui.led_alpha.text())
        except ValueError:
            self.ui.led_alpha.setText( str(self.config['Alpha']) )
            print 'Alpha should be a floating point number!'
            return
        
        if alpha < 0. or alpha > 1.:
            self.ui.led_alpha.setText( str(self.config['Alpha']) )
            print 'Alpha should be between 0.0 and 1.0!'
        else:
            self.config['Alpha'] = alpha
            
        self.glints_stack = np.zeros([self.config['Alpha'],3])
        self.pupils_stack = np.zeros([self.config['Alpha'],3])

    def pupilStackDephChange(self):
        '''
        Set a chosen pupilStackDeph parameter for some purposes.
        
        What is pupilStackDeph --> Sasha
        
        value : string
            value to be assigned to pupilStackDeph parameter. It would be converted
            to np.float32
        '''
        try:
            pupilStackDeph = float(self.ui.led_pupilStackDeph.text())
        except ValueError:
            self.ui.led_pupilStackDeph.setText( str(1) )                          # for now...
            #self.ui.led_pupilStackDeph.setText( str(self.config['Alpha']) )      # in future
            print 'PupilStackDeph should be a floating point number!'
            return
        
        if pupilStackDeph < 10. or pupilStackDeph > 300.:
            self.ui.led_pupilStackDeph.setText( str(100.) )                          # for now...
            #self.ui.led_alpha.setText( str(self.config['Alpha']) )             # in future
            print 'PupilStackDeph should be between 10.0 and 300.0!'
        else:
            #self.config['PupilStackDeph'] = alpha                                # in future
            pass
            
    def decisionStackDephChange(self):
        '''
        Set a chosen decisionStackDeph parameter for some purposes.
        
        What is decisionStackDeph --> Sasha
        
        value : string
            value to be assigned to decisionStackDeph parameter. It would be converted
            to np.float32
        '''
        try:
            decisionStackDeph = float(self.ui.led_decisionStackDeph.text())
        except ValueError:
            self.ui.led_decisionStackDeph.setText( str(1) )                          # for now...
            #self.ui.led_decisionStackDeph.setText( str(self.config['Alpha']) )      # in future
            print 'PupilStackDeph should be a floating point number!'
            return
        
        if decisionStackDeph < 0. or decisionStackDeph > 30.:
            self.ui.led_decisionStackDeph.setText( str(6) )                          # for now...
            #self.ui.led_alpha.setText( str(self.config['Alpha']) )             # in future
            print 'DecisionStackDeph should be between 0.0 and 10.0!'
        else:
            #self.config['DecisionStackDeph'] = alpha                                # in future
            pass

    def hsbPupil_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''

        self.ui.lbl_pupil.setText(str(value))
        self.config['PupilBar'] = value

    def hsbPupilNumber_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''

        self.ui.lbl_pupil2.setText(str(value))
        self.config['NumberOfPupils'] = value

    def hsbGlint_Change(self, value):
        ''' Set a text in a gui according to the possition of a slider.

        Parameters
        -----------
        value : int
            value to be displayed in an apriopriate label
        '''

        self.ui.lbl_glint.setText(str(value))
        self.config['NumberOfGlints'] = value

    def pupilUpdate(self, image):
        '''

        Parameters
        -----------
        image : np.array
            image on which pupil should be find and marked.

        '''
        self.pupil , self.where_pupil , self.pupils_stack = drawPupil(image , self.config['PupilBar'] , self.pupils_stack , self.config['NumberOfPupils'])

    def glintUpdate(self, image):
        '''

        Parameters
        -----------
        image : np.array
            image on which glints should be find and marked.
        '''
        self.glint , self.where_glint , self.glints_stack = drawGlint(image , self.where_pupil , self.config['NumberOfGlints'] , self.glints_stack)

    def paintEvent(self, event):
        '''

        Parameters
        -----------
        event : object
            standard event handler as described in QT4 documentation.

        '''
        painter = QtGui.QPainter(self)

        if self.timer_on:
            result_pupil = QtGui.QImage(self.pupil, self.w, self.h, QtGui.QImage.Format_RGB888).rgbSwapped()
            result_glint = QtGui.QImage(self.glint, self.w, self.h, QtGui.QImage.Format_RGB888).rgbSwapped()

            painter.drawImage(QtCore.QPoint(5, 35), result_pupil)
            painter.drawImage(QtCore.QPoint(5, 300), result_glint)

#    def closeEvent(self, event):
#        '''
#
#        Parameters
#        -----------
#        event : object
#            standard event handler as described in QT4 documentation.
#
#        '''
        
    def startButtonClicked(self):
        ''' Handles the behavior of the start/stop button, based on parameters picked from gui.
        '''
        
        if self.startFlag == 0:
            self.startFlag = 1
            self.ui.btn_start.setText('Stop')
        else:
            self.startFlag = 0
            self.pupilPositionsStack = []
            self.ui.btn_start.setText('Start')
            
            
            
    def runEyetracker(self):
        ''' Starts eyetracker with parameters picked from gui.
        '''
        self.algorithms[ str(self.ui.cmb_setAlgorithm.currentText()) ]()
       
       
       
    def module_raw(self):
        if self.startFlag == 1:
            print 'Pupil coordinates: {}.'.format(self.where_pupil)
            print 'Glint coordinates: {}.'.format(self.where_glint)
        
    def module_music(self):
        if self.musicPlayerFlag == 0 and self.startFlag == 1:
            self.resize(840,640)
            self.musicPlayerFlag = 1
            
            # zbieram self.where_pupil w stos o głębokości pupilStackDeph
            # wyłapuję max i min w każdym kierunku dla tego stosu
            # liczę średnią z ostatnich additional_2 położeń
            # jeśli przekracza alpha*max w danym kierunku to maluję odpowiedni przycisk na zielono
            # jeśli stanie się to additional_3 razy, to podejmuję decyzję
            # jeśli w dwóch próbkach z rzędu nie przekroczy progu, to resetuję
            
        elif self.musicPlayerFlag == 1 and self.startFlag == 0:
            self.resize(640,640)
            self.musicPlayerFlag = 0
        
    def module_text(self):
        if self.textViewerFlag == 0 and self.startFlag == 1:
            self.myTextViever = MyTextViewer()
            self.myTextViever.show()
            self.textViewerFlag = 1
        elif self.textViewerFlag == 1 and self.startFlag == 0:
            self.myTextViever.close()
            self.textViewerFlag = 0
        
    def module_speller(self):
        if self.spellerFlag == 0 and self.startFlag == 1:
            self.resize(1280, 640)
            self.spellerFlag = 1
            self.spellerString  = ''
        elif self.spellerFlag == 1 and self.startFlag == 0:
            self.resize(640,640)
            self.spellerFlag = 0
            
    def keyButtonClicked(self, clickedButtonNo):
        ''' Handles the behavior of the keyboard button.
        #MD k-board
        '''
        
        if self.spellerLvl == 0:
            self.newLabels = ['EASTER EGG hue']

            for buttonNo in range(1,7):
                self.newLabels.append(self.ui.lbls[clickedButtonNo][(buttonNo-1)*2])
                self.ui.keys[buttonNo].setText(self.newLabels[buttonNo])
            self.spellerLvl = 1

        elif self.spellerLvl == 1:
            chosenCharacter = self.newLabels[clickedButtonNo]

            if chosenCharacter == '_':
                self.spellerString += ' '
            elif chosenCharacter == '<':
                self.spellerString = self.spellerString[:-1]
            else:
                self.spellerString += chosenCharacter

            self.resetKeyboard()

        self.ui.lbl_stringWritten.setText(self.spellerString)

    def resetKeyboard(self):
        ''' Resets the keyboard level to 0.
        #MD k-board
        ''' 
        self.spellerLvl = 0
        for buttonNo in range(1,7):
            self.ui.keys[buttonNo].setText(self.ui.lbls[buttonNo])       
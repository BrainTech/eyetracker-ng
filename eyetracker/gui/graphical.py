## #!/usr/bin/env python
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

from PyQt4 import QtCore, QtGui
from platform import system
from os.path import abspath

import eyetracker

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_StartingWindow(object):
    ''' GUI graphical part for the main window.

    Class governing the graphical part of the default graphical user interface.
    It describes only parameters of used widgets, all operational functions
    are placed in separate class in eyetracker/gui/functional.

    '''

    def setupUi(self, StartingWindow):
        ''' Initialization of all needed widgets.

        '''

        StartingWindow.setObjectName(_fromUtf8("StartingWindow"))
        StartingWindow.setEnabled(True)
        StartingWindow.resize(1100, 650)
        StartingWindow.setMinimumSize(QtCore.QSize(1100, 700))
        StartingWindow.setMaximumSize(QtCore.QSize(1100, 700))
        icon = QtGui.QIcon()
        if system() == 'Windows':
            iconPath = abspath(_fromUtf8("pictures/camera.png"))
        else:
            iconPath = _fromUtf8("pictures/camera.svg")
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartingWindow.setWindowIcon(icon)
        
        self.trueScreen = QtGui.QDesktopWidget().screenGeometry()

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))


# GROUPBOXES:
        self.groupBoxCamera = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxCamera.setGeometry(QtCore.QRect(680 , 20 , 400 , 180))
        self.groupBoxCamera.setObjectName(_fromUtf8("groupBoxCamera"))

        self.groupBoxDetection = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxDetection.setGeometry(QtCore.QRect(680 , 220 , 400 , 150))
        self.groupBoxDetection.setObjectName(_fromUtf8("groupBoxDetection"))

        self.groupBoxCalibration = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxCalibration.setGeometry(QtCore.QRect(680 , 390 , 400 , 100))
        self.groupBoxCalibration.setObjectName(_fromUtf8("groupBoxDetection"))

        self.groupBoxApplication = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxApplication.setGeometry(QtCore.QRect(680 , 510 , 400 , 180))
        self.groupBoxApplication.setObjectName(_fromUtf8("groupBoxApplication"))       
        
#GLOBAL LABELS:      
        self.lbl_title = QtGui.QLabel(self.centralwidget)
        self.lbl_title.setEnabled(True)
        self.lbl_title.setGeometry(QtCore.QRect(20, 10, 640, 20))
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setTextFormat(QtCore.Qt.RichText)
        self.lbl_title.setObjectName(_fromUtf8("lbl_title"))

# BUTTONS:
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(510 , 550 , 150 , 30))
        icon1 = QtGui.QIcon()
        if system() == 'Windows':
            iconPath = abspath(_fromUtf8("pictures/start.png"))
        else:
            iconPath = _fromUtf8("pictures/start.svg")
        icon1.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_start.setIcon(icon1)
        self.btn_start.setIconSize(QtCore.QSize(24, 24))
        self.btn_start.setObjectName(_fromUtf8("btn_start"))

#         color = QtGui.QColor(250, 0, 0 )
#         palette = QtGui.QPalette()
#         palette.setColor(QtGui.QPalette.Button, color)
#         self.btn_start.setPalette(palette)
#         self.btn_start.setAutoFillBackground(1)

        self.btn_clear = QtGui.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(180 , 550 , 30 , 30))
        icon5 = QtGui.QIcon()
        if system() == 'Windows':
            iconPath = abspath(_fromUtf8("pictures/clear.png"))
        else:
            iconPath = _fromUtf8("pictures/clear.svg")
        icon5.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear.setIcon(icon5)
        self.btn_clear.setIconSize(QtCore.QSize(24, 24))
        self.btn_clear.setObjectName(_fromUtf8("btn_clear"))

 
        self.btn_save = QtGui.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(20 , 550 , 150 , 30))
        icon4 = QtGui.QIcon()
        if system() == 'Windows':
            iconPath = abspath(_fromUtf8("pictures/save.png"))
        else:
            iconPath = _fromUtf8("pictures/save.svg")
        icon4.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon4)
        self.btn_save.setIconSize(QtCore.QSize(24, 24))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))


# GROUPBOX CAMERA:
        self.lbl_setCamera = QtGui.QLabel(self.groupBoxCamera)
        self.lbl_setCamera.setGeometry(QtCore.QRect(20 , 20 , 180 , 30))
        self.lbl_setCamera.setObjectName(_fromUtf8("lbl_setCamera"))

        self.cmb_setCamera = QtGui.QComboBox(self.groupBoxCamera)
        self.cmb_setCamera.setGeometry(QtCore.QRect(200 , 20 , 180 , 30))
        self.cmb_setCamera.setObjectName(_fromUtf8("cmb_setCamera"))

        self.lbl_setResolution = QtGui.QLabel(self.groupBoxCamera)
        self.lbl_setResolution.setGeometry(QtCore.QRect(20 , 70 , 180 , 30))
        self.lbl_setResolution.setObjectName(_fromUtf8("lbl_setResolution"))

        self.cmb_setResolution = QtGui.QComboBox(self.groupBoxCamera)
        self.cmb_setResolution.setGeometry(QtCore.QRect(200 , 70 , 180 , 30))
        self.cmb_setResolution.setObjectName(_fromUtf8("cmb_setResolution"))

        self.chb_flip = QtGui.QCheckBox(self.groupBoxCamera)
        self.chb_flip.setGeometry(QtCore.QRect(30, 100, 94, 40))
        self.chb_flip.setObjectName(_fromUtf8("chb_flip"))

        self.chb_mirror = QtGui.QCheckBox(self.groupBoxCamera)
        self.chb_mirror.setGeometry(QtCore.QRect(30, 130, 94, 40))
        self.chb_mirror.setObjectName(_fromUtf8("chb_mirror"))


# GROUPBOX DETECTION:

        self.chb_useKalmanFiltration = QtGui.QCheckBox(self.groupBoxDetection)
        self.chb_useKalmanFiltration.setGeometry(QtCore.QRect(30, 10, 140, 40))
        self.chb_useKalmanFiltration.setObjectName(_fromUtf8("chb_useKalmanFiltration"))
        

        self.lbl_pupilDetection = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_pupilDetection.setGeometry(QtCore.QRect(20, 50, 180, 20))
        self.lbl_pupilDetection.setObjectName(_fromUtf8("lbl_pupilDetection"))

        self.hsb_pupil = QtGui.QScrollBar(self.groupBoxDetection)
        self.hsb_pupil.setEnabled(True)
        self.hsb_pupil.setGeometry(QtCore.QRect(200, 50, 150, 15))
        self.hsb_pupil.setMaximum(255)
        self.hsb_pupil.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil.setObjectName(_fromUtf8("hsb_pupil1"))

        self.lbl_pupil = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_pupil.setGeometry(QtCore.QRect(360, 50, 30, 20))
        self.lbl_pupil.setText(_fromUtf8(""))
        self.lbl_pupil.setObjectName(_fromUtf8("lbl_pupil1"))
 
 
#         self.lbl_pupilNumber = QtGui.QLabel(self.groupBoxDetection)
#         self.lbl_pupilNumber.setGeometry(QtCore.QRect(20, 50, 180, 20))
#         self.lbl_pupilNumber.setObjectName(_fromUtf8("lbl_pupilNbumber"))
#  
#         self.hsb_pupil2 = QtGui.QScrollBar(self.groupBoxDetection)
#         self.hsb_pupil2.setEnabled(True)
#         self.hsb_pupil2.setGeometry(QtCore.QRect(200, 50, 150, 15))
#         self.hsb_pupil2.setMaximum(5)
#         self.hsb_pupil2.setOrientation(QtCore.Qt.Horizontal)
#         self.hsb_pupil2.setObjectName(_fromUtf8("hsb_pupil2"))
#  
#         self.lbl_pupil2 = QtGui.QLabel(self.groupBoxDetection)
#         self.lbl_pupil2.setGeometry(QtCore.QRect(360, 50, 30, 20))
#         self.lbl_pupil2.setText(_fromUtf8(""))
#         self.lbl_pupil2.setObjectName(_fromUtf8("lbl_pupil2"))
 
 
        self.lbl_glintDetection = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_glintDetection.setGeometry(QtCore.QRect(20, 80, 180, 20))
        self.lbl_glintDetection.setObjectName(_fromUtf8("lbl_glintDetection"))
 
        self.hsb_glint = QtGui.QScrollBar(self.groupBoxDetection)
        self.hsb_glint.setEnabled(True)
        self.hsb_glint.setGeometry(QtCore.QRect(200, 80, 150, 15))
        self.hsb_glint.setMaximum(5)
        self.hsb_glint.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_glint.setObjectName(_fromUtf8("hsb_glint2"))
 
        self.lbl_glint = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_glint.setGeometry(QtCore.QRect(360, 80, 30, 20))
        self.lbl_glint.setText(_fromUtf8(""))
        self.lbl_glint.setObjectName(_fromUtf8("lbl_glint2"))
 
 
        self.lbl_averaging = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_averaging.setGeometry(QtCore.QRect(20, 110, 180, 20))
        self.lbl_averaging.setObjectName(_fromUtf8("lbl_averaging")) 
 
        self.hsb_averaging = QtGui.QScrollBar(self.groupBoxDetection)
        self.hsb_averaging.setEnabled(True)
        self.hsb_averaging.setGeometry(QtCore.QRect(200, 110, 150, 15))
        self.hsb_averaging.setMinimum(5)
        self.hsb_averaging.setMaximum(15)
        self.hsb_averaging.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_averaging.setObjectName(_fromUtf8("hsb_averaging")) 
 
        self.lbl_averagingN = QtGui.QLabel(self.groupBoxDetection)
        self.lbl_averagingN.setGeometry(QtCore.QRect(360, 110, 30, 20))
        self.lbl_averagingN.setText(_fromUtf8(""))
        self.lbl_averagingN.setObjectName(_fromUtf8("lbl_averagingN")) 
 
# GROUPBOX CALIBRATION: 
        self.lbl_setCalibrationAlgorithm = QtGui.QLabel(self.groupBoxCalibration)
        self.lbl_setCalibrationAlgorithm.setGeometry(QtCore.QRect(20 , 20 , 180 , 30))
        self.lbl_setCalibrationAlgorithm.setObjectName(_fromUtf8("lbl_calibrationAlgorithm"))
        
        self.cmb_setCalibrationAlgorithm = QtGui.QComboBox(self.groupBoxCalibration)
        self.cmb_setCalibrationAlgorithm.setGeometry(QtCore.QRect(200, 20, 180, 30))
        self.cmb_setCalibrationAlgorithm.setObjectName(_fromUtf8("cmb_calibrationAlgorithm"))
 
 
        self.lbl_calibrationSpeed = QtGui.QLabel(self.groupBoxCalibration)
        self.lbl_calibrationSpeed.setGeometry(QtCore.QRect(20,60,180,20))
        self.lbl_calibrationSpeed.setObjectName(_fromUtf8("lbl_calibrationSpeed"))

        self.hsb_calibrationSpeed = QtGui.QScrollBar(self.groupBoxCalibration)
        self.hsb_calibrationSpeed.setEnabled(True)
        self.hsb_calibrationSpeed.setGeometry(QtCore.QRect(200, 60, 150, 15))
        self.hsb_calibrationSpeed.setMinimum(5)
        self.hsb_calibrationSpeed.setMaximum(25)
        self.hsb_calibrationSpeed.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_calibrationSpeed.setObjectName(_fromUtf8("hsb_calibrationSpeed")) 
 
        self.lbl_calibrationSpeedN = QtGui.QLabel(self.groupBoxCalibration)
        self.lbl_calibrationSpeedN.setGeometry(QtCore.QRect(360, 60, 30, 20))
        self.lbl_calibrationSpeedN.setText(_fromUtf8(""))
        self.lbl_calibrationSpeedN.setObjectName(_fromUtf8("lbl_calibrationSpeedN"))           



# GROUPBOX ALGORITHM:
        self.lbl_setApplicationAlgorithm = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_setApplicationAlgorithm.setGeometry(QtCore.QRect(20 , 20 , 180 , 30))
        self.lbl_setApplicationAlgorithm.setObjectName(_fromUtf8("lbl_setApplicationAlgorithm"))
        
        self.cmb_setApplicationAlgorithm = QtGui.QComboBox(self.groupBoxApplication)
        self.cmb_setApplicationAlgorithm.setGeometry(QtCore.QRect(200, 20, 180, 30))
        self.cmb_setApplicationAlgorithm.setObjectName(_fromUtf8("cmb_setApplicationAlgorithm"))        


        self.lbl_applicationSmoothness = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_applicationSmoothness.setGeometry(QtCore.QRect(20,60,180,30))
        self.lbl_applicationSmoothness.setObjectName(_fromUtf8("lbl_applicationSmoothness"))
          
        self.hsb_applicationSmoothness = QtGui.QScrollBar(self.groupBoxApplication)
        self.hsb_applicationSmoothness.setEnabled(True)
        self.hsb_applicationSmoothness.setGeometry(QtCore.QRect(200, 60, 150, 15))
        self.hsb_applicationSmoothness.setMinimum(0)
        self.hsb_applicationSmoothness.setMaximum(100)
        self.hsb_applicationSmoothness.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_applicationSmoothness.setObjectName(_fromUtf8("hsb_applicationSmoothness")) 
 
        self.lbl_applicationSmoothnessN = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_applicationSmoothnessN.setGeometry(QtCore.QRect(360, 60, 30, 20))
        self.lbl_applicationSmoothnessN.setText(_fromUtf8(""))
        self.lbl_applicationSmoothnessN.setObjectName(_fromUtf8("lbl_applicationSmoothnessN"))           



        self.lbl_neswThreshold = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_neswThreshold.setGeometry(QtCore.QRect(20,90,180,30))
        self.lbl_neswThreshold.setObjectName(_fromUtf8("lbl_neswThreshold"))
          
        self.hsb_neswThreshold = QtGui.QScrollBar(self.groupBoxApplication)
        self.hsb_neswThreshold.setEnabled(True)
        self.hsb_neswThreshold.setGeometry(QtCore.QRect(200, 95, 150, 15))
        self.hsb_neswThreshold.setMinimum(1)
        self.hsb_neswThreshold.setMaximum(15)
        self.hsb_neswThreshold.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_neswThreshold.setObjectName(_fromUtf8("hsb_neswThreshold")) 
 
        self.lbl_neswThresholdN = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_neswThresholdN.setGeometry(QtCore.QRect(360, 90, 30, 20))
        self.lbl_neswThresholdN.setText(_fromUtf8(""))
        self.lbl_neswThresholdN.setObjectName(_fromUtf8("lbl_neswThresholdN"))
        
        
        self.lbl_neswQueueLength = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_neswQueueLength.setGeometry(QtCore.QRect(20,120,180,30))
        self.lbl_neswQueueLength.setObjectName(_fromUtf8("lbl_neswQueueLength"))
          
        self.hsb_neswQueueLength = QtGui.QScrollBar(self.groupBoxApplication)
        self.hsb_neswQueueLength.setEnabled(True)
        self.hsb_neswQueueLength.setGeometry(QtCore.QRect(200, 125, 150, 15))
        self.hsb_neswQueueLength.setMinimum(15)
        self.hsb_neswQueueLength.setMaximum(60)
        self.hsb_neswQueueLength.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_neswQueueLength.setObjectName(_fromUtf8("hsb_neswQueueLength")) 
 
        self.lbl_neswQueueLengthN = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_neswQueueLengthN.setGeometry(QtCore.QRect(360, 120, 30, 20))
        self.lbl_neswQueueLengthN.setText(_fromUtf8(""))
        self.lbl_neswQueueLengthN.setObjectName(_fromUtf8("lbl_neswQueueLengthN"))
        

        self.lbl_neswDeadTime = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_neswDeadTime.setGeometry(QtCore.QRect(20,150,180,30))
        self.lbl_neswDeadTime.setObjectName(_fromUtf8("lbl_neswDeadTime"))
          
        self.hsb_neswDeadTime = QtGui.QScrollBar(self.groupBoxApplication)
        self.hsb_neswDeadTime.setEnabled(True)
        self.hsb_neswDeadTime.setGeometry(QtCore.QRect(200,155,150,15))
        self.hsb_neswDeadTime.setMinimum(30)
        self.hsb_neswDeadTime.setMaximum(90)
        self.hsb_neswDeadTime.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_neswDeadTime.setObjectName(_fromUtf8("hsb_neswDeadTime")) 
 
        self.lbl_neswDeadTimeN = QtGui.QLabel(self.groupBoxApplication)
        self.lbl_neswDeadTimeN.setGeometry(QtCore.QRect(360, 150, 30, 20))
        self.lbl_neswDeadTimeN.setText(_fromUtf8(""))
        self.lbl_neswDeadTimeN.setObjectName(_fromUtf8("lbl_neswDeadTimeN"))
        
# MISCELLOUS:            
        self.timer = QtCore.QBasicTimer()


# SET ALL THINGS UP:
        StartingWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        '''Attach names to all widgets set up in setupUi function.
        '''

        StartingWindow.setWindowTitle(_translate("StartingWindow", "Eyetracker -- start" + eyetracker.version, None))
        
        self.lbl_title.setText(_translate("StartingWindow", "Eyetracker " + eyetracker.version, None))
        self.lbl_pupilDetection.setText(_translate("StartingWindow", "Pupil detection threshold:", None))
        #self.lbl_useKalmanFiltration.setText(_translate("StartingWindow", "Pupil detection algorithm:", None))
        self.lbl_glintDetection.setText(_translate("StartingWindow", "Number of glints to track:", None))
        self.lbl_averaging.setText(_translate("StartingWindow", "Smoothing via averaging:", None))
        self.lbl_setCalibrationAlgorithm.setText(_translate("StartingWindow", "Calibration type:", None))
        self.lbl_calibrationSpeed.setText(_translate("StartingWindow", "Calibration speed:", None))
        self.lbl_setApplicationAlgorithm.setText(_translate("StartingWindow", "Application to run:", None))
        self.lbl_applicationSmoothness.setText(_translate("StartingWindow", "Cursor app smoothing:", None))
        self.lbl_setCamera.setText(_translate("StartingWindow", "Choose camera:", None))
        self.lbl_setResolution.setText(_translate("StartingWindow", "Choose resolution:", None))
        self.lbl_neswThreshold.setText(_translate("StartingWindow", "NESW threshold:", None))
        self.lbl_neswQueueLength.setText(_translate("StartingWindow", "NESW decision queue:", None))
        self.lbl_neswDeadTime.setText(_translate("StartingWindow", "NESW dead time:", None))
        
        self.chb_flip.setText(_translate("StartingWindow", "Flip", None))
        self.chb_mirror.setText(_translate("StartingWindow", "Mirror", None))
        self.chb_useKalmanFiltration.setText(_translate("StartingWindow", "Use Kalman filtration", None))
        
        self.btn_start.setText(_translate("StartingWindow", "START", None))
        self.btn_save.setText(_translate("StartingWindow", "SAVE", None))
        
        self.groupBoxCamera.setTitle(_translate("MainWindow", "Camera settings", None))
        self.groupBoxDetection.setTitle(_translate("MainWindow", "Detection settings", None))
        self.groupBoxCalibration.setTitle(_translate("MainWindow", "Calibration settings", None))
        self.groupBoxApplication.setTitle(_translate("MainWindow", "Application settings", None))



###################################################################################################################################################

class Ui_CursorCalibrationWindow(object):
    ''' GUI graphical part for the cursor calibration window.

    Class governing the graphical part of the cursor calibration graphical
    user interface. It describes only parameters of used widgets, all
    operational functions are placed in separate class in eyetracker/gui/functional.

    '''

    def setupUi(self, StartingWindow):
        ''' Initialization of all needed widgets.

        '''

        StartingWindow.setObjectName(_fromUtf8("CursorCalibrationWindow"))
        StartingWindow.setEnabled(True)
        #StartingWindow.resize(1100, 700)
        #StartingWindow.setMinimumSize(QtCore.QSize(1100, 700))
        #StartingWindow.setMaximumSize(QtCore.QSize(1100, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/camera.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartingWindow.setWindowIcon(icon)
        
        self.trueScreen = QtGui.QDesktopWidget().screenGeometry()
        #print trueScreen.width(), trueScreen.height()

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))        


# MISCELLOUS:            
        self.timer = QtCore.QBasicTimer()


# SET ALL THINGS UP:
        StartingWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        '''Attach names to all widgets set up in setupUi function.
        '''

        StartingWindow.setWindowTitle(_translate("CursorCalibrationWindow", "Eyetracker -- cursor calibration" + eyetracker.version, None))




###################################################################################################################################################

class Ui_NeswCalibrationWindow(object):
    ''' GUI graphical part for the NESW calibration window.

    Class governing the graphical part of the NESW calibration graphical
    user interface. It describes only parameters of used widgets, all
    operational functions are placed in separate class in eyetracker/gui/functional.

    '''

    def setupUi(self, StartingWindow):
        ''' Initialization of all needed widgets.

        '''

        StartingWindow.setObjectName(_fromUtf8("NeswCalibrationWindow"))
        StartingWindow.setEnabled(True)
        #StartingWindow.resize(1100, 700)
        #StartingWindow.setMinimumSize(QtCore.QSize(1100, 700))
        #StartingWindow.setMaximumSize(QtCore.QSize(1100, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/camera.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartingWindow.setWindowIcon(icon)
        
        self.trueScreen = QtGui.QDesktopWidget().screenGeometry()
        #print trueScreen.width(), trueScreen.height()

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))        


# MISCELLOUS:            
        self.timer = QtCore.QBasicTimer()


# SET ALL THINGS UP:
        StartingWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        '''Attach names to all widgets set up in setupUi function.
        '''

        StartingWindow.setWindowTitle(_translate("NeswCalibrationWindow", "Eyetracker -- NESW calibration" + eyetracker.version, None))

###################################################################################################################################################

class Ui_NeswSpellerWindow(object):
    ''' GUI graphical part for the NESW speller window.

    Class governing the graphical part of the NESW speller graphical
    user interface. It describes only parameters of used widgets, all
    operational functions are placed in separate class in eyetracker/gui/functional.

    '''

    def setupUi(self, StartingWindow , btn_labels):
        ''' Initialization of all needed widgets.

        '''

        StartingWindow.setObjectName(_fromUtf8("NeswSpellerWindow"))
        StartingWindow.setEnabled(True)
        #StartingWindow.resize(1100, 700)
        #StartingWindow.setMinimumSize(QtCore.QSize(1100, 700))
        #StartingWindow.setMaximumSize(QtCore.QSize(1100, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/camera.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartingWindow.setWindowIcon(icon)
        
        self.trueScreen = QtGui.QDesktopWidget().screenGeometry()
        #print trueScreen.width(), trueScreen.height()

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))        

# BUTTONS:
        font = QtGui.QFont()
        #font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setPointSize(25)
        

        self.btn_1 = QtGui.QPushButton(self.centralwidget)
        self.btn_1.setGeometry(QtCore.QRect(10 , 10 , self.trueScreen.width()/5. , self.trueScreen.height()/5.))
        self.btn_1.setFont(font)
        #self.btn_1.setStyleSheet("background-color: gray")
        self.btn_1.setObjectName(_fromUtf8("btn_1"))

        self.btn_2 = QtGui.QPushButton(self.centralwidget)
        self.btn_2.setGeometry(QtCore.QRect(10 , 2*self.trueScreen.height()/5.-20 , self.trueScreen.width()/5. , self.trueScreen.height()/5.))
        self.btn_2.setFont(font)
        #self.btn_2.setStyleSheet("background-color: gray")
        self.btn_2.setObjectName(_fromUtf8("btn_2"))
        
        self.btn_3 = QtGui.QPushButton(self.centralwidget)
        self.btn_3.setGeometry(QtCore.QRect(10 , 4*self.trueScreen.height()/5.-60 , self.trueScreen.width()/5. , self.trueScreen.height()/5.))
        self.btn_3.setFont(font)
        #self.btn_3.setStyleSheet("background-color: gray")
        self.btn_3.setObjectName(_fromUtf8("btn_3"))
        
        self.btn_4 = QtGui.QPushButton(self.centralwidget)
        self.btn_4.setGeometry(QtCore.QRect(4*self.trueScreen.width()/5.-10 , 10 , self.trueScreen.width()/5. , self.trueScreen.height()/5.))
        self.btn_4.setFont(font)
        #self.btn_4.setStyleSheet("background-color: gray")
        self.btn_4.setObjectName(_fromUtf8("btn_4"))
        
        self.btn_5 = QtGui.QPushButton(self.centralwidget)
        self.btn_5.setGeometry(QtCore.QRect(4*self.trueScreen.width()/5.-10 , 2*self.trueScreen.height()/5.-20 , self.trueScreen.width()/5. , self.trueScreen.height()/5.))
        self.btn_5.setFont(font)
        #self.btn_5.setStyleSheet("background-color: gray")
        self.btn_5.setObjectName(_fromUtf8("btn_5"))
        
        self.btn_6 = QtGui.QPushButton(self.centralwidget)
        self.btn_6.setGeometry(QtCore.QRect(4*self.trueScreen.width()/5.-10 , 4*self.trueScreen.height()/5.-60 , self.trueScreen.width()/5. , self.trueScreen.height()/5.))
        self.btn_6.setFont(font)
        #self.btn_6.setStyleSheet("background-color: gray")
        self.btn_6.setObjectName(_fromUtf8("btn_6"))
        
        self.btn_7 = QtGui.QPushButton(self.centralwidget)
        self.btn_7.setGeometry(QtCore.QRect(2*self.trueScreen.width()/5.-20 , 10 , self.trueScreen.width()/4. , self.trueScreen.height()/5.))
        self.btn_7.setFont(font)
        #self.btn_7.setStyleSheet("background-color: gray")
        self.btn_7.setObjectName(_fromUtf8("btn_7"))
        
        self.btn_8 = QtGui.QPushButton(self.centralwidget)
        self.btn_8.setGeometry(QtCore.QRect(2*self.trueScreen.width()/5.-20 , 4*self.trueScreen.height()/5.-60 , self.trueScreen.width()/4. , self.trueScreen.height()/5.))
        self.btn_8.setFont(font)
        #self.btn_8.setStyleSheet("background-color: gray")
        self.btn_8.setObjectName(_fromUtf8("btn_8"))

#GLOBAL TEXT EDIT:      
        #self.ted_text = QtGui.QTextEdit(self.centralwidget)
        self.ted_text = QtGui.QLabel(self.centralwidget)
        self.ted_text.setEnabled(True)
        self.ted_text.setGeometry(QtCore.QRect(self.trueScreen.width()/3., self.trueScreen.height()/3., self.trueScreen.width()/3., self.trueScreen.height()/3.))
        #self.ted_text.setAlignment(QtCore.Qt.AlignCenter)
        font2 = QtGui.QFont()
        font2.setBold(True)
        font2.setItalic(True)
        font2.setWeight(75)
        font2.setPointSize(15)
        self.ted_text.setFont(font2)
        #self.ted_text.setTextFormat(QtCore.Qt.RichText)
        self.ted_text.setObjectName(_fromUtf8("ted_text"))

# MISCELLOUS:            
        self.timer = QtCore.QBasicTimer()

# SET ALL THINGS UP:
        StartingWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(StartingWindow , btn_labels)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow , btn_labels):
        '''Attach names to all widgets set up in setupUi function.
        '''

        StartingWindow.setWindowTitle(_translate("NeswSpellerWindow", "Eyetracker -- NESW speller" + eyetracker.version, None))
#         self.btn_1.setText(_translate("btn_1", "A Ä„ B C Ä† D", None))
#         self.btn_2.setText(_translate("btn_2", "E Ä� F G H I", None))
#         self.btn_3.setText(_translate("btn_3", "J K L Ĺ� M N", None))
#         self.btn_4.setText(_translate("btn_4", "Ĺ� O Ă“ P R Q", None))
#         self.btn_5.setText(_translate("btn_5", "S Ĺš T U W V", None))
#         self.btn_6.setText(_translate("btn_6", "X Y Z Ĺ» Ĺą ~", None))
        
        self.btn_1.setText(_translate("btn_1", btn_labels[0], None))
        self.btn_2.setText(_translate("btn_2", btn_labels[1], None))
        self.btn_3.setText(_translate("btn_3", btn_labels[2], None))
        self.btn_4.setText(_translate("btn_4", btn_labels[3], None))
        self.btn_5.setText(_translate("btn_5", btn_labels[4], None))
        self.btn_6.setText(_translate("btn_6", btn_labels[5], None))
        
        self.btn_7.setText(_translate("btn_7", "DELETE", None))
        self.btn_8.setText(_translate("btn_8", "SPACE", None))
###################################################################################################################################################


if __name__ == '__main__':
    print 'Using this class without it\'s functional part may be possible, but'
    print 'it would be completely useless.'

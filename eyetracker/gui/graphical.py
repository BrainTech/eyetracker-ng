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


class Ui_MusicPlayerWindow(object):
    ''' GUI graphical part for a simple music player.

    Class governing the graphical part of the graphical user interface.
    It describes only parameters of used widgets, all operational functions
    are placed in separate class in eyetracker/gui/functional.

    '''
    def setupUi(self , MusicPlayerWindow):
        ''' Initialization of all needed widgets.

        '''
        trueScreen = QtGui.QDesktopWidget().screenGeometry()
        #print screen.width(), screen.height()
        screen_width  = 1000
        screen_height = 700
        
        MusicPlayerWindow.setObjectName(_fromUtf8("MusicPlayerWindow"))
        MusicPlayerWindow.setEnabled(True)
        MusicPlayerWindow.setGeometry( (trueScreen.width() - screen_width)/2.0 , (trueScreen.height() - screen_height)/2.0, screen_width, screen_height)
        #MusicPlayerWindow.setMinimumSize(QtCore.QSize(200, 200))
        #MusicPlayerWindow.setMaximumSize(QtCore.QSize(200, 200))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/camera.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MusicPlayerWindow.setWindowIcon(icon)

        self.centralwidget = QtGui.QWidget(MusicPlayerWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        text_size_width  = 800
        text_size_height = 500


        self.lbl_text = QtGui.QLabel(self.centralwidget)
        self.lbl_text.setEnabled(True)
        pos_x  = (screen_width - text_size_width) / 2.0
        pos_y  = (screen_height- text_size_height) / 2.0
        self.lbl_text.setGeometry(QtCore.QRect(pos_x, pos_y, text_size_width, text_size_height))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(75)
        self.lbl_text.setFont(font)
        self.lbl_text.setTextFormat(QtCore.Qt.RichText)
        self.lbl_text.setObjectName(_fromUtf8("lbl_text"))
        

        self.btn_right = QtGui.QPushButton(self.centralwidget)
        size_x = (screen_width - text_size_width) / 2.0
        pos_x  = screen_width- size_x
        size_y = text_size_height
        pos_y  = (screen_height- text_size_height) / 2.0
        self.btn_right.setGeometry(QtCore.QRect(pos_x, pos_y, size_x, size_y))
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/start.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.btn_right.setIcon(icon1)
        self.btn_right.setObjectName(_fromUtf8("btn_right"))


        self.btn_left = QtGui.QPushButton(self.centralwidget)
        size_x = (screen_width - text_size_width) / 2.0
        pos_x  = 0.0
        size_y = text_size_height
        pos_y  = (screen_height- text_size_height) / 2.0
        self.btn_left.setGeometry(QtCore.QRect(pos_x, pos_y, size_x, size_y))
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/start.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.btn_right.setIcon(icon1)
        self.btn_left.setObjectName(_fromUtf8("btn_left"))


        self.btn_up = QtGui.QPushButton(self.centralwidget)
        size_x = text_size_width
        pos_x  = (screen_width - text_size_width) / 2.0
        size_y = (screen_height - text_size_height) / 2.0 
        pos_y  = 0.0
        self.btn_up.setGeometry(QtCore.QRect(pos_x, pos_y, size_x, size_y))
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/start.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.btn_right.setIcon(icon1)
        self.btn_up.setObjectName(_fromUtf8("btn_up"))



        self.btn_down = QtGui.QPushButton(self.centralwidget)
        size_x = text_size_width
        pos_x  = (screen_width - text_size_width) / 2.0
        size_y = (screen_height - text_size_height) / 2.0 
        pos_y  = (screen_height + text_size_height) / 2.0
        self.btn_down.setGeometry(QtCore.QRect(pos_x, pos_y, size_x, size_y))
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/start.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.btn_right.setIcon(icon1)
        self.btn_down.setObjectName(_fromUtf8("btn_down"))        
        

        MusicPlayerWindow.setCentralWidget(self.centralwidget)
        #self.statusbar = QtGui.QStatusBar(MusicPlayerWindow)
        #self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #MusicPlayerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MusicPlayerWindow)
        QtCore.QMetaObject.connectSlotsByName(MusicPlayerWindow)


        
    def retranslateUi(self, MusicPlayerWindow):
        '''Attach names to all widgets set up in setupUi function.
        '''

        MusicPlayerWindow.setWindowTitle(_translate("MusicPlayerWindow", "Eyetracter -- start", None))
        self.lbl_text.setText(_translate("MusicPlayerWindow", "siofoihasfoawiuhyefąąąąąąą", None))







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
        StartingWindow.resize(640, 640)
        StartingWindow.setMinimumSize(QtCore.QSize(640, 640))
        #StartingWindow.setMaximumSize(QtCore.QSize(640, 640))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/camera.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StartingWindow.setWindowIcon(icon)

        self.centralwidget = QtGui.QWidget(StartingWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.lbl_title = QtGui.QLabel(self.centralwidget)
        self.lbl_title.setEnabled(True)
        self.lbl_title.setGeometry(QtCore.QRect(100, 10, StartingWindow.width(), 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setTextFormat(QtCore.Qt.RichText)
        self.lbl_title.setObjectName(_fromUtf8("lbl_title"))

        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(150, 560, 160, 35))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/start.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_start.setIcon(icon1)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))

        self.lbl_setCamera = QtGui.QLabel(self.centralwidget)
        self.lbl_setCamera.setGeometry(QtCore.QRect(360, 40, 160, 20))
        self.lbl_setCamera.setObjectName(_fromUtf8("lbl_setCamera"))

        self.lbl_setResolution = QtGui.QLabel(self.centralwidget)
        self.lbl_setResolution.setGeometry(QtCore.QRect(360, 110, 160, 20))
        self.lbl_setResolution.setObjectName(_fromUtf8("lbl_setResolution"))

        self.cmb_setCamera = QtGui.QComboBox(self.centralwidget)
        self.cmb_setCamera.setGeometry(QtCore.QRect(360, 70, 160, 30))
        self.cmb_setCamera.setObjectName(_fromUtf8("cmb_setCamera"))

        self.cmb_setResolution = QtGui.QComboBox(self.centralwidget)
        self.cmb_setResolution.setGeometry(QtCore.QRect(360, 140, 160, 30))
        self.cmb_setResolution.setObjectName(_fromUtf8("cmb_setResolution"))

        self.chb_flip = QtGui.QCheckBox(self.centralwidget)
        self.chb_flip.setGeometry(QtCore.QRect(360, 180, 94, 20))
        self.chb_flip.setObjectName(_fromUtf8("chb_flip"))

        self.chb_mirror = QtGui.QCheckBox(self.centralwidget)
        self.chb_mirror.setGeometry(QtCore.QRect(360, 205, 94, 20))
        self.chb_mirror.setObjectName(_fromUtf8("chb_mirror"))

        self.lbl_pupilDetection = QtGui.QLabel(self.centralwidget)
        self.lbl_pupilDetection.setGeometry(QtCore.QRect(360, 250, 160, 20))
        self.lbl_pupilDetection.setObjectName(_fromUtf8("lbl_pupilDetection"))

        self.hsb_pupil = QtGui.QScrollBar(self.centralwidget)
        self.hsb_pupil.setEnabled(True)
        self.hsb_pupil.setGeometry(QtCore.QRect(360, 280, 160, 16))
        self.hsb_pupil.setMaximum(255)
        self.hsb_pupil.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil.setObjectName(_fromUtf8("hsb_pupil1"))

        self.lbl_pupil = QtGui.QLabel(self.centralwidget)
        self.lbl_pupil.setGeometry(QtCore.QRect(530, 280, 50, 16))
        self.lbl_pupil.setText(_fromUtf8(""))
        self.lbl_pupil.setObjectName(_fromUtf8("lbl_pupil1"))

        self.lbl_pupilNumber = QtGui.QLabel(self.centralwidget)
        self.lbl_pupilNumber.setGeometry(QtCore.QRect(360, 310, 250, 20))
        self.lbl_pupilNumber.setObjectName(_fromUtf8("lbl_pupilNbumber"))

        self.hsb_pupil2 = QtGui.QScrollBar(self.centralwidget)
        self.hsb_pupil2.setEnabled(True)
        self.hsb_pupil2.setGeometry(QtCore.QRect(360, 340, 160, 16))
        self.hsb_pupil2.setMaximum(5)
        self.hsb_pupil2.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_pupil2.setObjectName(_fromUtf8("hsb_pupil2"))

        self.lbl_pupil2 = QtGui.QLabel(self.centralwidget)
        self.lbl_pupil2.setGeometry(QtCore.QRect(530, 340, 50, 16))
        self.lbl_pupil2.setText(_fromUtf8(""))
        self.lbl_pupil2.setObjectName(_fromUtf8("lbl_pupil2"))

        self.lbl_glintDetection = QtGui.QLabel(self.centralwidget)
        self.lbl_glintDetection.setGeometry(QtCore.QRect(360, 370, 250, 20))
        self.lbl_glintDetection.setObjectName(_fromUtf8("lbl_glintDetection"))

        self.hsb_glint = QtGui.QScrollBar(self.centralwidget)
        self.hsb_glint.setEnabled(True)
        self.hsb_glint.setGeometry(QtCore.QRect(360, 410, 160, 16))
        self.hsb_glint.setMaximum(5)
        self.hsb_glint.setOrientation(QtCore.Qt.Horizontal)
        self.hsb_glint.setObjectName(_fromUtf8("hsb_glint2"))

        self.lbl_glint = QtGui.QLabel(self.centralwidget)
        self.lbl_glint.setGeometry(QtCore.QRect(530, 410, 50, 16))
        self.lbl_glint.setText(_fromUtf8(""))
        self.lbl_glint.setObjectName(_fromUtf8("lbl_glint2"))

        self.lbl_alpha = QtGui.QLabel(self.centralwidget)
        self.lbl_alpha.setGeometry(QtCore.QRect(360, 440, 140, 16))
        self.lbl_alpha.setObjectName(_fromUtf8("lbl_alpha"))
        
        self.led_alpha = QtGui.QLineEdit(self.centralwidget)
        self.led_alpha.setGeometry(QtCore.QRect(500, 440, 50, 20))
        self.led_alpha.setObjectName(_fromUtf8("led_alpha"))
        
        self.lbl_pupilStackDeph = QtGui.QLabel(self.centralwidget)
        self.lbl_pupilStackDeph.setGeometry(QtCore.QRect(360, 470, 140, 16))
        self.lbl_pupilStackDeph.setObjectName(_fromUtf8("lbl_pupilStackDeph"))
        
        self.led_pupilStackDeph = QtGui.QLineEdit(self.centralwidget)
        self.led_pupilStackDeph.setGeometry(QtCore.QRect(500, 470, 50, 20))
        self.led_pupilStackDeph.setObjectName(_fromUtf8("led_pupilStackDeph"))

        self.lbl_decisionStackDeph = QtGui.QLabel(self.centralwidget)
        self.lbl_decisionStackDeph.setGeometry(QtCore.QRect(360, 500, 140, 16))
        self.lbl_decisionStackDeph.setObjectName(_fromUtf8("lbl_decisionStackDeph"))
        
        self.led_decisionStackDeph = QtGui.QLineEdit(self.centralwidget)
        self.led_decisionStackDeph.setGeometry(QtCore.QRect(500, 500, 50, 20))
        self.led_decisionStackDeph.setObjectName(_fromUtf8("led_decisionStackDeph"))

        self.cmb_setAlgorithm = QtGui.QComboBox(self.centralwidget)
        self.cmb_setAlgorithm.setGeometry(QtCore.QRect(20, 560, 120, 35))
        self.cmb_setAlgorithm.setObjectName(_fromUtf8("cmb_setAlgorithm"))

        #self.btn_load = QtGui.QPushButton(self.centralwidget)
        #self.btn_load.setGeometry(QtCore.QRect(500, 510, 120, 35))
        #icon3 = QtGui.QIcon()
        #icon3.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/load.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.btn_load.setIcon(icon3)
        #self.btn_load.setIconSize(QtCore.QSize(24, 24))
        #self.btn_load.setObjectName(_fromUtf8("btn_load"))

        self.btn_clear = QtGui.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(455, 560, 35, 35))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/clear.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear.setIcon(icon5)
        self.btn_clear.setIconSize(QtCore.QSize(24, 24))
        self.btn_clear.setObjectName(_fromUtf8("btn_clear"))

        self.btn_save = QtGui.QPushButton(self.centralwidget)
        self.btn_save.setGeometry(QtCore.QRect(500, 560, 120, 35))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("pictures/save.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon4)
        self.btn_save.setIconSize(QtCore.QSize(24, 24))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))

        ### --- ###
        self.btn_key1 = QtGui.QPushButton(self.centralwidget)
        self.btn_key1.setGeometry(QtCore.QRect(770, 50, 150, 150))
        self.btn_key1.setIconSize(QtCore.QSize(24,24))
        self.btn_key1.setObjectName(_fromUtf8("btn_key1"))

        self.btn_key2 = QtGui.QPushButton(self.centralwidget)
        self.btn_key2.setGeometry(QtCore.QRect(970, 50, 150, 150))
        self.btn_key2.setIconSize(QtCore.QSize(24,24))
        self.btn_key2.setObjectName(_fromUtf8("btn_key2"))

        self.btn_key3 = QtGui.QPushButton(self.centralwidget)
        self.btn_key3.setGeometry(QtCore.QRect(670, 230, 150, 150))
        self.btn_key3.setIconSize(QtCore.QSize(24,24))
        self.btn_key3.setObjectName(_fromUtf8("btn_key3"))

        self.btn_key4 = QtGui.QPushButton(self.centralwidget)
        self.btn_key4.setGeometry(QtCore.QRect(1070, 230, 150, 150))
        self.btn_key4.setIconSize(QtCore.QSize(24,24))
        self.btn_key4.setObjectName(_fromUtf8("btn_key4"))

        self.btn_key5 = QtGui.QPushButton(self.centralwidget)
        self.btn_key5.setGeometry(QtCore.QRect(770, 400, 150, 150))
        self.btn_key5.setIconSize(QtCore.QSize(24,24))
        self.btn_key5.setObjectName(_fromUtf8("btn_key5"))

        self.btn_key6 = QtGui.QPushButton(self.centralwidget)
        self.btn_key6.setGeometry(QtCore.QRect(970, 400, 150, 150))
        self.btn_key6.setIconSize(QtCore.QSize(24,24))
        self.btn_key6.setObjectName(_fromUtf8("btn_key6"))

        #MD string
        self.lbl_stringTitle = QtGui.QLabel(self.centralwidget)
        self.lbl_stringTitle.setGeometry(QtCore.QRect(907, 220, 100, 20))
        self.lbl_stringTitle.setObjectName(_fromUtf8("lbl_stringTitle"))

        self.lbl_stringWritten = QtGui.QLabel(self.centralwidget)
        self.lbl_stringWritten.setGeometry(QtCore.QRect(870, 230, 100, 100))
        self.lbl_stringWritten.setObjectName(_fromUtf8("lbl_stringTitle"))
        ### --- ###


        self.timer = QtCore.QBasicTimer()

        StartingWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(StartingWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        StartingWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartingWindow)
        QtCore.QMetaObject.connectSlotsByName(StartingWindow)

    def retranslateUi(self, StartingWindow):
        '''Attach names to all widgets set up in setupUi function.
        '''

        StartingWindow.setWindowTitle(_translate("StartingWindow", "Eyetracter -- start", None))
        self.lbl_title.setText(_translate("StartingWindow", "Eyetracker "+eyetracker.version, None))
        self.btn_start.setText(_translate("StartingWindow", "START", None))
        self.lbl_setCamera.setText(_translate("StartingWindow", "Choose camera:", None))
        self.lbl_setResolution.setText(_translate("StartingWindow", "Choose resolution:", None))
        self.chb_flip.setText(_translate("StartingWindow", "Flip", None))
        self.chb_mirror.setText(_translate("StartingWindow", "Mirror", None))
        self.lbl_pupilDetection.setText(_translate("StartingWindow", "Pupil detection:", None))
        self.lbl_pupilNumber.setText(_translate("StartingWindow", "Number of pupils to track:", None))
        self.lbl_glintDetection.setText(_translate("StartingWindow", "Number of glints to track:", None))
        self.lbl_alpha.setText(_translate("StartingWindow", "Alpha threshold:", None))
        self.lbl_pupilStackDeph.setText(_translate("StartingWindow", "PupilStackDeph:", None))
        self.lbl_decisionStackDeph.setText(_translate("StartingWindow", "DecisionStackDeph:", None))
        #self.btn_load.setText(_translate("StartingWindow", "LOAD", None))
        self.btn_save.setText(_translate("StartingWindow", "SAVE", None))
        
        self.lbls = {
        1: "A B C D E F",
        2: "G H I J K L",
        3: "M N O P R S",
        4: "T U W X Y Z",
        5: "0 1 2 3 4 5",
        6: "6 7 8 9 _ <"}
        self.keys = {
        1: self.btn_key1,
        2: self.btn_key2,
        3: self.btn_key3,
        4: self.btn_key4,
        5: self.btn_key5,
        6: self.btn_key6}
        for keyNo in range(1,7):
            self.keys[keyNo].setText(_translate("StartingWindow", self.lbls[keyNo], None))
        #MD string
        self.lbl_stringTitle.setText(_translate("StartingWindow", "Pisany tekst:", None))
        self.lbl_stringWritten.setText(_translate("StartingWindow", "", None))

if __name__ == '__main__':
    print 'Using this class without it\'s functional part may be possible, but'
    print 'it would be completely useless.'

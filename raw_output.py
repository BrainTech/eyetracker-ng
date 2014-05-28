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

import sys

#from analysis.processing import imageFlipMirror, runningAverage

#from camera.display import drawPupil, drawGlint
#from camera.capture import lookForCameras
#from camera.camera import Camera


if __name__ == '__main__':
    
    config = {}
    flag   = 'key'
    tmp    = ''
    
    for arg in sys.argv:
        if arg == 'raw_output.py':
            pass
        else:
            if flag == 'key':
                config[arg] = 0
                tmp         = arg
                flag        = 'arg'
            else:
                config[tmp] = arg
                flag        = 'key'
            
    print config
    
    ###
    while(True):
        ret, frame = cap.read()
        
        frame_gray = bgr2gray(frame)
        
        thresh = cv2.getTrackbarPos('threshold', 'camera')
        
        frame_thresh = threshold(frame_gray, thresh_v=thresh)

        where_pupil = pupil(frame_thresh, param2=20, minRadius=20)


        if cv2.waitKey(1) & 0xFF == ord('q') or len(middles) == 1000:
            break
    ###

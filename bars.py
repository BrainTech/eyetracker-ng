import numpy as np
import cv2
from camera import Camera
from matplotlib import pyplot as plt
from eyetracker.analysis.processing import threshold, gray2bgr, bgr2gray, mark
from eyetracker.analysis.detect import glint, pupil

plt.ion()

def nothing(x):
    pass

cam = Camera(1)

cv2.namedWindow("Eyetracking")

cv2.createTrackbar("Threshold", "Eyetracking", 0, 255, nothing)

plt.xlim([0,256])
plt.legend(('cdf', 'histogram'), loc='upper left')	

#color = ('b','g','r')

while True:

    plt.cla()

    track_pos = cv2.getTrackbarPos("Threshold", "Eyetracking")
    
    frame = cam.get_frame()

    gray_frame = bgr2gray(frame)
    
    bw_frame = threshold(gray_frame, track_pos)

    where_glint = glint(gray_frame)

    where_pupil = pupil(bw_frame)

    bw_color_frame = gray2bgr(bw_frame)

    mark(bw_color_frame, where_glint)

    mark(bw_color_frame, where_pupil, color='blue')
    
    effect_frame = np.concatenate((frame, bw_color_frame), axis=1)

    #for i,col in enumerate(color):
    hist = cv2.calcHist([gray_frame], [0], None, [256], [0,256])
    plt.plot(hist)#, color=col)
    plt.xlim([0,256])
    plt.title('Histogram of the Image')
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()
    plt.plot(cdf_normalized)#, color=col)

    plt.draw()
    
    cv2.imshow("Eyetracking", effect_frame)
    key = cv2.waitKey(10) & 0xFF
    if key == 27 or key == ord('q'):
        break

cam.close()
cv2.destroyAllWindows()

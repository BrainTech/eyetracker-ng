import eyetracker.camera.camera as camera
import eyetracker.camera.display as display
from eyetracker.analysis.detect import glint, pupil
from eyetracker.analysis.processing import gray2bgr, bgr2gray, mark, threshold, thresholds
import cv2
import numpy as np

def chainpupil(frame):
    """
    From given thresholded frame returns candidates for pupil.
    Chain of operations occures: gaussian filtering, erosion, flating,
    dilation. After that circles are matched to remaining objects on
    picture.
    """
    kernel = np.ones((5,5),np.uint8)
    blur = cv2.GaussianBlur(frame,(15,15),0)
    framer = cv2.erode(blur,kernel,iterations = 1)
    framer[framer>0]=255
    framer = cv2.dilate(framer,kernel,iterations = 6)
    framtnt = np.copy(framer)
    contours,hierarchy = cv2.findContours(framtnt, 1, 2)
    all_circles = []
    for i in xrange(len(contours)):
        cnt = contours[i]
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        if radius < frame.shape[0]//2 and radius < frame.shape[1]//2:
            all_circles.append([int(x), int(y), int(radius)])
    if len(all_circles)>0:
        all_circles = np.array(all_circles)
    else:
        all_circles = None 
    return all_circles

def nothing(x):
    pass

cam_id = camera.lookForCameras()
cams = cam_id.keys()
cam = camera.Camera(cam_id['Camera_2'])
cam_nr = 0
window = 'decide on the name'

cv2.namedWindow(window)
cv2.namedWindow('choose your camera')
cv2.createTrackbar('threshold value', window, 0, 255, nothing)
cv2.createTrackbar('threshold type', window, 0, 5, nothing)

key = 0

while key != ord('y'):
    frame = cam.frame()
    key = display.displayImage(frame, 'choose your camera')
    if key == ord('>'):
        cam_nr += 1
        cam.close()
        cam = camera.Camera(cam_id[cams[cam_nr % len(cams)]])

cv2.destroyWindow('choose your camera')

threshold_types = thresholds.keys()

print 'Indexes corresponding to threshold types:'
for i, v in enumerate(threshold_types):
    print i, ':', v

kernel = np.ones((5,5),np.uint8)

while True:
    thresh_v = cv2.getTrackbarPos('threshold value', window)
    thresh_t = int(cv2.getTrackbarPos('threshold type', window))

    frame = cam.frame()

    frame_gray = bgr2gray(frame)

    frame_thresh = threshold(frame_gray, thresh_v, 
                             thresh_type=threshold_types[thresh_t])
    
    where_glint = glint(frame_gray)

    where_pupil = chainpupil(frame_thresh)
    
    ''' your code '''

    mark(frame, where_glint)

    mark(frame, where_pupil,color='blue')
    
    frame_bgr = gray2bgr(frame_thresh)

    # wizualizacja tego co sie w chainpupil
    blur = cv2.GaussianBlur(frame_thresh,(15,15),0)
    framer = cv2.erode(blur,kernel,iterations = 1)
    framer[framer>0]=255
    framer = cv2.dilate(framer,kernel,iterations = 6)
    framer = gray2bgr(framer)
    new_image = np.hstack((frame, framer))

    ''' end of your code'''

    ''' press q or ESC to quit'''

    key = display.displayImage(new_image, where=window)
    if key == 27 or key == ord('q'):
        break
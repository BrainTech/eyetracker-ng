import eyetracker
import cv2

cam_id = eyetracker.camera.camera.lookForCameras()

cam = eyetracker.camera.camera.Camera(cam_id['Camera_1'])

while True:
    frame = cam.frame()
    
## you'r code ##






    eyetracker.camera.display.displayImage(frame)
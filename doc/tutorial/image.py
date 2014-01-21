import eyetracker

cam_id = eyetracker.camera.camera.lookForCameras()

cam = eyetracker.camera.camera.Camera(cam_id['Camera_1'])

while True:
    frame = cam.frame()
    
    ''' your code '''



    ''' end of your code'''

    ''' press q or ESC to quit'''

    key = eyetracker.camera.display.displayImage(frame)
    if key == 27 or key == ord('q'):
        break

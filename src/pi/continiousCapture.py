import time
import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.rotation = 90
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    while True:
        camera.capture('../../static/ram/picam.jpg')
        time.sleep(1)

import time
import os
import libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()

def init_picam():
        config = picam.create_preview_configuration(main={"size":(1600,1200)})
        config["transform"] = libcamera.Transform(hflip=1,vflip=1)
        picam.configure(config)

def capture_frame(path="/home/rohan/Desktop/zenith2024/captures/", fname="capture.jpg"):
        filename = os.path.join(path, fname)
        picam.capture_file(filename)
        return filename

def start_camera():
        init_picam()
        picam.start()

def stop_camera():
        picam.close()
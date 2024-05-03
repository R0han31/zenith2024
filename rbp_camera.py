import time
import os
try:
        import libcamera
        from picamera2 import Picamera2, Preview
except RuntimeError:
        pass

try:
        picam = Picamera2()

        config = picam.create_preview_configuration(main={"size":(1600,1200)})
        config["transform"] = libcamera.Transform(hflip=1,vflip=1)
        picam.configure(config)

except RuntimeError:
        pass


# picam.start_preview(Preview.QTGL)

#picam.capture_file("ifsk.jpg")

def capture_frame(path="/home/rohan/Desktop/zenith2024/captures/", fname="capture.jpg"):
        filename = os.path.join(path, fname)
        picam.capture_file(filename)
        return filename

def start_camera():
        picam.start()

def stop_camera():
        picam.close()

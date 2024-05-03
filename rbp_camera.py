import time
import os
try:
        print("before import libcamera")
        import libcamera
        print("after import libcamera")
        print("before import picamera")
        from picamera2 import Picamera2, Preview
        print("after import picamera")
except RuntimeError:
        pass

try:
        print("before init picam")
        with Picamera2() as picam:
                print("after init picam")

                print("before config picam")

                config = picam.create_preview_configuration(main={"size":(1600,1200)})
                config["transform"] = libcamera.Transform(hflip=1,vflip=1)
                picam.configure(config)
                print("after config picam")
        
except RuntimeError:
        pass



# picam.start_preview(Preview.QTGL)

#picam.capture_file("ifsk.jpg")

def capture_frame(path="/home/rohan/Desktop/zenith2024/captures/", fname="capture.jpg"):
        filename = os.path.join(path, fname)
        picam.capture_file(filename)
        return filename

def start_camera():
        try:
                picam.close()
        except Exception as e:
                print(e)
        try:
                picam.start()
        except Exception as e:
                print(e)

def stop_camera():
        picam.close()

from rbp_camera import *
from ultralytics import YOLO

model = YOLO('/home/rohan/Desktop/zenith24/models/Final.pt')

if __name__ == "__main__":
	start_camera()
	while True:
		inp = input("Press enter to capture a frame:")
		if inp == "exit":
			break
		if inp:
			img_path = capture_frame()
			input("Press enter to predict:")
			results = model.predict(img_path)
			result = results[0]
			names = result.names
			
			for i in range(len(result.boxes)):
				box = result.boxes[i]
				print('Object: ', names[box.cls[0].item()])
	
	stop_camera()
	

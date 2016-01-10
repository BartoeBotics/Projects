# Requirements - Raspberry Pi, Raspberry Pi Camera, Python, and OpenCV

# This runs the program
# python hats_on_face_detection.py --face cascades/haarcascade_frontalface_default.xml --hat images/christmas_hat.jpg

from FaceDetection.facedetector import FaceDetector
from FaceDetection import imutils
from FaceDetection import auto_canny
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import argparse
import time
import cv2

fix = 0
x = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True,
	help = "Path to the face cascade file")
ap.add_argument("-v", "--video", 
	help = "Path to the (optional) video file")
ap.add_argument("--hat", required = True,
	help = "Path to the hat file")
args = vars(ap.parse_args())

# load image of hat and set up templates
hat = cv2.imread(args["hat"])

# initialize the camera and grab a reference to the raw camera
# capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# construct the face detector and allow the camera to warm
# up
fd = FaceDetector(args["face"])
time.sleep(0.1)

# capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image
	frame = f.array

	# resize the frame and convert it to grayscale
	# frame = imutils.resize(frame, width = 300)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the image and then clone the frame
	# so that we can draw on it
	faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5,
		minSize = (30, 30))
	frameClone = frame.copy()

	new_hat = frameClone.copy()
	cv2.rectangle(new_hat, (0,0), (new_hat.shape[1],new_hat.shape[0]), 
		(255, 255, 255), -1)

	# loop over the face bounding boxes and draw them
	for (x, y, w, h) in faceRects:
		# cv2.rectangle(frameClone, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		if 1.4 * w < 80:
			width = 80
		else:
			width = int(1.4 * w)
		resized_hat = imutils.resize(hat, width = width)
		if (y + 0.25 * resized_hat.shape[0]) > resized_hat.shape[0] and (x - 5 + resized_hat.shape[1]) < frameClone.shape[1]:
			fix = 1
			x_offset = x - 5
			y_offset = y - 0.75 * resized_hat.shape[0]
			new_hat[y_offset:y_offset + resized_hat.shape[0], 
				x_offset:x_offset + resized_hat.shape[1]] = resized_hat
			gray_hat = cv2.cvtColor(new_hat, cv2.COLOR_BGR2GRAY)
			# blurred_hat = cv2.GaussianBlur(gray_hat, (3,3), 0)
			# edged_hat = cv2.Canny(gray_hat, 169, 255)
			edged_hat = auto_canny.auto_canny(gray_hat)
		
			(_, cnts, _) = cv2.findContours(edged_hat.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)

			# create negative mask
			cv2.drawContours(frameClone, cnts, -1, (0, 0, 0), cv2.FILLED)
			
	#create positive mask and combine
	if fix == 1:
		mask = np.zeros(frameClone.shape[:2], dtype = "uint8")
		cv2.drawContours(mask, cnts, -1, (255, 255, 255), cv2.FILLED)
		final = cv2.bitwise_and(new_hat, new_hat, mask = mask)

	# show our detected faces, then clear the frame in
	# preparation for the next frame
	if fix == 1:
		resized_frameClone = imutils.resize(frameClone, width = 1065)
		resized_final = imutils.resize(final, width = 1065)
		cv2.imshow("Face", cv2.bitwise_or(resized_frameClone, resized_final))
	else:
		resized_frameClone = imutils.resize(frameClone, width = 1065)
		cv2.imshow("Face", resized_frameClone)
	rawCapture.truncate(0)

	# take a picture it will last longer
	if cv2.waitKey(1) & 0xFF == ord("c"):
		if fix == 1:
			x = x + 1		
			cv2.imwrite("Momento_{}.jpg".format(x), cv2.bitwise_or(resized_frameClone, resized_final))
			print("Photo Taken!!!")
			time.sleep(2)
		else:
			x = x + 1
			cv2.imwrite("Momento_{}.jpg".format(x), resized_frameClone)
			print("Photo Taken!!!")
			time.sleep(2)
			
	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

	fix = 0
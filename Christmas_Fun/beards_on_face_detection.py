# Requirements - Raspberry Pi, Raspberry Pi Camera, Python, and OpenCV

# This runs the program
# python beards_on_face_detection.py --face cascades/haarcascade_frontalface_default.xml --beard images/white_beard.jpg

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
ap.add_argument("--beard", required = True,
	help = "Path to the beard file")
args = vars(ap.parse_args())

# load image of beard and set up templates
beard = cv2.imread(args["beard"])

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
	# so tbeard we can draw on it
	faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5,
		minSize = (30, 30))
	frameClone = frame.copy()

	new_beard = frameClone.copy()
	cv2.rectangle(new_beard, (0,0), (new_beard.shape[1],new_beard.shape[0]), 
		(255, 255, 255), -1)

	# loop over the face bounding boxes and draw them
	for (x, y, w, h) in faceRects:
		# cv2.rectangle(frameClone, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		resized_beard = imutils.resize(beard, width = w)
		if (resized_beard.shape[0] + y + (3/5 * h)) < frameClone.shape[0]:
			fix = 1
			x_offset = x
			y_offset = y + (3/5 * h)
			new_beard[y_offset:y_offset + resized_beard.shape[0], 
				x_offset:x_offset + resized_beard.shape[1]] = resized_beard
			gray_beard = cv2.cvtColor(new_beard, cv2.COLOR_BGR2GRAY)
			# blurred_beard = cv2.GaussianBlur(gray_beard, (5,5), 0)
			# edged_beard = cv2.Canny(gray_beard, 169, 255)
			edged_beard = auto_canny.auto_canny(gray_beard)
			
			(_, cnts, _) = cv2.findContours(edged_beard.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
		
			# print("I count {} beard(s)".format(len(cnts)))

			# create negative mask
			cv2.drawContours(frameClone, cnts, -1, (0, 0, 0), cv2.FILLED)
			
	# create positive mask and combine
	if fix == 1:
		mask = np.zeros(frameClone.shape[:2], dtype = "uint8")
		cv2.drawContours(mask, cnts, -1, (255, 255, 255), cv2.FILLED)
		final = cv2.bitwise_and(new_beard, new_beard, mask = mask)
	
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
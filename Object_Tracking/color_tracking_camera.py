from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
import numpy as np
import cv2
import time

# Set GPIO pins 7, 8, and 11 as output
GPIO.setmode(GPIO.BCM);
GPIO.setup(7, GPIO.OUT);
GPIO.setup(8, GPIO.OUT);
GPIO.setup(11, GPIO.OUT);

# Define the upper and lower boundaries for a color
# # Rubik's Cube - Red Side
# redLower = np.array([0, 15, 115], dtype = "uint8")
# redUpper = np.array([55, 115, 255], dtype = "uint8")
# Red Construction Paper
redLower = np.array([10, 30, 120], dtype = "uint8")
redUpper = np.array([70, 120, 255], dtype = "uint8")

# Initialize the camera and grab a reference to the raw camera
# capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Capture frames from the camera
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# Grab the raw NumPy array representing the image
	frame = f.array

	# Set xLocation
	xLocation = 0

	# Determine which pixels fall within the boundaries
	# and then blur the binary image
	red = cv2.inRange(frame, redLower, redUpper)
	red = cv2.GaussianBlur(red, (3, 3), 0)

	# Find contours in the image
	(_, cnts, _) = cv2.findContours(red.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# Check to see if any contours were found
	if len(cnts) > 0:
		# Sort the contours and find the largest one
		cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

		# Compute the bounding box around the contour
		# then draw it.  Find the xLocation.
		x, y, w, h = cv2.boundingRect(cnt)
		cv2.rectangle(frame, (int(x),int(y)), (int(x)+int(w), int(y)+int(h)), (0,255,0), 2)
		xLocation = x + w/2
		# print ("xLocation: ", xLocation)

		# Determine where the object is on the screen
		segmentWidth = frame.shape[1]/3
		if xLocation < segmentWidth:
			print ("Left")
			GPIO.output(7, True);
			GPIO.output(8, False);
			GPIO.output(11, False);
		elif xLocation > segmentWidth and xLocation < (2*segmentWidth):
			print ("Center")
			GPIO.output(7, False);
			GPIO.output(8, True);
			GPIO.output(11, False);
		else:
			print ("Right")
			GPIO.output(7, False);
			GPIO.output(8, False);
			GPIO.output(11, True);
		
	else:
		GPIO.output(7, False);
		GPIO.output(8, False);
		GPIO.output(11, False);	

	# Show the frame and the binary image
	cv2.imshow("Tracking", frame)
	cv2.imshow("Binary", red)
	rawCapture.truncate(0)

	# If the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break
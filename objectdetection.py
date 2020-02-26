import io
import picamera
import cv2
import numpy
import RPi.GPIO as GPIO                    
import time
import threading 
from nanpy import (ArduinoApi, SerialManager)
import pdb

GPIO.setmode(GPIO.BOARD)
TRIG = 16                              
ECHO = 18
TRIG1 = 11                              
ECHO1 = 13
TRIG2 = 29
ECHO2 = 31
GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(TRIG1,GPIO.OUT)                  
GPIO.setup(ECHO1,GPIO.IN)
GPIO.setup(TRIG2,GPIO.OUT)                  
GPIO.setup(ECHO2,GPIO.IN)
motor = 8
motor1 = 7

try:
	connection = SerialManager()
	a = ArduinoApi(connection = connection)
except:
	print ('Failed')
a.pinMode(motor, a.OUTPUT);
a.pinMode(motor1, a.OUTPUT);
a.pinMode(13, a.OUTPUT)
def roadSign():
	#pdb.set_trace() 
	#Create a memory stream so photos doesn't need to be saved in a file
	stream = io.BytesIO()

	#Get the picture (low resolution, so it should be quite fast)
	#Here you can also specify other parameters (e.g.:rotate the image)
	#while True :
	with picamera.PiCamera() as camera:
		camera.resolution = (112, 112)
		camera.capture(stream, format='jpeg', use_video_port=True)
		#Convert the picture into a numpy array
	buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

	#Now creates an OpenCV image
	image = cv2.imdecode(buff, 1)

	#Load a cascade file for detecting faces
	face_cascade = cv2.CascadeClassifier('stopsigndetector.xml')

	#Convert to grayscale
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

	#Look for faces in the image using the loaded cascade file
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	global y
	y = (len(faces))
	print ("Found",y," face(s)")
	#Draw a rectangle around every found face
	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
	#time.sleep(1)
	#Save the result image
	#cv2.imshow('result',image)
	stream.seek(0)
	stream.truncate()
	del buff
def schoolaheadSign():
	#pdb.set_trace() 
	#Create a memory stream so photos doesn't need to be saved in a file
	stream = io.BytesIO()

	#Get the picture (low resolution, so it should be quite fast)
	#Here you can also specify other parameters (e.g.:rotate the image)
	#while True :
	with picamera.PiCamera() as camera:
		camera.resolution = (112, 112)
		camera.capture(stream, format='jpeg', use_video_port=True)
		#Convert the picture into a numpy array
	buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

	#Now creates an OpenCV image
	image1 = cv2.imdecode(buff, 1)

	#Load a cascade file for detecting faces
	face_cascade1 = cv2.CascadeClassifier('schoolsigndetector.xml')

	#Convert to grayscale
	gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)

	#Look for faces in the image using the loaded cascade file
	faces1 = face_cascade1.detectMultiScale(gray1, 1.1, 5)
	global x
	x = (len(faces1))
	print ("Found",x," schoolsigns(s)")
	#Draw a rectangle around every found face
	for (x,y,w,h) in faces1:
		cv2.rectangle(image1,(x,y),(x+w,y+h),(255,255,0),2)

	#Save the result image
	#cv2.imshow('result',image)
	stream.seek(0)
	stream.truncate()
	del buff
def redtrafficsign():
	#pdb.set_trace() 
	#Create a memory stream so photos doesn't need to be saved in a file
		stream = io.BytesIO()
	#Get the picture (low resolution, so it should be quite fast)
	#Here you can also specify other parameters (e.g.:rotate the image)
		with picamera.PiCamera() as camera:
			camera.resolution = (1280, 720)
			camera.capture(stream, format='jpeg', use_video_port=False)
			#Convert the picture into a numpy array
		buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

		#Now creates an OpenCV image
		image2 = cv2.imdecode(buff, 1)

		#Load a cascade file for detecting faces
		face_cascade2 = cv2.CascadeClassifier('redsignal.xml')

		#Convert to grayscale
		gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)

		#Look for faces in the image using the loaded cascade file
		faces2 = face_cascade2.detectMultiScale(gray2, 1.5, 5)
		global d
		d = (len(faces2))
		print ("Found",d," redsignal(s)")
		#Draw a rectangle around every found face
		for (x,y,w,h) in faces2:
			cv2.rectangle(image2,(x,y),(x+w,y+h),(255,255,0),2)
		stream.seek(0)
		stream.truncate()
def maincode ():
	while (True):
		roadSign()
		time.sleep(0.1)
		schoolaheadSign()
		time.sleep(0.1)
		redtrafficsign()
		time.sleep(0.1)
		if (y > 0):
				a.digitalWrite (13, a.LOW)
				time.sleep(5)
				a.digitalWrite (13, a.HIGH)
				time.sleep(3)
		elif(x > 0):
			for l in range (0, 10):
				a.digitalWrite(13, a.HIGH)
				time.sleep(0.05)
				a.digitalWrite(13, a.LOW)
				time.sleep(0.05)
				l = l+1
		if (d > 0):
			a.digitalWrite (13, a.LOW)
maincode()


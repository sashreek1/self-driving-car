#from multiprocessing import Process
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

motorstate=0
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
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
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
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
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
		cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
	stream.seek(0)
	stream.truncate()
	del buff
def obstacleahead():
	global distance
	global motorstate
#sensor ahead
	pulse_end = None
	pulse_start = None
	pulse_duration = None
	GPIO.output(TRIG, False)                 
	#print "Waitng For Sensor To Settle"
	time.sleep(0.002)                            

	GPIO.output(TRIG, True)                  
	time.sleep(0.00001)                      
	GPIO.output(TRIG, False)                 
	#print "waiting for echo =0", time.time()
	while GPIO.input(ECHO)==0:               
		pulse_start = time.time()              
	#timeout = time.time()+0.1
	#print "waiting for echo =1", time.time()
	while  GPIO.input(ECHO)==1:               
		pulse_end = time.time()
	#	if (pulse_end > timeout):
	#		print "echo didnt return ahead"
	#		break   
	global distance 
	if (pulse_end == None or pulse_start == None):
		distance = 0
		return distance
	pulse_duration = pulse_end - pulse_start 
	#if (pulse_duration <> 0):
	distance = pulse_duration * 17150        
	distance = round(distance, 2)            
	if distance > 2 and distance < 400:      
		print "Distance ahead:",distance ,"cm"
		return distance
    
	
def obstacleright():
	pulse_end1 = None
	pulse_start1 = None
	pulse_duration1 = None
	GPIO.output(TRIG1, False)                 
	#print "Waitng For Sensor To Settle"
	time.sleep(0.002)                            

	GPIO.output(TRIG1, True)                  
	time.sleep(0.00001)                      
	GPIO.output(TRIG1, False)                 
	#print "waiting for echo1 =0", time.time()
	while GPIO.input(ECHO1)==0:               
		pulse_start1 = time.time()              
	#timeout = time.time()+0.1
	#print "waiting for echo1 =1", time.time()
	while  GPIO.input(ECHO1)==1:               
		pulse_end1 = time.time()
	#	if (pulse_end > timeout):
	#		print "echo didnt return ahead"
	#		break 
	global distance1   
	if (pulse_end1 == None or pulse_start1 == None):
		distance1 = 0
		return distance1
	pulse_duration1 = pulse_end1 - pulse_start1 
	#if (pulse_duration <> 0):
	distance1 = pulse_duration1 * 17150        
	distance1 = round(distance1, 2)            
	if distance1 > 2 and distance1 < 400:      
		print "Distance right:",distance1 ,"cm"
		return distance1

def obstacleleft():
#sensorleft 
	pulse_end2 = None
	pulse_start2 = None
	pulse_duration2 = None
	GPIO.output(TRIG2, False)                 
	#print "Waitng For Sensor To Settle"
	time.sleep(0.002)                            

	GPIO.output(TRIG2, True)                  
	time.sleep(0.00001)                      
	GPIO.output(TRIG2, False)                 
	#print "waiting for echo2 =0", time.time()
	while GPIO.input(ECHO2)==0:               
		pulse_start2 = time.time()              
	#timeout = time.time()+0.1
	#print "waiting for echo2 =1", time.time()
	while  GPIO.input(ECHO2)==1:               
		pulse_end2 = time.time()
	#	if (pulse_end > timeout):
	#		print "echo didnt return ahead"
	#		break    
	global distance2
	if (pulse_end2 == None or pulse_start2 == None):
		distance2 = 0
		return distance2
	pulse_duration2 = pulse_end2 - pulse_start2 
	#if (pulse_duration <> 0):
	distance2 = pulse_duration2 * 17150        
	distance2 = round(distance2, 2)            
	if distance2 > 2 and distance2 < 400:      
		print "Distance left:",distance2 ,"cm"
		return distance2
def maincode():
	while(True):
		obstacleahead()
		time.sleep(0.1)
		obstacleleft()
		time.sleep(0.1)
		obstacleright()
		time.sleep(0.1)
		roadSign()
		time.sleep(0.1)
		motorstate = 0
		if (distance < 50):     
			a.digitalWrite(13, a.LOW)
			motorstate = 0
		else:
			a.digitalWrite(13, a.HIGH) 
		if (distance1 < 20 ):
			if (motorstate == 0 or motorstate == 2) :
				a.digitalWrite(motor, a.HIGH)
				motorstate = 1 
			else :
				a.digitalWrite(motor, a.LOW)
		else:
			a.digitalWrite(motor, a.LOW)
		if (distance2 < 20 ):
			if (motorstate == 0 or motorstate == 1) :    
				a.digitalWrite(motor1, a.HIGH)
				motorstate = 2
		else:
			a.digitalWrite(motor1, a.LOW)
		if (y > 0):
			a.digitalWrite (13, a.LOW)
			time.sleep(5)
			a.digitalWrite (13, a.HIGH)
			time.sleep(3)
			x = 0
			d = 0
		if(x > 0 ):
			for l in range (0, 10):
				a.digitalWrite(13, a.HIGH)
				time.sleep(0.05)
				a.digitalWrite(13, a.LOW)
				time.sleep(0.05)
				l = l+1
			y = 0
			d = 0 
		if (d > 0):
			a.digitalWrite (13, a.LOW)
			x = 0
			y = 0
			
	        

maincode()



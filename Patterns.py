import sys
import math
import time
from random import randint

sharedBool = False
sharedIndex = 0
sharedInt = 0
stopUpdating = False
sleepTime = 0
sharedNextTick = 0.01

pixelTuple = [255,255,255]
pixelBlue = [0,255,0]
pixelRed = [255,0,0]
pixelGreen = [0,0,255]

specificOffTime = 0.5
specificOnTime = 2.0
#specificOnTime = 0.05 #nice! (could poof this fast too)
#specificOnTime = 0.02 #perfect for most things

def resetSharedVars():
	global sharedBool
	global sharedIndex
	global sharedInt
	global stopUpdating
	sharedBool = False
	sharedIndex = 0
	sharedInt = 0
	stopUpdating = False

def sharedUpdate(ledStrip):
	global sleepTime
	global stopUpdating

	if stopUpdating == True:
		pass
	else:
		ledStrip.update()
		
	time.sleep(sleepTime)

def clearAll(ledStrip):
	global sharedInt
	global stopUpdating
	for i in range(0, ledStrip.nLeds):
		#if i == 0:
			#ledStrip.setPixel(i, [255, 255, 255])	
		#else:
		ledStrip.setPixel(i, [0, 0, 0])

		if stopUpdating == False and sharedInt < 1000:
			sharedInt += 1
		else:
			stopUpdating = True

def randomString(ledStrip):
	for i in range(0, ledStrip.nLeds):
		if randint(0,1) == 0:
			ledStrip.setPixel(i, [0, 0, 0])
		else:
			ledStrip.setPixel(i, pixelBlue)

def randomPoint(ledStrip):
	p = randint(0, ledStrip.nLeds)
	for i in range(0, ledStrip.nLeds):
		if i == p:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	
def simpleChaser(ledStrip):
	global sharedIndex
	p = sharedIndex
	sharedIndex += 1
	if sharedIndex > ledStrip.nLeds - 1:
		sharedIndex = 0
	for i in range(0, ledStrip.nLeds):
		if i == p:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	
def cylonChaser(ledStrip):
	global sharedBool
	global sharedIndex

	if sharedBool == False:
		sharedIndex += 1
	else:
		sharedIndex -= 1

	if sharedIndex > ledStrip.nLeds - 1:
		sharedIndex = ledStrip.nLeds - 1
		sharedBool = True
	if sharedIndex < 0:
		sharedIndex = 0
		sharedBool = False

	for i in range(0, ledStrip.nLeds):
		if (i == sharedIndex):
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])
	
def stringBlink(ledStrip):
	global sharedBool
	b = sharedBool
	for i in range(0, ledStrip.nLeds):
		if b == True:
			ledStrip.setPixel(i,[255, 255, 255])
			sharedBool = False
		else:
			ledStrip.setPixel(i, [1, 1, 1])
			sharedBool = True

def lightningStringBlink(ledStrip, probability):
	c = randint(0,100)
	for i in range(0, ledStrip.nLeds):
		if c < probability:
			ledStrip.setPixel(i,[255, 255, 255])
		else:
			ledStrip.setPixel(i, [0, 0, 0])

def stringPulsate(ledStrip):
	global sharedBool
	global sharedInt
	if sharedBool == False:
		sharedInt *= 2
	else:
		sharedInt /= 2	

	if sharedInt > 255:
		sharedInt = 255
		sharedBool = True
	if sharedInt < 1:
		sharedInt = 1
		sharedBool = False	
	
	for i in range(0, ledStrip.nLeds):
		ledStrip.setPixel(i,[sharedInt, sharedInt, sharedInt])

def watery(ledStrip, intensity):
	t = time.clock()
	for i in range(0, ledStrip.nLeds):
		p = math.sin(t + i)
		p = abs(p) * intensity
		p = int(p)
		#print p
		ledStrip.setPixel(i,[p,0,p])

def blueWatery(ledStrip, intensity):
	t = time.clock()
	for i in range(0, ledStrip.nLeds):
		p = math.sin(t + i)
		p = abs(p) * intensity
		p = int(p)
		#print p
		ledStrip.setPixel(i,[0, p, 0])
		ledStrip.update()

def lightChase(ledStrip):
	global sharedIndex
	for i in range(0, ledStrip.nLeds):
		if i == sharedIndex:
			ledStrip.setPixel(i,[255, 255, 255])
		elif i == sharedIndex + 1:
			ledStrip.setPixel(i,[255, 255, 255])	
		elif i == sharedIndex + 2:
			ledStrip.setPixel(i,[255, 255, 255])		
		else:
			ledStrip.setPixel(i, [0, 0, 0])		

	sharedIndex += 3
	#print sharedIndex
	if sharedIndex > ledStrip.nLeds - 1:
		sharedIndex = 0

def lightChaseBlue(ledStrip):
	global sharedIndex
	for i in range(0, ledStrip.nLeds):
		if i == sharedIndex:
			ledStrip.setPixel(i,[0, 255, 0])
		elif i == sharedIndex + 1:
			ledStrip.setPixel(i,[0, 255, 0])	
		elif i == sharedIndex + 2:
			ledStrip.setPixel(i,[0, 255, 0])		
		else:
			ledStrip.setPixel(i, [0, 0, 0])		

	sharedIndex += 3
	#print sharedIndex
	if sharedIndex > ledStrip.nLeds - 1:
		sharedIndex = 0
		
def blinkSpecific(ledStrip, node):
	global sharedBool
	global sharedNextTick
	b = sharedBool
	for i in range(0, ledStrip.nLeds):
			if i == node:
				if time.time() > sharedNextTick:
					if b == True:
						ledStrip.setPixel(i,pixelTuple)
						sharedBool = False
						sharedNextTick = time.time() + specificOnTime
					else:
						ledStrip.setPixel(i, [0, 0, 0])
						sharedBool = True
						sharedNextTick = time.time() + specificOffTime
			else:
				ledStrip.setPixel(i, [0, 0, 0])

def blinkSpecificAll(ledStrip):
	global sharedBool
	global sharedNextTick
	b = sharedBool
	if time.time() > sharedNextTick:
		print "tick " + format(b)
		
		for i in range(0, ledStrip.nLeds):
			if b == True:
				ledStrip.setPixel(i,pixelTuple)
				sharedBool = False
				sharedNextTick = time.time() + specificOnTime
			else:
				ledStrip.setPixel(i, [0, 0, 0])
				sharedBool = True
				sharedNextTick = time.time() + specificOffTime

def chaseSpecific(ledStrip):
	global sharedBool
	global sharedNextTick
	global sharedIndex
	b = sharedBool
	j = sharedIndex
	if time.time() > sharedNextTick:
		#print "tick " + format(b)
		
		for i in range(0, ledStrip.nLeds):
			if b == True:
				if i == j:
					ledStrip.setPixel(i,pixelTuple)
					sharedBool = False
					sharedNextTick = time.time() + specificOnTime
					sharedIndex += 1
					if sharedIndex > ledStrip.nLeds - 1:
						sharedIndex = 0
			else:
				ledStrip.setPixel(i, [0, 0, 0])
				sharedBool = True
				sharedNextTick = time.time() + specificOffTime


def allOn(ledStrip):
	for i in range(0, ledStrip.nLeds):
		ledStrip.setPixel(i, pixelBlue)

def manualControl(ledStrip, light):
	for i in range(0, ledStrip.nLeds):
		if(i == light):
			j = i * 3
			ledStrip.setPixel(j,[255,255,255])
			ledStrip.setPixel(j+1,[255,255,255])
			ledStrip.setPixel(j+2,[255,255,255])
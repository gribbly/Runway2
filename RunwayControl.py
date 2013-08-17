import sys
import math
import time
from random import randint

#physical
nodeMap = []
nodeStates = []
nodeCount = 0

#logical
lightsAll = []
flamesAll = []
lightsLeft = []
lightsRight = []
lightSideLength = 0
flamesLeft = []
flamesRight = []
flameSideLength = 0

#logging
events = []

#globals
rcTick = 1.0
rcNextTick = 0
rcBool = False
rcIndex1 = 0
rcIndex2 = 0

#colors
pixelWhite = [255,255,255]
pixelBlue = [0,255,0]
pixelYellow = [255,255,0]
pixelRed = [255,0,0]
pixelGreen = [0,0,255]
pixelOff = [0,0,0]
pixelFlame = [255,0,0]

def log_event(msg):
	events.append(msg)


def create(ledStrip):
	log_event('creating node array [{0} nodes total]'.format(ledStrip.nLeds))

	#first node
	nodeMap.append('N')
	
	#intro
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')
	
	#side 1
	for i in range(0,20):
		nodeMap.append('F')
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
	
	#side 2
	for i in range(0,20):
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
		nodeMap.append('F')

	#outro
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')

	#last node
	nodeMap.append('N')
	
	sharedCreate(ledStrip)

	return events

def createCamTestRig(ledStrip):	
	log_event('WARNING: This is Cam\'s test rig mode!')
	log_event('creating node array [{0} nodes total]'.format(ledStrip.nLeds))

	#first node
	nodeMap.append('N')
	
	#intro
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')
	
	#side 1
	for i in range(0,8):
		nodeMap.append('F')
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
	
	#side 2
	for i in range(0,8):
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
		nodeMap.append('1')
		nodeMap.append('2')
		nodeMap.append('3')
		nodeMap.append('F')

	#outro
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')
	nodeMap.append('1')
	nodeMap.append('2')
	nodeMap.append('3')

	#last node
	nodeMap.append('N')
	
	sharedCreate(ledStrip)

	return events

def sharedCreate(ledStrip):
	print "nodeMap:"
	for i in range(0,len(nodeMap)):
		#print format(i) + " " + nodeMap[i]
		print nodeMap[i]
	
	#light addresses
	for	i in range(0,len(nodeMap)):
		if nodeMap[i] == '1' or nodeMap[i] == '2' or nodeMap[i] == '3':
			lightsAll.append(i)
	
	#flame addresses
	for i in range(0,len(nodeMap)):
		if nodeMap[i] == 'F':
			flamesAll.append(i)
			
	log_event("Map contains {0} light nodes...".format(len(lightsAll)))
	print 'LIGHTS:'
	print lightsAll
	log_event("Map contains {0} flame nodes...".format(len(flamesAll)))
	print 'FLAMES:'
	print flamesAll
	
	#left and right side lights
	global lightSideLength
	lightSideLength = len(lightsAll)/2
	print '\nlightSideLength = {0} nodes'.format(lightSideLength)
	
	for i in range(0,lightSideLength):	
		lightsLeft.append(lightsAll[i])
	for i in range(0, lightSideLength):
		lightsRight.append(lightsAll[i+lightSideLength])
		
	lightsRight.reverse()
		
	log_event("Left side has {0} light nodes...".format(len(lightsLeft)))
	print 'LIGHTS (LEFT SIDE):'
	print lightsLeft
	log_event("Right side has {0} light nodes...".format(len(lightsRight)))
	print 'LIGHTS (RIGHT SIDE):'
	print lightsRight
	
	#left and right side flames	
	global flameSideLength
	flameSideLength = len(flamesAll)/2
	print '\nflameSideLength = {0} nodes'.format(flameSideLength)

	for i in range(0,flameSideLength):
		flamesLeft.append(flamesAll[i])
	for i in range(0, flameSideLength):
		flamesRight.append(flamesAll[i+flameSideLength])
		
	flamesRight.reverse()
		
	log_event("Left side has {0} flame nodes...".format(len(flamesLeft)))
	print 'FLAMES (LEFT SIDE):'
	print flamesLeft
	log_event("Right side has {0} flame nodes...".format(len(flamesRight)))
	print 'FLAMES (RIGHT SIDE):'
	print flamesRight
	
	#init nodeStates
	for i in range(0, len(nodeMap)):
		nodeStates.append(False)

def changeTick(n):
	global rcTick
	rcTick = n
	print "RunwayControl - tick is now {0}".format(rcTick)

def showNode(n):
	nodeStates[n] = True

def showLights():
	for i in range(0,len(lightsAll)):
		nodeStates[lightsAll[i]] = True

def showFlames():
	for i in range(0,len(flamesAll)):
		nodeStates[flamesAll[i]] = True
		
def showLeftSideAll():
	global lightsLeft, lightsRight, lightSideLength
	global flamesLeft, flamesRight, flameSideLength

	for i in range(0,lightSideLength):
		nodeStates[lightsAll[i]] = True	
	for i in range(0,flameSideLength):
		nodeStates[flamesAll[i]] = True

def showRightSideAll():
	global lightsLeft, lightsRight, lightSideLength
	global flamesLeft, flamesRight, flameSideLength

	for i in range(lightSideLength, len(lightsAll)):
		nodeStates[lightsAll[i]] = True	
	for i in range(flameSideLength , len(flamesAll)):
		nodeStates[flamesAll[i]] = True

def chaseLights1():
	global rcTick, rcNextTick
	global rcIndex1
	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		for i in range(0,len(lightsAll)):
			if i == rcIndex1:
				nodeStates[lightsAll[i]] = True
		rcIndex1 += 1
		if rcIndex1 > len(lightsAll):
			rcIndex1 = 0

def chaseLights2():
	global rcIndex1, lightsLeft, lightsRight, lightSideLength
	for i in range(0,lightSideLength):
		if i == rcIndex1:
			nodeStates[lightsLeft[i]] = True
			nodeStates[lightsRight[i]] = True
	rcIndex1 += 1
	if rcIndex1 > lightSideLength:
		rcIndex1 = 0

def chaseLights3():
	global rcIndex1, lightsLeft, lightsRight, lightSideLength
	for i in range(lightSideLength-1, 0, -1):
		if i == rcIndex1:
			nodeStates[lightsLeft[i]] = True
			nodeStates[lightsRight[i]] = True
	rcIndex1 -= 1
	if rcIndex1 < 0:
		rcIndex1 = lightSideLength-1
		
def chaseLightsAndFlames1():
	global rcIndex1, rcIndex2
	global lightsLeft, lightsRight, lightSideLength
	global flamesLeft, flamesRight, flameSideLength

	for i in range(0,flameSideLength):
		if i == rcIndex2:
			nodeStates[flamesLeft[i]] = True
			nodeStates[flamesRight[i]] = True
		else:
			nodeStates[flamesLeft[i]] = False
			nodeStates[flamesRight[i]] = False
	rcIndex2 += 1
	if rcIndex2 > flameSideLength:
		rcIndex2 = 0
		
	for j in range(0,lightSideLength):
		if j == rcIndex1:
			nodeStates[lightsLeft[j]] = True
			nodeStates[lightsRight[j]] = True
		else:
			nodeStates[lightsLeft[j]] = False
			nodeStates[lightsRight[j]] = False
	rcIndex1 += 1
	if rcIndex1 > lightSideLength:
		rcIndex1 = 0
		
def chaseLights4(n):
	global rcIndex1, lightsLeft, lightsRight, lightSideLength
	if rcIndex1 > n - 1:
		rcIndex1 = 0
	for i in range(0, lightSideLength - rcIndex1):
		if i % n == 0:
			nodeStates[lightsLeft[i + rcIndex1]] = True
			nodeStates[lightsRight[i + rcIndex1]] = True
			
	rcIndex1 += 1

def chaseLights5(n, w):
	#todo: support w
	global rcIndex1, lightsLeft, lightsRight, lightSideLength
	if rcIndex1 > n - 1:
		rcIndex1 = 0
	for i in range(0, lightSideLength - rcIndex1):
		if i % n == 0:
			nodeStates[lightsLeft[i + rcIndex1]] = True
			nodeStates[lightsRight[i + rcIndex1]] = True
			
	rcIndex1 += 1


def clear():
	for i in range(0,len(nodeMap)):
		nodeStates[i] = False

def update(ledStrip):
	for i in range(0,len(nodeMap)):
		if nodeStates[i] == True:
			#debug
			if nodeMap[i] == 'F':
				ledStrip.setPixel(i, pixelFlame)
			else:
				ledStrip.setPixel(i, pixelBlue)
		else:
			ledStrip.setPixel(i, pixelOff)
		
	ledStrip.update()
	time.sleep(0)

def coinToss():
	if randint(0,1) == 0:
		return False
	else:
		return True
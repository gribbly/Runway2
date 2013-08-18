import sys
import math
import time
from random import randint

#physical
nodeMap = []
nodeStates = []
nodeCount = 0
lightNodesAll = []
flameNodesAll = []
lightNodesLeft = []
lightNodesRight = []
lightNodesPerSide = 0
flameNodesLeft = []
flameNodesRight = []
flameNodesPerSide = 0

#logical
lightsAll = []
lightsLeft = []
lightsRight = []
lightsPerSide = 0

#logging
events = []

#globals
rcTick = 0.01666666666667
rcNextTick = 0
rcLightDuration = 1.0
rcFlameDuration = 0.05
rcLightFadeTime = 0.5
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
pixelOn = pixelBlue

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
			lightNodesAll.append(i)
	
	#flame addresses
	for i in range(0,len(nodeMap)):
		if nodeMap[i] == 'F':
			flameNodesAll.append(i)
			
	log_event("Map contains {0} light nodes...".format(len(lightNodesAll)))
	print 'LIGHTS NODES:'
	print lightNodesAll
	log_event("Map contains {0} flame nodes...".format(len(flameNodesAll)))
	print 'FLAME NODES:'
	print flameNodesAll
	
	#logical lights
	for i in range(0, len(lightNodesAll), 3):
		lightsAll.append([lightNodesAll[i],lightNodesAll[i+1],lightNodesAll[i+2]])
	
	print 'LIGHTS...'
	for i in range(0, len(lightsAll)):
		print 'Light {0}'.format(i + 1)
		print lightsAll[i]
	
	#left and right side lights
	global lightNodesPerSide, lightsPerSide
	lightNodesPerSide = len(lightNodesAll)/2
	lightsPerSide = lightNodesPerSide/3
	print '\nlightNodesPerSide = {0} nodes'.format(lightNodesPerSide)
	print '\nlightsPerSide = {0} lights'.format(lightsPerSide)
	
	for i in range(0,lightNodesPerSide):	
		lightNodesLeft.append(lightNodesAll[i])
	for i in range(0, lightNodesPerSide):
		lightNodesRight.append(lightNodesAll[i+lightNodesPerSide])
		
	lightNodesRight.reverse()
		
	log_event("Left side has {0} light nodes...".format(len(lightNodesLeft)))
	print 'LIGHTS (LEFT SIDE):'
	print lightNodesLeft
	log_event("Right side has {0} light nodes...".format(len(lightNodesRight)))
	print 'LIGHTS (RIGHT SIDE):'
	print lightNodesRight
	
	#left and right side flames	
	global flameNodesPerSide, flamesPerSide
	flameNodesPerSide = len(flameNodesAll)/2
	print '\nflameNodesPerSide = {0} nodes'.format(flameNodesPerSide)

	for i in range(0,flameNodesPerSide):
		flameNodesLeft.append(flameNodesAll[i])
	for i in range(0, flameNodesPerSide):
		flameNodesRight.append(flameNodesAll[i+flameNodesPerSide])
		
	flameNodesRight.reverse()
		
	log_event("Left side has {0} flame nodes...".format(len(flameNodesLeft)))
	print 'FLAMES (LEFT SIDE):'
	print flameNodesLeft
	log_event("Right side has {0} flame nodes...".format(len(flameNodesRight)))
	print 'FLAMES (RIGHT SIDE):'
	print flameNodesRight
	
	#init nodeStates
	for i in range(0, len(nodeMap)):
		nodeStates.append(0)

def showNode(n):
	global rcTick, rcNextTick
	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		nodeStates[n] = rcLightDuration + rcLightFadeTime

def showLights():
	global rcTick, rcNextTick
	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		for i in range(0,len(lightNodesAll)):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime

def showFlames():
	global rcTick, rcNextTick
	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		for i in range(0,len(flameNodesAll)):
			nodeStates[flameNodesAll[i]] = rcFlameDuration
		
def showLeftSideAll():
	global rcTick, rcNextTick
	global lightNodesLeft, lightNodesRight, lightNodesPerSide
	global flameNodesLeft, flameNodesRight, flameNodesPerSide

	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		for i in range(0,lightNodesPerSide):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime	
		for i in range(0,flameNodesPerSide):
			nodeStates[flameNodesAll[i]] = rcFlameDuration

def showRightSideAll():
	global rcTick, rcNextTick
	global lightNodesLeft, lightNodesRight, lightNodesPerSide
	global flameNodesLeft, flameNodesRight, flameNodesPerSide

	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		for i in range(lightNodesPerSide, len(lightNodesAll)):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime	
		for i in range(flameNodesPerSide , len(flameNodesAll)):
			nodeStates[flameNodesAll[i]] = rcFlameDuration

def chaseLights1():
	global rcTick, rcNextTick
	global rcIndex1
	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		for i in range(0,len(lightNodesAll)):
			if i == rcIndex1:
				nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime
		rcIndex1 += 1
		if rcIndex1 > len(lightNodesAll):
			rcIndex1 = 0

def chaseLights2():
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	for i in range(0,lightNodesPerSide):
		if i == rcIndex1:
			nodeStates[lightNodesLeft[i]] = rcLightDuration + rcLightFadeTime
			nodeStates[lightNodesRight[i]] = rcLightDuration + rcLightFadeTime
	rcIndex1 += 1
	if rcIndex1 > lightNodesPerSide:
		rcIndex1 = 0

def chaseLights3():
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	for i in range(lightNodesPerSide-1, 0, -1):
		if i == rcIndex1:
			nodeStates[lightNodesLeft[i]] = rcLightDuration + rcLightFadeTime
			nodeStates[lightNodesRight[i]] = rcLightDuration + rcLightFadeTime
	rcIndex1 -= 1
	if rcIndex1 < 0:
		rcIndex1 = lightNodesPerSide-1
		
def chaseLights4(n):
	global rcTick, rcNextTick
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		if rcIndex1 > n - 1:
			rcIndex1 = 0
		for i in range(0, lightNodesPerSide - rcIndex1):
			if i % n == 0:
				nodeStates[lightNodesLeft[i + rcIndex1]] = rcLightDuration + rcLightFadeTime
				nodeStates[lightNodesRight[i + rcIndex1]] = rcLightDuration + rcLightFadeTime
		rcIndex1 += 1

def chaseLights5():
	#light simple chaser
	global rcIndex1
	if checkTick():
		if rcIndex1 > len(lightsAll):
			rcIndex1 = 0
		for i in range(0,len(lightsAll)):
			if i == rcIndex1:
				activateLight(i)
			else:
				pass
		rcIndex1 += 1

def chaseLights6():
	#light circle chaser
	global rcIndex1
	if checkTick():
		if rcIndex1 > len(lightsAll)/2:
			rcIndex1 = 0
		for i in range(0,len(lightsAll)/2):
			if i == rcIndex1:
				activateLight(i)
				activateLight(i + len(lightsAll)/2)
			else:
				pass
		rcIndex1 += 1

def chaseLights7():
	#light dual chaser
	global rcIndex1
	if checkTick():
		if rcIndex1 > len(lightsAll)/2:
			rcIndex1 = 0
		for i in range(0,len(lightsAll)/2):
			if i == rcIndex1:
				leftI = i
				rightI = (len(lightsAll) - 1) - i
				activateLight(leftI)
				activateLight(rightI)
			else:
				pass
		rcIndex1 += 1

def chaseLights8(n):
	#light dual chaser, every n lights
	global rcIndex1
	if checkTick():
		if rcIndex1 > n - 1:
			rcIndex1 = 0
		for i in range(0,(len(lightsAll)/2) - rcIndex1):
			if i % n == 0:
				leftI = i + rcIndex1
				rightI = ((len(lightsAll) - 1) - i) - rcIndex1
				activateLight(leftI)
				activateLight(rightI)
			else:
				pass
		rcIndex1 += 1

def twinkleAllLights():
	if checkTick():
		for i in range(0,len(lightsAll)):
			if coinToss() == True:
				activateLight(i)
			else:
				pass

def showLogicalLight(n):
	if checkTick():
		for i in range(0,len(lightsAll)):
			if i == n:
				activateLight(i)
			else:
				pass

def clear():
	for i in range(0,len(nodeMap)):
		nodeStates[i] = 0

def clearImmediate():
	clear()
	update()

def decrementDurations(t):
	for i in range(0,len(nodeMap)):
		nodeStates[i] -= t

def updateFingerLights(l):
	for i in range(0, len(l)):
		requestedLightNumber = l[i]
		requestedLightNodes = getNodesFromLightNumber(requestedLightNumber)
		for i in range(0, len(requestedLightNodes)):
			nodeStates[lightNodesAll[requestedLightNodes[i]]] = rcLightDuration + rcLightFadeTime

def updateFingerFlames(f):
	for i in range(0, len(f)):
		requestedFlameNumber = f[i]
		requestedFlameNode = getNodeFromFlameNumber(requestedFlameNumber)
		nodeStates[flameNodesAll[requestedFlameNode]] = rcFlameDuration

def checkTick():
	global rcTick, rcNextTick
	if time.time() > rcNextTick:
		rcNextTick = time.time() + rcTick
		return True
	else:
		return False
		
def activateLight(i):
		try:
			nodeStates[lightsAll[i][0]] = rcLightDuration + rcLightFadeTime
		except:
			print "index error 0"
		try:
			nodeStates[lightsAll[i][1]] = rcLightDuration + rcLightFadeTime
		except:
			print "index error 1"
		try:
			nodeStates[lightsAll[i][2]] = rcLightDuration + rcLightFadeTime
		except:
			print "index error 2"

def update(ledStrip):
	global lightFadeTime
	for i in range(0,len(nodeMap)):
		if nodeStates[i] > rcLightFadeTime:
			#debug
			if nodeMap[i] == 'F':
				ledStrip.setPixel(i, pixelFlame)
			else:
				ledStrip.setPixel(i, pixelOn)
		elif nodeStates[i] > 0 and nodeStates[i] <= rcLightFadeTime:
			if nodeMap[i] == 'F':
				ledStrip.setPixel(i, pixelFlame)
			else:
				r = pixelOn[0]
				g = pixelOn[1]
				b = pixelOn[2]
				p = int(nodeStates[i]/rcLightFadeTime * 255)
				if r > 0:
					r = p
				if g > 0:
					g = p
				if b > 0:
					b = p
				ledStrip.setPixel(i, [r,g,b])
		else:
			ledStrip.setPixel(i, pixelOff)
	ledStrip.update()
	time.sleep(0)

def changeTick(n):
	global rcTick
	rcTick = max(min(n, 20.0), 0.01666666666667)
	print "RunwayControl - tick is now {0}".format(rcTick)
	rcNextTick = 0 #apply next update

def changeLightFadeTime(n):
	global rcLightFadeTime
	rcLightFadeTime = max(min(n, 10.0), 0)
	print "RunwayControl - light fade time is now {0}".format(rcLightFadeTime)

def changeLightDuration(n):
	global rcLightDuration
	rcLightDuration = max(min(n, 10.0), 0.0005)
	print "RunwayControl - light duration is now {0}".format(rcLightDuration)
	
def changeFlameDuration(n):
	global rcFlameDuration
	rcFlameDuration = max(min(n, 3.0), 0.005)
	print "RunwayControl - flame duration is now {0}".format(rcFlameDuration)

def getNodesFromLightNumber(n):
	node1 = (3 * n) - 1
	node2 = node1 - 1
	node3 = node1 - 2
	return [node1, node2, node3]
	
def getNodeFromFlameNumber(n):
	node1 = n - 1
	return node1

def coinToss():
	if randint(0,1) == 0:
		return False
	else:
		return True
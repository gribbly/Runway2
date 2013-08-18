import sys
import math
import time
import random

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
lightColorsAll = []
lightColorsLeft = []
lightColorsRight = []
lightsAndFire = []
lightsAndFireLeft = []
lightsAndFireRight = []

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
rcIndex3 = 0
rcIndex4 = 0
rcNextEvent1 = 0
rcColorModeRainbow = False
rcColorModeEq = False
rcAllowFire = False

#colors
pixelWhite = [255,255,255]
pixelBlue = [0,255,0]
pixelPink = [255,255,0]
pixelYellow = [255,0,255]
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
	print nodeMap
	
	#light addresses
	for	i in range(0,len(nodeMap)):
		if nodeMap[i] == '1' or nodeMap[i] == '2' or nodeMap[i] == '3':
			lightNodesAll.append(i)
	
	#flame addresses
	for i in range(0,len(nodeMap)):
		if nodeMap[i] == 'F':
			flameNodesAll.append(i)
			
	log_event("Map contains {0} light nodes...".format(len(lightNodesAll)))
	print '\nLIGHT NODES:'
	print lightNodesAll
	log_event("Map contains {0} flame nodes...".format(len(flameNodesAll)))
	print '\nFLAME NODES:'
	print flameNodesAll
	
	#logical lights
	for i in range(0, len(lightNodesAll), 3):
		lightsAll.append([lightNodesAll[i],lightNodesAll[i+1],lightNodesAll[i+2]])
	
	print '\nLIGHTS:'
	for i in range(0, len(lightsAll)):
		print 'Light {0}: '.format(i + 1) + str(lightsAll[i])
		#print lightsAll[i]
	
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
	print 'LIGHT NODES (LEFT SIDE):'
	print lightNodesLeft
	log_event("Right side has {0} light nodes...".format(len(lightNodesRight)))
	print 'LIGHTS NODES (RIGHT SIDE):'
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
	print 'FLAME NODES (LEFT SIDE):'
	print flameNodesLeft
	log_event("Right side has {0} flame nodes...".format(len(flameNodesRight)))
	print 'FLAME NODES (RIGHT SIDE):'
	print flameNodesRight	

	#init nodeStates
	for i in range(0, len(nodeMap)):
		nodeStates.append(0)
		
	setColorMap("eq")

def setColorMap(s):
	print 'RunwayControl - setting color map to: ' + s

	for i in range(0, len(lightsAll) / 2):
		if s == "eq":
			segmentLength = (len(lightsAll) / 2) / 3
			if i < segmentLength:
				#print '{0} - segment 1'.format(i)
				lightColorsLeft.append(pixelGreen)
				lightColorsRight.append(pixelGreen)
			elif i <= (segmentLength * 2):
				#print '{0} - segment 2'.format(i)
				lightColorsLeft.append(pixelYellow)
				lightColorsRight.append(pixelYellow)
			else:
				#print '{0} - segment 3'.format(i)
				lightColorsLeft.append(pixelRed)
				lightColorsRight.append(pixelRed)
		else:
			segmentLength = (len(lightsAll) / 2) / 3
			if i < segmentLength:
				#print '{0} - segment 1'.format(i)
				lightColorsLeft.append(pixelGreen)
				lightColorsRight.append(pixelGreen)
			elif i <= (segmentLength * 2):
				#print '{0} - segment 2'.format(i)
				lightColorsLeft.append(pixelPink)
				lightColorsRight.append(pixelPink)
			else:
				#print '{0} - segment 3'.format(i)
				lightColorsLeft.append(pixelBlue)
				lightColorsRight.append(pixelBlue)
	lightColorsRight.reverse()
	global lightColorsAll
	lightColorsAll = lightColorsLeft + lightColorsRight

	print 'LIGHT COLORS:'
	for i in range(0, len(lightColorsAll)):
		print '{0} - [{1},{2},{3}]'.format(i, lightColorsAll[i][0], lightColorsAll[i][1], lightColorsAll[i][2])

def showNode(n):
	if checkTick():
		nodeStates[n] = rcLightDuration + rcLightFadeTime

def showLights():
	if checkTick():
		for i in range(0,len(lightNodesAll)):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime

def showFlames():
	if checkTick():
		for i in range(0,len(flameNodesAll)):
			nodeStates[flameNodesAll[i]] = rcFlameDuration
		
def showLeftSideAll():
	global lightNodesLeft, lightNodesRight, lightNodesPerSide
	global flameNodesLeft, flameNodesRight, flameNodesPerSide
	if checkTick():
		for i in range(0,lightNodesPerSide):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime	
		for i in range(0,flameNodesPerSide):
			nodeStates[flameNodesAll[i]] = rcFlameDuration

def showRightSideAll():
	global lightNodesLeft, lightNodesRight, lightNodesPerSide
	global flameNodesLeft, flameNodesRight, flameNodesPerSide
	if checkTick():
		for i in range(lightNodesPerSide, len(lightNodesAll)):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime	
		for i in range(flameNodesPerSide , len(flameNodesAll)):
			nodeStates[flameNodesAll[i]] = rcFlameDuration

def chaseNodeSimple():
	global rcIndex1
	if checkTick():
		for i in range(0,len(lightNodesAll)):
			if i == rcIndex1:
				nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeTime
		rcIndex1 += 1
		if rcIndex1 > len(lightNodesAll):
			rcIndex1 = 0

def chaseNodeDual():
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	if checkTick():
		for i in range(0,lightNodesPerSide):
			if i == rcIndex1:
				nodeStates[lightNodesLeft[i]] = rcLightDuration + rcLightFadeTime
				nodeStates[lightNodesRight[i]] = rcLightDuration + rcLightFadeTime
		rcIndex1 += 1
		if rcIndex1 > lightNodesPerSide:
			rcIndex1 = 0

def chaseNodeDualReverse():
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	if checkTick():
		for i in range(lightNodesPerSide-1, 0, -1):
			if i == rcIndex1:
				nodeStates[lightNodesLeft[i]] = rcLightDuration + rcLightFadeTime
				nodeStates[lightNodesRight[i]] = rcLightDuration + rcLightFadeTime
		rcIndex1 -= 1
		if rcIndex1 < 0:
			rcIndex1 = lightNodesPerSide-1
		
def chaseMultiNodeDual(n):
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	if checkTick():
		if rcIndex1 > n - 1:
			rcIndex1 = 0
		for i in range(0, lightNodesPerSide - rcIndex1):
			if i % n == 0:
				nodeStates[lightNodesLeft[i + rcIndex1]] = rcLightDuration + rcLightFadeTime
				nodeStates[lightNodesRight[i + rcIndex1]] = rcLightDuration + rcLightFadeTime
		rcIndex1 += 1

def chaseLightSimple():
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

def chaseLightCircuit():
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

def chaseLightDual():
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

def chaseMultiLightDual(n):
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

def sillyRabbits1():
	global rcIndex1, rcIndex2, rcIndex3, rcIndex4, rcNextEvent1
	if checkTick():
		if time.time() > rcNextEvent1:
			rcIndex3 = random.randint(0, len(lightsAll))
			rcIndex4 = rcIndex3 + random.randint(-3, 3)
			rcIndex4 = max(min(rcIndex4, len(lightsAll)), 0)
			#print 'rcIndex3 = {0}, rcIndex4 = {1}'.format(rcIndex3, rcIndex4)
			rcNextEvent1 = time.time() + random.uniform(2.5,6.0)
		if rcIndex1 < rcIndex3:
			rcIndex1 += 1
		elif rcIndex1 > rcIndex3:
			rcIndex1 -= 1
		if rcIndex2 < rcIndex4:
			rcIndex2 += 1
		elif rcIndex2 > rcIndex4:
			rcIndex2 -= 1
		
		if abs(rcIndex1 - rcIndex2) < 5:
			#print "woah!"
			rcIndex3 = random.randint(0, len(lightsAll))

		activateLight(rcIndex1)
		activateLight(rcIndex2)

def fillUpLightsSimple():
	global rcIndex1
	if checkTick():
		if rcIndex1 > len(lightsAll):
			rcIndex1 = 0
		for i in range(0,len(lightsAll)):
			if i < rcIndex1:
				activateLight(i)
			else:
				pass
		rcIndex1 += 1		

def fillUpLightsDual():
	global rcIndex1
	if checkTick():
		if rcIndex1 > len(lightsAll)/2:
			rcIndex1 = 0
		for i in range(0,len(lightsAll)/2):
			if i < rcIndex1:
				leftI = i
				rightI = (len(lightsAll) - 1) - i
				activateLight(leftI)
				activateLight(rightI)
			else:
				pass
		rcIndex1 += 1	

def fillUpLightsDualEq(e):
	if checkTick():
		e = max(min(e, len(lightsAll)/2), 0)
		for i in range(0,len(lightsAll)/2):
			if i <= e:
				leftI = i
				rightI = (len(lightsAll) - 1) - i
				activateLight(leftI)
				activateLight(rightI)
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

def updateFingerLights(a):
	for i in range(0, len(a)):
		activateLight(a[i] - 1)

def updateFingerFlames(a):
	for i in range(0, len(a)):
		requestedFlameNumber = a[i]
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
	global lightFadeTime, pixelOn, pixelFlame, lightColorsAll, rcColorModeEq

	for i in range(0,len(nodeMap)):
		#color mapping
		if rcColorModeEq == True:
			j = float(i)/len(nodeMap)
			k = int(j * 35)
			pixelOn = lightColorsAll[k]

		if nodeStates[i] > rcLightFadeTime:
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
	
def changeAllowFlame(b):
	global rcAllowFire, pixelFlame, pixelWhite, pixelOff
	rcAllowFire = b
	if rcAllowFire == True:
		pixelFlame = pixelWhite
	else:
		pixelFlame = pixelOff
	print "RunwayControl - flame control = " + str(rcAllowFire)
	
def changeColor(c):
	global pixelOn, rcColorModeEq, rcColorModeRainbow
	print "RunwayControl - switching color to " + c
	rcColorModeRainbow = False
	rcColorModeEq = False
	if c == "default" or c == "blue":
		pixelOn = pixelBlue
	elif c == "white":
		pixelOn = pixelWhite
	elif c == "red":
		pixelOn = pixelRed
	elif c == "yellow":
		pixelOn = pixelYellow
	elif c == "green":
		pixelOn = pixelGreen
	elif c == "pink":
		pixelOn = pixelPink
	elif c == "random":
		pixelOn = getRandomColor()
	elif c == "rainbow":
		rcColorModeRainbow = True
	elif c == "eq":
		rcColorModeEq = True
	else:
		print "RunwayControl - WARNING: Unknown color " + c
		pixelOn = pixelBlue

def getRandomColor():
	i = random.randint(0,5)
	if i == 0:
		return pixelBlue
	elif i == 1:
		return pixelWhite
	elif i == 2:
		return pixelRed
	elif i == 3:
		return pixelGreen
	elif i == 4:
		return pixelYellow
	elif i == 5:
		return pixelPink
	else:
		return pixelBlue
	
def getNodeFromFlameNumber(n):
	node1 = n - 1
	return node1

def coinToss():
	if random.randint(0,1) == 0:
		return False
	else:
		return True
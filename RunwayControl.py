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
rcTick1 = 0.01666666666667
rcNextTick1 = 0
rcTick2 = 0.01666666666667
rcNextTick2 = 0
rcLightDuration = 0.05
rcFlameDuration = 0.05
rcLightFadeInTime = 0
rcLightFadeOutTime = 0.5
rcBool1 = False
rcBool2 = False
rcIndex1 = 0
rcIndex2 = 0
rcIndex3 = 0
rcIndex4 = 0
rcNextEvent1 = 0
rcColorMapEnabled = False
rcRainbowMode = False
rcAllowFire = False
pixelBuffer = []

#colors
pixelWhite = [255,255,255]
pixelBlue = [0,255,0]
pixelHalfBlue = [0,128,0]
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
	nodeMap.extend("123123123")
	
	#side 1
	for i in range(0,19):
		nodeMap.extend("F123123")
	
	#end of side 1
	nodeMap.extend("F123")

	#start side 2
	nodeMap.extend("123123F")
	
	#rest of side 2
	for i in range(0,19):
		nodeMap.extend("123123F")

	#outro
	nodeMap.extend("123123")

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
	nodeMap.extend("123123123")

	#side 1
	for i in range(0,8):
		nodeMap.extend("F123123")
		
	#start side 2
	nodeMap.extend("123F")
	
	#rest of side 2
	for i in range(0,7):
		nodeMap.extend("123123F")

	#outro
	nodeMap.extend("123123")

	#last node
	nodeMap.append('N')
	
	sharedCreate(ledStrip)

	return events

def sharedCreate(ledStrip):
	#print "nodeMap: ({0})".format(len(nodeMap))
	#print nodeMap
	
	#light addresses
	for	i in range(0,len(nodeMap)):
		if nodeMap[i] in ['1', '2', '3']:
			lightNodesAll.append(i)
	
	#flame addresses
	for i in range(0,len(nodeMap)):
		if nodeMap[i] == 'F':
			flameNodesAll.append(i)
			
	#log_event("Map contains {0} light nodes...".format(len(lightNodesAll)))
	#print '\nlightNodesAll:'
	#print lightNodesAll
	#log_event("Map contains {0} flame nodes...".format(len(flameNodesAll)))
	#print '\nflameNodesAll:'
	#print flameNodesAll
	
	#logical lights
	for i in range(0, len(lightNodesAll), 3):
		lightsAll.append([lightNodesAll[i],lightNodesAll[i+1],lightNodesAll[i+2]])
	
	#print '\nlightsAll ({0}):'.format(len(lightsAll))
	#for i in range(0, len(lightsAll)):
		#print 'Light {0}: '.format(i + 1) + str(lightsAll[i])
		#print lightsAll[i]
	
	#left and right side lights
	global lightNodesPerSide, lightsPerSide
	lightNodesPerSide = len(lightNodesAll)/2
	lightsPerSide = lightNodesPerSide/3
	#print '\nlightNodesPerSide = {0} nodes'.format(lightNodesPerSide)
	#print '\nlightsPerSide = {0} lights'.format(lightsPerSide)
	
	for i in range(0,lightNodesPerSide):	
		lightNodesLeft.append(lightNodesAll[i])
	for i in range(0, lightNodesPerSide):
		lightNodesRight.append(lightNodesAll[i+lightNodesPerSide])
		
	lightNodesRight.reverse()
		
	#log_event("Left side has {0} light nodes...".format(len(lightNodesLeft)))
	#print '\nlightNodesLeft:'
	#print lightNodesLeft
	#log_event("Right side has {0} light nodes...".format(len(lightNodesRight)))
	#print '\nlightNodesRight:'
	#print lightNodesRight
	
	#left and right side flames	
	global flameNodesPerSide, flamesPerSide
	flameNodesPerSide = len(flameNodesAll)/2
	#print '\nflameNodesPerSide = {0} nodes'.format(flameNodesPerSide)

	for i in range(0,flameNodesPerSide):
		flameNodesLeft.append(flameNodesAll[i])
	for i in range(0, flameNodesPerSide):
		flameNodesRight.append(flameNodesAll[i+flameNodesPerSide])
		
	flameNodesRight.reverse()
		
	#log_event("Left side has {0} flame nodes...".format(len(flameNodesLeft)))
	#print '\nflameNodesLeft:'
	#print flameNodesLeft
	#log_event("Right side has {0} flame nodes...".format(len(flameNodesRight)))
	#print '\nflameNodesRight:'
	#print flameNodesRight
	
	constructLightsAndFireArrays()

	#init nodeStates
	for i in range(0, len(nodeMap)):
		nodeStates.append(0)
		
	setColorMap("eq")
	
	#init pixel buffer
	for i in range(0, len(nodeMap)):
		pixelBuffer.append(pixelOff)

def constructLightsAndFireArrays():
	global lightsAndFire, lightsAndFireLeft, lightsAndFireRight
	lightIndex = 0
	fireIndex = 0
	
	for c in nodeMap:
		if c == '1':
			lightsAndFire.append(['L', lightIndex])
			lightIndex += 1
		elif c == 'F':
			lightsAndFire.append(['F', fireIndex])
			fireIndex += 1
		else:
			pass

	#print '\nlightsAndFire ({0}):'.format(len(lightsAndFire))
	#print lightsAndFire
	
	for i in range(0, len(lightsAndFire)):
		if i < len(lightsAndFire) / 2:
			lightsAndFireLeft.append(lightsAndFire[i])
		else:
			lightsAndFireRight.append(lightsAndFire[i])
	
	lightsAndFireRight.reverse()
	
	#print '\nlightsAndFireLeft ({0}):'.format(len(lightsAndFireLeft))
	#print lightsAndFireLeft
	#print '\nlightsAndFireRight ({0}):'.format(len(lightsAndFireRight))
	#print lightsAndFireRight

def setColorMap(s):
	#print 'RunwayControl - setting color map to: ' + s

	global lightColorsAll, lightColorsLeft, lightColorsRight
	lightColorsAll = []
	lightColorsLeft = []
	lightColorsRight = []
	
	b = False

	for i in range(0, len(lightsAll) / 2):
		if s == "eq":
			segmentLength = (len(lightsAll) / 2) / 3
			if i < segmentLength:
				##print '{0} - segment 1'.format(i)
				lightColorsLeft.append(pixelGreen)
				lightColorsRight.append(pixelGreen)
			elif i <= (segmentLength * 2):
				##print '{0} - segment 2'.format(i)
				lightColorsLeft.append(pixelBlue)
				lightColorsRight.append(pixelBlue)
			else:
				##print '{0} - segment 3'.format(i)
				lightColorsLeft.append(pixelRed)
				lightColorsRight.append(pixelRed)
		elif s == 'checker':
			if b == True:
				lightColorsLeft.append(pixelGreen)
				lightColorsRight.append(pixelGreen)
				b = False
			else:
				lightColorsLeft.append(pixelBlue)
				lightColorsRight.append(pixelBlue)
				b = True
		else:
			segmentLength = (len(lightsAll) / 2) / 3
			if i < segmentLength:
				##print '{0} - segment 1'.format(i)
				lightColorsLeft.append(pixelGreen)
				lightColorsRight.append(pixelGreen)
			elif i <= (segmentLength * 2):
				##print '{0} - segment 2'.format(i)
				lightColorsLeft.append(pixelRed)
				lightColorsRight.append(pixelRed)
			else:
				##print '{0} - segment 3'.format(i)
				lightColorsLeft.append(pixelBlue)
				lightColorsRight.append(pixelBlue)
	lightColorsRight.reverse()
	lightColorsAll = lightColorsLeft + lightColorsRight

	#print 'lightColorsAll {0}:'.format(len(lightColorsAll))
	#for i in range(0, len(lightColorsAll)):
		#print '{0} - [{1},{2},{3}]'.format(i, lightColorsAll[i][0], lightColorsAll[i][1], lightColorsAll[i][2])

def showNode(n):
	if checkTick1():
		nodeStates[n] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime

def showLights():
	if checkTick1():
		for i in range(0,len(lightNodesAll)):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime

def showFlames():
	if checkTick1():
		for i in range(0,len(flameNodesAll)):
			nodeStates[flameNodesAll[i]] = rcFlameDuration
		
def showLeftSideAll():
	global lightNodesLeft, lightNodesRight, lightNodesPerSide
	global flameNodesLeft, flameNodesRight, flameNodesPerSide
	if checkTick1():
		for i in range(0,lightNodesPerSide):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime	
		for i in range(0,flameNodesPerSide):
			nodeStates[flameNodesAll[i]] = rcFlameDuration

def showRightSideAll():
	global lightNodesLeft, lightNodesRight, lightNodesPerSide
	global flameNodesLeft, flameNodesRight, flameNodesPerSide
	if checkTick1():
		for i in range(lightNodesPerSide, len(lightNodesAll)):
			nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime	
		for i in range(flameNodesPerSide , len(flameNodesAll)):
			nodeStates[flameNodesAll[i]] = rcFlameDuration

def chaseNodeSimple():
	global rcIndex1
	if checkTick1():
		for i in range(0,len(lightNodesAll)):
			if i == rcIndex1:
				nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
		rcIndex1 += 1
		if rcIndex1 > len(lightNodesAll):
			rcIndex1 = 0

def chaseNodeDual():
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	if checkTick1():
		if rcIndex1 > lightNodesPerSide:
			rcIndex1 = 0
		for i in range(0,lightNodesPerSide):
			if i == rcIndex1:
				nodeStates[lightNodesLeft[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
				nodeStates[lightNodesRight[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
		rcIndex1 += 1

def chaseNodeDualReverse():
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	if checkTick1():
		if rcIndex1 < 0:
			rcIndex1 = lightNodesPerSide
		for i in range(0, lightNodesPerSide):
			if i == rcIndex1:
				nodeStates[lightNodesLeft[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
				nodeStates[lightNodesRight[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
		rcIndex1 -= 1
		
def chaseMultiNodeDual(n):
	global rcIndex1, lightNodesLeft, lightNodesRight, lightNodesPerSide
	if checkTick1():
		if rcIndex1 > n - 1:
			rcIndex1 = 0
		for i in range(0, lightNodesPerSide - rcIndex1):
			if i % n == 0:
				nodeStates[lightNodesLeft[i + rcIndex1]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
				nodeStates[lightNodesRight[i + rcIndex1]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
		rcIndex1 += 1

def chaseLightSimple():
	#light simple chaser
	global rcIndex1
	if checkTick1():
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
	if checkTick1():
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
	if checkTick1():
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

def chaseLightDualBounce():
	#light dual chaser with bounce
	global rcIndex1, rcBool1
	if checkTick1():
		if rcBool1 == True:
			if rcIndex1 >= len(lightsAll)/2:
				rcBool1 = False
			for i in range(0,len(lightsAll)/2):
				if i == rcIndex1:
					leftI = i
					rightI = (len(lightsAll) - 1) - i
					activateLight(leftI)
					activateLight(rightI)
				else:
					pass
			if rcBool1 == True:		
				rcIndex1 += 1
		else:
			if rcIndex1 <= 0:
				rcBool1 = True
			for i in range(0,len(lightsAll)/2):
				if i == rcIndex1:
					leftI = i
					rightI = (len(lightsAll) - 1) - i
					activateLight(leftI)
					activateLight(rightI)
				else:
					pass
			if rcBool1 == False:
				rcIndex1 -= 1

def chaseMultiLightDual(n):
	#light dual chaser, every n lights
	global rcIndex1
	if checkTick1():
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
		
def chaseMultiLight(n):
	#light chaser, every n lights
	global rcIndex1
	if checkTick1():
		if rcIndex1 > n - 1:
			rcIndex1 = 0
		for i in range(0,(len(lightsAll)) - rcIndex1):
			if i % n == 0:

				activateLight(i + rcIndex1)
			else:
				pass
		rcIndex1 += 1

def twinkleAllLights():
	if checkTick1():
		for i in range(0,len(lightsAll)):
			if coinToss(1) == True:
				activateLight(i)
			else:
				pass

def showLogicalLight(n):
	if checkTick1():
		for i in range(0,len(lightsAll)):
			if i == n:
				activateLight(i)
			else:
				pass

def sillyRabbits1():
	global rcIndex1, rcIndex2, rcIndex3, rcIndex4, rcNextEvent1
	if checkTick1():
		if time.time() > rcNextEvent1:
			rcIndex3 = random.randint(0, len(lightsAll) - 1)
			rcIndex4 = rcIndex3 + random.randint(-3, 3)
			rcIndex4 = max(min(rcIndex4, len(lightsAll)) - 1, 0)
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
	if checkTick1():
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
	if checkTick1():
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
	if checkTick1():
		e = max(min(e, len(lightsAll)/2), 0)
		for i in range(0,len(lightsAll)/2):
			if i <= e:
				leftI = i
				rightI = (len(lightsAll) - 1) - i
				activateLight(leftI)
				activateLight(rightI)
			else:
				pass

def fillUpLightsDualEqFake():
	if checkTick1():
		e = random.randint(0,len(lightsAll)/2)
		for i in range(0,len(lightsAll)/2):
			if i <= e:
				leftI = i
				rightI = (len(lightsAll) - 1) - i
				activateLight(leftI)
				activateLight(rightI)
			else:
				pass

def lightAndFireChaserSimple():
	global rcIndex1
	if checkTick1():
		if rcIndex1 > len(lightsAndFire):
			rcIndex1 = 0
		for i in range(0,len(lightsAndFire)):
			if i == rcIndex1:
				if lightsAndFire[i][0] == 'F':
					activateFlame(lightsAndFire[i][1] + 1)
				elif lightsAndFire[i][0] == 'L':
					activateLight(lightsAndFire[i][1])
		rcIndex1 += 1

def lightAndFireChaserLeft():
	global rcIndex1
	chaseLength = len(lightsAndFireLeft) - 1	
	if checkTick1():
		if rcIndex1 > chaseLength:
			rcIndex1 = 0
		for i in range(0,chaseLength):
			if i == rcIndex1:
				if lightsAndFireLeft[i][0] == 'L':
					activateLight(lightsAndFireLeft[i][1])

				#if next index is fire, light it now and skip next node
				if lightsAndFireLeft[i + 1][0] == 'F':
					activateFlame(lightsAndFireLeft[i + 1][1] + 1)
					rcIndex1 += 1
		rcIndex1 += 1

def lightAndFireChaserRight():
	global rcIndex2
	chaseLength = len(lightsAndFireRight) - 1	
	if checkTick2():
		if rcIndex2 > chaseLength:
			rcIndex2 = 0
		for i in range(0,chaseLength):
			if i == rcIndex2:
				if lightsAndFireRight[i][0] == 'L':
					activateLight(lightsAndFireRight[i][1])

				#if this index is fire, light it and next light now
				#then skip ahead by 1
				if lightsAndFireRight[i][0] == 'F':
					activateFlame(lightsAndFireRight[i][1] + 1)
					activateLight(lightsAndFireRight[i + 1][1])
					rcIndex2 += 1
		rcIndex2 += 1

def lightAndFireChaserLeftReverse():
	global rcIndex1
	chaseLength = len(lightsAndFireLeft) - 1	
	if checkTick1():
		if rcIndex1 < 0:
			rcIndex1 = chaseLength
		for i in range(0,chaseLength):
			if i == rcIndex1:
				if lightsAndFireLeft[i][0] == 'L':
					activateLight(lightsAndFireLeft[i][1])

				#if this index is fire, light it and next light now
				#then skip ahead by 1
				if lightsAndFireLeft[i][0] == 'F':
					activateFlame(lightsAndFireLeft[i][1] + 1)
					activateLight(lightsAndFireLeft[i - 1][1])
					rcIndex1 -= 1
		rcIndex1 -= 1

def lightAndFireChaserRightReverse():
	global rcIndex2
	chaseLength = len(lightsAndFireRight) - 1	
	if checkTick2():
		if rcIndex2 < 0:
			rcIndex2 = chaseLength
		for i in range(0,chaseLength):
			if i == rcIndex2:
				if lightsAndFireRight[i][0] == 'L':
					activateLight(lightsAndFireRight[i][1])

				#if next index is fire, light it now and skip next node
				if lightsAndFireRight[i - 1][0] == 'F':
					activateFlame(lightsAndFireRight[i - 1][1] + 1)
					rcIndex2 -= 1
		rcIndex2 -= 1

def lightAndFireChaserLeftBounce():
	global rcIndex1, rcBool1
	chaseLength = len(lightsAndFireLeft) - 1	
	if checkTick1():
		if rcBool1 == True:
			if rcIndex1 > chaseLength:
				rcBool1 = False	
			for i in range(0,chaseLength):
				if i == rcIndex1:
					if lightsAndFireLeft[i][0] == 'L':
						activateLight(lightsAndFireLeft[i][1])

					#if next index is fire, light it now and skip next node
					if lightsAndFireLeft[i + 1][0] == 'F':
						activateFlame(lightsAndFireLeft[i + 1][1] + 1)
						rcIndex1 += 1
			if rcBool1 == True:
				rcIndex1 += 1
		else:
			if rcIndex1 < 0:
				rcBool1 = True
			for i in range(0,chaseLength):
				if i == rcIndex1:
					if lightsAndFireLeft[i][0] == 'L':
						activateLight(lightsAndFireLeft[i][1])

					#if this index is fire, light it and next light now
					#then skip ahead by 1
					if lightsAndFireLeft[i][0] == 'F':
						activateFlame(lightsAndFireLeft[i][1] + 1)
						activateLight(lightsAndFireLeft[i - 1][1])
						rcIndex1 -= 1
			if rcBool1 == False:
				rcIndex1 -= 1

def lightAndFireChaserRightBounce():
	global rcIndex2, rcBool2
	chaseLength = len(lightsAndFireRight) - 1	
	if checkTick2():
		if rcBool2 == True:
			if rcIndex2 > chaseLength:
				rcBool2 = False
			for i in range(0,chaseLength):
				if i == rcIndex2:
					if lightsAndFireRight[i][0] == 'L':
						activateLight(lightsAndFireRight[i][1])

					#if this index is fire, light it and next light now
					#then skip ahead by 1
					if lightsAndFireRight[i][0] == 'F':
						activateFlame(lightsAndFireRight[i][1] + 1)
						activateLight(lightsAndFireRight[i + 1][1])
						rcIndex2 += 1
			if rcBool2 == True:
				rcIndex2 += 1
		else:
			if rcIndex2 < 0:
				rcBool2 = True
			for i in range(0,chaseLength):
				if i == rcIndex2:
					if lightsAndFireRight[i][0] == 'L':
						activateLight(lightsAndFireRight[i][1])

					#if next index is fire, light it now and skip next node
					if lightsAndFireRight[i - 1][0] == 'F':
						activateFlame(lightsAndFireRight[i - 1][1] + 1)
						rcIndex2 -= 1
			if rcBool2 == False:
				rcIndex2 -= 1

def twinkleAllFlames():
	if checkTick2():
		for i in range(0,len(flameNodesAll)):
			if coinToss(1) == True:
				activateFlame(i)
			else:
				pass

def twinkleAllLightsRandomFade():
	global rcLightFadeOutTime
	if checkTick1():
		for i in range(0,len(lightsAll)):
			if coinToss(3) == True:
				rcLightFadeOutTime = random.uniform(0.2, 2.0)
				activateLight(i)
			else:
				pass

def twinkleOneFlame():
	if checkTick2():
		luckyWinner = random.randint(0,len(flameNodesAll))
		for i in range(0,len(flameNodesAll)):
			if i == luckyWinner:
				activateFlame(i)
			else:
				pass

def twinkleOneLight():
	if checkTick1():
		luckyWinner = random.randint(0,len(lightsAll))
		for i in range(0,len(lightsAll)):
			if i == luckyWinner:
				activateLight(i)
			else:
				pass

def twinkleAllLightNodes():
	if checkTick1():
		for i in range(0,len(lightNodesAll)):
			if coinToss(5) == True:
				nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
			else:
				pass

def lightningSync():
	if checkTick1():
		if coinToss(3) == True:
			for i in range(0,len(lightNodesAll)):
				nodeStates[lightNodesAll[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
			else:
				pass

def lightningSides():
	if checkTick1():
		if coinToss(3) == True:
			for i in range(0,len(lightNodesLeft)):
				nodeStates[lightNodesLeft[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
			else:
				pass
		if coinToss(3) == True:
			for i in range(0,len(lightNodesRight)):
				nodeStates[lightNodesRight[i]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
			else:
				pass

def chaseFlames():
	global rcIndex1
	if checkTick1():
		if rcIndex1 > len(flameNodesAll):
			rcIndex1 = 0
		for i in range(0,len(flameNodesAll)):
			if i == rcIndex1:
				nodeStates[flameNodesAll[i]] = rcFlameDuration
		rcIndex1 += 1

def chaseFlamesDual():
	global rcIndex2
	if checkTick2():
		if rcIndex2 > len(flameNodesAll)/2:
			rcIndex2 = 0
		for i in range(0,len(flameNodesAll)/2):
			if i == rcIndex2:
				leftI = i
				rightI = (len(flameNodesAll) - 1) - i
				activateFlame(leftI + 1)
				activateFlame(rightI + 1)
			else:
				pass
		rcIndex2 += 1

def chaseMultiFlamesDual(n):
	#flames dual chaser, every n flames
	global rcIndex2
	if checkTick2():
		if n > len(flameNodesAll)/2:
			n = len(flameNodesAll)/2
		if rcIndex2 > n - 1:
			rcIndex2 = 0
		for i in range(0,(len(flameNodesAll)/2) - rcIndex2):
			if i % n == 0:
				leftI = i + rcIndex2
				rightI = ((len(flameNodesAll) - 1) - i) - rcIndex2
				activateFlame(leftI + 1)
				activateFlame(rightI + 1)
			else:
				pass
		rcIndex2 += 1

def chaseMultiFlamesDualReverse(n):
	#reverse flames dual chaser, every n flames
	global rcIndex2
	if checkTick2():
		if n > len(flameNodesAll)/2:
			n = len(flameNodesAll)/2
		if rcIndex2 < 0:
			rcIndex2 = n - 1
		for i in range(0,(len(flameNodesAll)/2) - rcIndex2):
			if i % n == 0:
				leftI = i + rcIndex2
				rightI = ((len(flameNodesAll) - 1) - i) - rcIndex2
				activateFlame(leftI + 1)
				activateFlame(rightI + 1)
			else:
				pass
		rcIndex2 -= 1

def chaseFlamesDualReverse():
	global rcIndex2
	if checkTick2():
		if rcIndex2 < 0:
			rcIndex2 = len(flameNodesAll)/2
		for i in range(0,len(flameNodesAll)/2):
			if i == rcIndex2:
				leftI = i
				rightI = (len(flameNodesAll) - 1) - i
				activateFlame(leftI + 1)
				activateFlame(rightI + 1)
			else:
				pass
		rcIndex2 -= 1

def chaseFlamesDualBounce():
	global rcIndex2, rcBool2
	if checkTick2():
		if rcBool2 == True:
			if rcIndex2 > (len(flameNodesAll)/2) -1:
				rcBool2 = False
			for i in range(0,len(flameNodesAll)/2):
				if i == rcIndex2:
					leftI = i
					rightI = (len(flameNodesAll) - 1) - i
					activateFlame(leftI + 1)
					activateFlame(rightI + 1)
				else:
					pass
			if rcBool2 == True:			
				rcIndex2 += 1
		else:
			if rcIndex2 < 0:
				rcBool2 = True
			for i in range(0,len(flameNodesAll)/2):
				if i == rcIndex2:
					leftI = i
					rightI = (len(flameNodesAll) - 1) - i
					activateFlame(leftI + 1)
					activateFlame(rightI + 1)
				else:
					pass
			if rcBool2 == False:					
				rcIndex2 -= 1			

def clear():
	for i in range(0,len(nodeMap)):
		nodeStates[i] = 0

def clearImmediate(ledStrip):
	print 'RunwayControl - clearImmediate()'
	clear()
	update(ledStrip)

def decrementDurations(t):
	for i in range(0,len(nodeMap)):
		nodeStates[i] -= t

def updateFingerLights(a):
	for i in range(0, len(a)):
		activateLight(a[i] - 1)

def updateFingerFlames(a):
	for i in range(0, len(a)):
		activateFlame(a[i])

def checkTick1():
	global rcTick1, rcNextTick1
	if time.time() > rcNextTick1:
		rcNextTick1 = time.time() + rcTick1
		return True
	else:
		return False

def checkTick2():
	global rcTick2, rcNextTick2
	if time.time() > rcNextTick2:
		rcNextTick2 = time.time() + rcTick2
		return True
	else:
		return False

def activateLight(i):
	#print 'RunwayControl - activateLight {0}'.format(i)
	try:
		nodeStates[lightsAll[i][0]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
	except:
		pass
		#print "activateLight - ERROR: Light {0}, node 0 doesn't exist".format(i)
	try:
		nodeStates[lightsAll[i][1]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
	except:
		pass
		#print "activateLight - ERROR: Light {0}, node 1 doesn't exist".format(i)
	try:
		nodeStates[lightsAll[i][2]] = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime
	except:
		pass
		#print "activateLight - ERROR: Light {0}, node 2 doesn't exist".format(i)

def activateFlame(i):
	#print 'RunwayControl - activateFlame {0}'.format(i)
	requestedFlameNumber = i
	requestedFlameNode = getNodeFromFlameNumber(requestedFlameNumber)
	nodeStates[flameNodesAll[requestedFlameNode]] = rcFlameDuration

def update(ledStrip):
	global rcLightFadeOutTime, rcLightFadeInTime, pixelOn, pixelFlame, lightColorsAll, rcColorMapEnabled, rcRainbowMode

	effectiveLightDuration = rcLightDuration + rcLightFadeOutTime + rcLightFadeInTime

	for i in xrange(0,len(nodeMap)):
		#color mapping
		if rcColorMapEnabled == True:
			j = float(i)/len(nodeMap)
			k = int(j * len(lightColorsAll)-1)
			pixelOn = lightColorsAll[k]

		if nodeStates[i] > effectiveLightDuration - rcLightFadeInTime and rcLightFadeInTime > 0:
			if nodeMap[i] == 'F':
				ledStrip.setPixel(i, pixelFlame)
			else:
				fadeAmount = 0
				nodeTime = effectiveLightDuration - nodeStates[i]
				if nodeTime > 0:
					fadeAmount = nodeTime/rcLightFadeInTime
				r, g, b = pixelOn
				p = int(fadeAmount * 255)
				if r > 0:
					r = p
				if g > 0:
					g = p
				if b > 0:
					b = p
				ledStrip.setPixel(i, [r,g,b])
		elif nodeStates[i] > rcLightFadeOutTime:
			if nodeMap[i] == 'F':
				ledStrip.setPixel(i, pixelFlame)
			else:
				if rcRainbowMode == True:
					pixelOn = getRandomColor()
				ledStrip.setPixel(i, pixelOn)
		elif nodeStates[i] > 0 and nodeStates[i] <= rcLightFadeOutTime:
			if nodeMap[i] == 'F':
				ledStrip.setPixel(i, pixelFlame)
			else:
				r = pixelOn[0]
				g = pixelOn[1]
				b = pixelOn[2]
				p = int(nodeStates[i]/rcLightFadeOutTime * 255)
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
	#time.sleep(0)

def syncIndices():
	#print 'RunwayControl - syncIndices'
	global rcIndex1, rcIndex2, rcIndex3, rcIndex4
	rcIndex1 = 0
	rcIndex2 = 0
	rcIndex3 = 0
	rcIndex4 = 0

def syncIndices2():
	#print 'RunwayControl - hackIndices'
	global rcIndex1, rcIndex2, rcIndex3, rcIndex4
	rcIndex1 = 0
	rcIndex2 = 0
	rcIndex3 = 0
	rcIndex4 = 0

def changeTick(n):
	global rcTick1, rcTick2
	rcTick1 = max(min(n, 20.0), 0.01)
	rcTick2 = max(min(n, 20.0), 0.01)
	rcNextTick1 = 0 #apply next update
	rcNextTick2 = 0 #apply next update
	print "RunwayControl - tick is now {0}".format(rcTick1)
	
def changeLightFadeTime(n):
	global rcLightFadeOutTime
	rcLightFadeOutTime = max(min(n, 10.0), 0)
	print "RunwayControl - light fade out is now {0}".format(rcLightFadeOutTime)

def changeLightFadeInTime(n):
	global rcLightFadeInTime
	rcLightFadeInTime = max(min(n, 2.0), 0)
	print "RunwayControl - light fade in is now {0}".format(rcLightFadeInTime)

def changeLightDuration(n):
	global rcLightDuration
	rcLightDuration = max(min(n, 10.0), 0.0005)
	print "RunwayControl - light duration is now {0}".format(rcLightDuration)
	
def changeFlameDuration(n):
	global rcFlameDuration
	rcFlameDuration = max(min(n, 3.0), 0.005)
	print "RunwayControl - flame duration is now {0}".format(rcFlameDuration)
	
def changeAllowFlame(b):
	global rcAllowFire, pixelFlame, pixelWhite, pixelRed, pixelOff
	rcAllowFire = b
	if rcAllowFire == True:
		pixelFlame = pixelRed
	else:
		pixelFlame = pixelOff
	print "RunwayControl - flame control = " + str(rcAllowFire)
	
def changeColor(c):
	global pixelOn, rcColorMapEnabled, rcRainbowMode
	print "RunwayControl - switching color to " + c
	rcColorMapEnabled = False
	rcRainbowMode = False
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
		rcRainbowMode = True
		changeLightFadeTime(0)
		changeLightFadeInTime(0)
	elif c == "eq":
		setColorMap("eq")
		rcColorMapEnabled = True
	elif c == "checker":
		setColorMap("checker")
		rcColorMapEnabled = True
	elif c == "halfBlue":
		pixelOn = pixelHalfBlue
	else:
		print "RunwayControl - WARNING: Unknown color " + c
		pixelOn = pixelBlue

def getRandomColor():
	i = random.randint(0,2)
	if i == 0:
		return pixelBlue
	elif i == 1:
		return pixelRed
	elif i == 2:
		return pixelGreen
	else:
		return pixelBlue
	
def getNodeFromFlameNumber(n):
	node1 = n - 1
	return node1

def coinToss(n):
	if random.randint(0,n) == 0:
		return True
	else:
		return False
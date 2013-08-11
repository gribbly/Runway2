import sys
import math
import time
from random import randint

nodemap = []
allLights = []
allFlames = []

nodestates = []

events = []

rcTick = 2.0
nextRcTick = 0
rcBool = False
rcIndex = 0

pixelWhite = [255,255,255]
pixelBlue = [0,255,0]
pixelYellow = [255,255,0]
pixelRed = [255,0,0]
pixelGreen = [0,0,255]
pixelOff = [0,0,0]

def log_event(msg):
	events.append(msg)
	

def create(ledStrip):
	log_event('creating node array [{0} nodes total]'.format(ledStrip.nLeds))

	#first node
	nodemap.append('N')
	
	#intro
	nodemap.append('1')
	nodemap.append('2')
	nodemap.append('3')
	nodemap.append('1')
	nodemap.append('2')
	nodemap.append('3')
	
	#side 1
	for i in range(0,20):
		nodemap.append('F')
		nodemap.append('1')
		nodemap.append('2')
		nodemap.append('3')
		nodemap.append('1')
		nodemap.append('2')
		nodemap.append('3')
	
	#side 2
	for i in range(0,20):
		nodemap.append('1')
		nodemap.append('2')
		nodemap.append('3')
		nodemap.append('1')
		nodemap.append('2')
		nodemap.append('3')
		nodemap.append('F')

	#outro
	nodemap.append('1')
	nodemap.append('2')
	nodemap.append('3')
	nodemap.append('1')
	nodemap.append('2')
	nodemap.append('3')

	#last node
	nodemap.append('N')
	
	for i in range(0,len(nodemap)):
		print format(i) + " " + nodemap[i]
	
	#light addresses
	for	i in range(0,ledStrip.nLeds - 1):
		if nodemap[i] == '1':
			allLights.append(i)
	
	#flame addresses
	for i in range(0,ledStrip.nLeds - 1):
		if nodemap[i] == 'F':
			allFlames.append(i)
			
	log_event("Map contains {0} lights...".format(len(allLights)))
	print allLights
	log_event("Map contains {0} flames...".format(len(allFlames)))
	print allFlames
	
	#init nodestates
	for i in range(0, len(nodemap)):
		nodestates.append(False)

	return events

def flamesBlink():
	global rcBool
	for i in range(0,len(allFlames)):
		nodestates[allFlames[i]] = rcBool
		if rcBool == True:
			rcBool = False
		else:
			rcBool = True
			
def flamesChase():
	global rcTick, nextRcTick
	if time.time() > nextRcTick:
		nextRcTick = time.time() + rcTick
	
		for i in range(0,len(allFlames)):
			if i == rcIndex:
				nodestates[allFlames[i]] = True
			else:
				nodestates[allFlames[i]] = True
				
def randomFlames():
	global rcTick, nextRcTick
	if time.time() > nextRcTick:
		nextRcTick = time.time() + rcTick

		for i in range(0,len(allFlames)):
			nodestates[allFlames[i]] = coinToss()

def update(ledStrip):
	for i in range(0, ledStrip.nLeds):
		if nodestates[i] == True:
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
#tweaks
nodes = 292 #should be 292
camTestRig = False #should be False
useRunwayControl = True #should be True
fakeMode = False #should be False
noServer = False #should be False

#starting values for realtime vars (app can change these)
startColor = "blue"
startPattern = 11 #tbd
adjustableTick = 0.2 #starting value
lightDuration = 0.05 #should be 0.05
flameDuration = 0.05 #should be 0.05
lightFadeTime = 0.2 #should be 0.2
lightGap = 3
lightEq = 0

#internal stuff (don't change this)
fixedTick = 0.01666666666667 #60fps
fingerLights = []
fingerFlames = []
debugTickCounter = 0
clearCounter = 0
appConnectTimer = -1
appConnected = False

import sys
import time
import random
if fakeMode == False:
	from LedStrip_WS2801 import LedStrip_WS2801
else:
	from LedStrip_WS2801 import LedStrip_Fake
import Patterns
import RunwayControl

# queues
from subprocess import PIPE, Popen
from threading  import Thread
from Queue import Queue, Empty

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
# /queues

def log_event(msg):
	f.write(format(time.time()) + ": " + msg + "\n")
	print format(time.time()) + ": " + msg
	pass	

#START
f = open('log','w')
log_event('HELLO WORLD @ {0}'.format(time.time()))

if fakeMode == False:
	log_event('starting in REAL mode')
	ledStrip = LedStrip_WS2801("/dev/spidev0.0", nodes)
else:
	print '*** WARNING: fakeMode is True ***'
	log_event('starting in FAKE mode')
	ledStrip = LedStrip_Fake(nodes)
	fixedTick = 1.0

pattern = startPattern
if len(sys.argv) > 1:
	try:
		pattern = int(sys.argv[1])
	except:
		log_event('WARNING! Bad pattern arg {0}'.format(sys.argv[1]))

debugN = 0 #used for pattern 0 and 12 in runwayMode
if len(sys.argv) > 2:
	try:
		debugN = int(sys.argv[2])
	except:
		log_event('WARNING! Bad arg {0} {1}'.format(sys.argv[1], sys.argv[2]))

if noServer == False:
	log_event('starting SuperSimple.py @ {0}'.format(time.time()))
	p = Popen(['./SuperSimple.py'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
	q = Queue()
	t = Thread(target=enqueue_output, args=(p.stdout, q))
	t.daemon = True # thread dies with the program
	t.start()
	log_event('started SuperSimple.py @ {0}'.format(time.time()))

log_event('fixedTick is {0}'.format(fixedTick))
log_event('adjustableTick is {0}'.format(adjustableTick))
log_event('pattern is {0}'.format(pattern))

nextFixedTick = 0

log_event('we have {0} ws2801 nodes'.format(ledStrip.nLeds))
log_event('clear strip @ {0}'.format(time.time()))
Patterns.clearAll(ledStrip)

if useRunwayControl == True:
	if camTestRig == True:
		output = RunwayControl.createCamTestRig(ledStrip)
	else:
		output = RunwayControl.create(ledStrip)
	for line in output:
		if line is not None:
			log_event(line)
			
RunwayControl.changeTick(adjustableTick)
RunwayControl.changeLightDuration(lightDuration)
RunwayControl.changeFlameDuration(flameDuration)
RunwayControl.changeLightFadeTime(lightFadeTime)
RunwayControl.changeColor(startColor)
RunwayControl.changeAllowFlame(False)

while True:	
	if noServer == False:
		try:  
			line = q.get_nowait() 
			#line = q.get(timeout=.1)
		except Empty:
			pass
		else: # got line
			appConnectTimer = 20
			if appConnected == False:
				appConnected = True
				RunwayControl.changeAllowFlame(True)

			line = line.strip()
			appInput = line.split(',')
			print appInput

			for input in appInput:
				command = input.split('=')
				if len(command) < 2:
					break #filter out commands that aren't in the form x=y

				if command[0] == 'alive':
					try: 
						pass
					except:
						log_event('Bad alive input: ' + str(line))		
				if command[0] == 'tick':
					try: 
						#log_event('Got tick command')
						adjustableTick = float(command[1].rstrip())
						RunwayControl.changeTick(adjustableTick)
					except:
						log_event('Bad tick input: ' + str(line))
				elif command[0] == 'pattern':
					try:
						#log_event('Got pattern command')
						pattern = int(command[1].rstrip())
						if useRunwayControl == False:
							Patterns.resetSharedVars()
					except:
						log_event('Bad pattern input: ' + str(line))
				elif command[0] == 'light' or command[0] == 'l':
					try: 
						fingerLights.append(int(command[1].rstrip()))
					except:
						log_event('Bad light input: ' + str(line))
				elif command[0] == 'fire':
					try: 
						fingerFlames.append(int(command[1].rstrip()))
					except:
						log_event('Bad fire input: ' + str(line))
				elif command[0] == 'ld':
					try: 
						RunwayControl.changeLightDuration(int(command[1].rstrip()))
					except:
						log_event('Bad light duration input: ' + str(line))
				elif command[0] == 'fd':
					try:
						RunwayControl.changeFlameDuration(int(command[1].rstrip()))
					except:
						log_event('Bad flame duration input: ' + str(line))
				elif command[0] == 'fadetime':
					try:
						RunwayControl.changeLightFadeTime(int(command[1].rstrip()))
					except:
						log_event('Bad light fade time input: ' + str(line))
				elif command[0] == 'lightgap':
					try:
						lightGap = (int(command[1].rstrip()))
						if lightGap < 1:
							lightGap = 1
					except:
						log_event('Bad lightgap: ' + str(line))
				elif command[0] == 'color':
					try:
						RunwayControl.changeColor(int(command[1].rstrip()))
					except:
						log_event('Bad color: ' + str(line))
				elif command[0] == 'eq':
					try:
						RunwayControl.changeColor(int(command[1].rstrip()))
					except:
						log_event('Bad color: ' + str(line))	
				elif command[0] == 'clear':
					try:
						RunwayControl.clearImmediate()
						fingerLights = []
						fingerFlames = []
					except:
						log_event('Bad clear input: ' + str(line))

	if time.time() > nextFixedTick:
		nextFixedTick = time.time() + fixedTick
		
		if appConnectTimer > -1:
			appConnectTimer -= fixedTick
			if appConnectTimer < 5:
				print 'appConnectTimer = {0:.2f}'.format(appConnectTimer)
		else:
			if appConnected == True:
				appConnected = False
				RunwayControl.changeAllowFlame(False)

		if useRunwayControl == True:
			RunwayControl.decrementDurations(fixedTick)
		
			if pattern == -1:
				RunwayControl.clear()				
			if pattern == 0: #debugging
				RunwayControl.showNode(debugN)
			elif pattern == 1:
				RunwayControl.showLights()
			elif pattern == 2:
				RunwayControl.showFlames()
			elif pattern == 3:
				RunwayControl.showLeftSideAll()		
			elif pattern == 4:
				RunwayControl.showRightSideAll()
			elif pattern == 5:
				RunwayControl.chaseNodeSimple()	
			elif pattern == 6:
				RunwayControl.chaseNodeDual()
			elif pattern == 7:
				RunwayControl.chaseNodeDualReverse()
			elif pattern == 8:
				RunwayControl.chaseMultiNodeDual(lightGap)
			elif pattern == 9:
				RunwayControl.chaseLightSimple()
			elif pattern == 10:
				RunwayControl.chaseLightCircuit()
			elif pattern == 11:
				RunwayControl.twinkleAllLights()
			elif pattern == 12: #debugging
				RunwayControl.showLogicalLight(debugN)
			elif pattern == 13:
				RunwayControl.chaseLightDual()				
			elif pattern == 14:
				RunwayControl.chaseMultiLightDual(lightGap)
			elif pattern == 15:
				RunwayControl.sillyRabbits1()
			elif pattern == 16:
				RunwayControl.fillUpLightsSimple()
			elif pattern == 17:
				RunwayControl.fillUpLightsDual()
			elif pattern == 18: 
				if camTestRig == True:
					lightEq = random.randint(0,18)
				RunwayControl.fillUpLightsDualEq(lightEq)
				
			else:
				log_event('WARNING! bad pattern number {0}'.format(pattern))
				pattern = 1 #set to something sane

			if len(fingerLights) > 0:
				RunwayControl.updateFingerLights(fingerLights)
			if len(fingerFlames) > 0:
				RunwayControl.updateFingerFlames(fingerFlames)
				
			RunwayControl.update(ledStrip)
			
			fingerLights = []
			fingerFlames = []
	
		else:
			if pattern == -1:
				pass
			elif pattern == 0:
				Patterns.clearAll(ledStrip)
			elif pattern == 1:
				Patterns.randomString(ledStrip)
			elif pattern == 2:
				Patterns.randomPoint(ledStrip)
			elif pattern == 3:
				Patterns.simpleChaser(ledStrip)
			elif pattern == 4:
				Patterns.cylonChaser(ledStrip)
			elif pattern == 5:
				Patterns.stringBlink(ledStrip)	
			elif pattern == 6:			
				Patterns.lightningStringBlink(ledStrip, 33) #probability
			elif pattern == 7:
				Patterns.stringPulsate(ledStrip)
			elif pattern == 8:
				Patterns.watery(ledStrip, 128) #intensity
			elif pattern == 9:
				Patterns.blueWatery(ledStrip, 128) #intensity
			elif pattern == 10:
				Patterns.lightChase(ledStrip)
			elif pattern == 11:
				Patterns.blinkSpecific(ledStrip, 1)
			elif pattern == 12:
				Patterns.allOn(ledStrip)
			elif pattern == 13:
				Patterns.lightChaseBlue(ledStrip)
			elif pattern == 14:
				Patterns.blinkSpecificAll(ledStrip)
			elif pattern == 15:
				Patterns.chaseSpecific(ledStrip)
			else:
				log_event('WARNING! bad pattern number {0}'.format(pattern))
				pattern = 1 #set to something sane
	
			Patterns.manualControl(ledStrip, manualLight)			
			Patterns.sharedUpdate(ledStrip)

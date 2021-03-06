#tweaks
nodes = 294 #should be 294
camTestRig = False #should be False
useRunwayControl = True #should be True
fakeMode = False #should be False
noServer = False #should be False
screenSaverMode = True #should be True

#starting values for realtime vars (app can change these)
startColor = "blue"
startPattern = 45 #tbd
adjustableTick = 0.25 #starting value
lightDuration = 0.05 #should be 0.05
flameDuration = 0.05 #should be 0.05
lightFadeTime = 0.2
lightGap = 3
lightEq = 0

#screensaverMode
presetTick = 7 #seconds
presetIndex = 0
presetCount = 99

#internal stuff (don't change this)
fixedTick = 0.01666666666667 #60fps
fingerLights = []
fingerFlames = []
debugTickCounter = 0
clearCounter = 0
appConnectTimer = -1
appConnected = False
flBool1 = False #used as simple pattern switching state machine

configList=[]

import sys
import time
import random
import ConfigParser
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
	#f.write(format(time.time()) + ": " + msg + "\n")
	print format(time.time()) + ": " + msg
	pass

def read_config():
	global configList, presetCount
	print 'Flasher.py - read_config START'
	config = ConfigParser.RawConfigParser()
	config.read('Config/Config.txt')
	for s in config.sections():
		print s
		items = config.items(s)
		configList.append(items)
		
	presetCount = len(configList)
		
	print 'Flasher.py - read_config END'

def changePreset(preset):
	global presetIndex, presetTick, nextPresetTick, pattern, lightGap
	print '\nFlasher.py - changePreset: {0}'.format(preset)

	presetIndex = preset
		
	if presetIndex > presetCount -1:
		print 'Flasher.py - bad preset number {0}. Max is {1}'.format(presetIndex, presetCount -1)
		presetIndex = 0
		return None	

	presetList = configList[presetIndex]
	
	for k,v in presetList:
		if k == 'time':
			presetTick = float(v)
			nextPresetTick = time.time() + presetTick
			print 'Flasher.py - preset lasts for: {0}s'.format(presetTick)
			
		if k == 'pattern':
			pattern = int(v)
		if k == 'color':
			RunwayControl.changeColor(str(v))
		if k == 'tick':
			RunwayControl.changeTick(float(v))
		if k == 'ld':
			RunwayControl.changeLightDuration(float(v))
		if k == 'fadeout':
			RunwayControl.changeLightFadeTime(float(v))
		if k == 'fadein':
			RunwayControl.changeLightFadeInTime(float(v))
		if k == 'lightgap':
			lightGap = int(v)

	print 'Flasher.py - pattern is now: {0}'.format(pattern)

	if pattern in [20,21,22,35]:
		RunwayControl.syncIndices()
	if pattern in [40]:
		RunwayControl.syncIndices2()

#START
#f = open('log','w')
log_event('HELLO WORLD @ {0}'.format(time.time()))

read_config()

if fakeMode == False:
	log_event('starting in REAL mode')
	ledStrip = LedStrip_WS2801("/dev/spidev0.0", nodes)
else:
	print '*** WARNING: fakeMode is True ***'
	log_event('starting in FAKE mode')
	ledStrip = LedStrip_Fake(nodes)
	fixedTick = 1.0

RunwayControl.changeTick(adjustableTick)
RunwayControl.changeLightDuration(lightDuration)
RunwayControl.changeFlameDuration(flameDuration)
RunwayControl.changeLightFadeTime(lightFadeTime)
RunwayControl.changeColor(startColor)
RunwayControl.changeAllowFlame(False)

nextFixedTick = 0
nextPresetTick = 0

pattern = startPattern
if len(sys.argv) > 1:
	try:
		p = int(sys.argv[1])
		print 'requesting preset {0}'.format(p)
		changePreset(p)
		#pattern = int(sys.argv[1])
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
				RunwayControl.changeFlameDuration(0.05)
				screenSaverMode = False

			line = line.strip()
			appInput = line.split(',')
			print appInput

			for input in appInput:
				command = input.split('=')
				if len(command) < 2:
					break #filter out commands that aren't in the form x=y

				if command[0] == 'alive':
					pass
				elif command[0] == 'tick':
					try: 
						#log_event('Got tick command')
						adjustableTick = float(command[1].rstrip())
						RunwayControl.changeTick(adjustableTick)
					except:
						log_event('Bad tick input: ' + str(line))
				elif command[0] == 'preset':
					try:
						changePreset(int(command[1].rstrip()))
					except:
						log_event('Bad preset input: ' + str(line))
				elif command[0] == 'pattern':
					try:
						#log_event('Got pattern command')
						pattern = int(command[1].rstrip())
						if pattern in [20,21,22,35]:
							RunwayControl.syncIndices()
						if pattern in [40]:
							RunwayControl.syncIndices2()
						if useRunwayControl == False:
							Patterns.resetSharedVars()
					except:
						log_event('Bad pattern input: ' + str(line))
				elif command[0] == 'light' or command[0] == 'l':
					try: 
						fingerLights.append(int(command[1].rstrip()))
					except:
						log_event('Bad light input: ' + str(line))
				elif command[0] == 'fire' or command[0] == 'f':
					try: 
						fingerFlames.append(int(command[1].rstrip()))
					except:
						log_event('Bad fire input: ' + str(line))
				elif command[0] == 'ld' or command[0] == 'lightduration':
					print command
					try: 
						RunwayControl.changeLightDuration(float(command[1].rstrip()))
					except:
						log_event('Bad light duration input: ' + str(line))
				elif command[0] == 'fd' or command[0] == 'fireduration':
					try:
						RunwayControl.changeFlameDuration(float(command[1].rstrip()))
					except:
						log_event('Bad flame duration input: ' + str(line))
				elif command[0] == 'fadetime':
					try:
						RunwayControl.changeLightFadeTime(float(command[1].rstrip()))
					except:
						log_event('Bad fadetime input: ' + str(line))
				elif command[0] == 'fadein':
					try:
						RunwayControl.changeLightFadeInTime(float(command[1].rstrip()))
					except:
						log_event('Bad fadein input: ' + str(line))
				elif command[0] == 'lightgap':
					try:
						lightGap = (int(command[1].rstrip()))
						if lightGap < 1:
							lightGap = 1
					except:
						log_event('Bad lightgap command: ' + str(line))
				elif command[0] == 'color':
					try:
						RunwayControl.changeColor(str(command[1].rstrip()))
					except:
						log_event('Bad color command: ' + str(line))
				elif command[0] == 'eql':
					try:
						lightEq = (int(command[1].rstrip()))
					except:
						log_event('Bad eq command: ' + str(line))	
				elif command[0] == 'clear':
					RunwayControl.clearImmediate(ledStrip)
					fingerLights = []
					fingerFlames = []
				elif command[0] == 'panic':
					pattern = 0
					RunwayControl.clearImmediate(ledStrip)
					RunwayControl.changeAllowFlame(False)
					appConnected = False
					fingerLights = []
					fingerFlames = []
				else:
					pass

	if time.time() > nextPresetTick:
		nextPresetTick = time.time() + presetTick
		if screenSaverMode == True:
			changePreset(presetIndex)
			presetIndex += 1
			if presetIndex > presetCount:
				presetIndex = 0

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
				screenSaverMode = True
				presetIndex = 0
				nextPresetTick = 0

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
				RunwayControl.fillUpLightsDualEq(lightEq)
			elif pattern == 19:
				RunwayControl.lightAndFireChaserSimple()
			elif pattern == 20:
				RunwayControl.lightAndFireChaserLeft()
				RunwayControl.lightAndFireChaserRight()
			elif pattern == 21:
				RunwayControl.lightAndFireChaserLeftReverse()
				RunwayControl.lightAndFireChaserRightReverse()
			elif pattern == 22:
				RunwayControl.lightAndFireChaserLeft()
				RunwayControl.lightAndFireChaserRightReverse()
			elif pattern == 23:
				RunwayControl.twinkleAllFlames()
			elif pattern == 24:
				RunwayControl.twinkleAllLights()
				RunwayControl.twinkleAllFlames()
			elif pattern == 25:
				RunwayControl.twinkleAllLightsRandomFade()
			elif pattern == 26:
				RunwayControl.lightAndFireChaserLeft()
			elif pattern == 27:
				RunwayControl.lightAndFireChaserRight()	
			elif pattern == 28:
				RunwayControl.lightAndFireChaserLeftReverse()
			elif pattern == 29:
				RunwayControl.lightAndFireChaserRightReverse()	
			elif pattern == 30:
				RunwayControl.twinkleOneFlame()
			elif pattern == 31:
				RunwayControl.twinkleOneLight()
			elif pattern == 32:
				RunwayControl.twinkleOneLight()
				RunwayControl.twinkleOneFlame()
			elif pattern == 33:
				RunwayControl.twinkleAllLightNodes()
			elif pattern == 34:
				RunwayControl.twinkleAllLightNodes()
				RunwayControl.twinkleOneFlame()
			elif pattern == 35:
				RunwayControl.lightAndFireChaserLeftReverse()
				RunwayControl.lightAndFireChaserRight()
			elif pattern == 36:
				RunwayControl.fillUpLightsDualEqFake()		
			elif pattern == 37:
				RunwayControl.lightningSync()		
			elif pattern == 38:
				RunwayControl.lightningSides()
			elif pattern == 39:	
				RunwayControl.chaseLightDualBounce()
			elif pattern == 40:
				RunwayControl.lightAndFireChaserLeftBounce()
				RunwayControl.lightAndFireChaserRightBounce()
			elif pattern == 41:
				RunwayControl.chaseFlames()
			elif pattern == 42:
				RunwayControl.chaseFlamesDual()
			elif pattern == 43:
				RunwayControl.chaseFlamesDualReverse()
			elif pattern == 44:
				RunwayControl.chaseFlamesDualBounce()
			elif pattern == 45:
				RunwayControl.chaseLightDualBounce()
				RunwayControl.chaseFlamesDualBounce()
			elif pattern == 46:
				RunwayControl.chaseMultiFlamesDual(lightGap)
			elif pattern == 47:
				RunwayControl.chaseMultiFlamesDualReverse(lightGap)
			elif pattern == 48:
				RunwayControl.chaseMultiFlamesDual(3)
			elif pattern == 49:
				RunwayControl.chaseMultiFlamesDualReverse(3)
			elif pattern == 50:
				RunwayControl.chaseMultiLight(lightGap)
			elif pattern == 51:
				RunwayControl.chaseMultiLight(4)
			else:
				log_event('WARNING! bad pattern number {0}'.format(pattern))
				pattern = 13 #set to something sane

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

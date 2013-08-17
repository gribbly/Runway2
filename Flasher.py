#tweaks
nodes = 292 #should be 292
useRunwayControl = True #should be True
camTestRig = False #should be False
fakeMode = False #should be False
noServer = False #should be False
startPattern = 8 #tbd
fixedTick = 0.01666666666667 #120fps

#realtime vars (for app to control)
clearEveryNTicks = 1
adjustableTick = 1.0 #starting value
manualLight = -1

#internal state vars (don't change)
debugTickCounter = 0
clearCounter = 0

import sys
import time
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

debugNode = 0 #only used for pattern 0 in runwayMode
if len(sys.argv) > 2:
	try:
		debugNode = int(sys.argv[2])
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

while True:	
	#print "tick..." + format(time.time())
	if noServer == False:
		try:  
			line = q.get_nowait() 
			#line = q.get(timeout=.1)
		except Empty:
			pass
		else: # got line
			print line
			input = str(line).split(',')
			command = input[0].split('=')
			if command[0] == 'tick':
				try: 
					log_event('Got tick command')
					adjustableTick = float(command[1].rstrip())
				except:
					log_event('Bad tick input: ' + str(line))
				else:
					log_event('Tick update:' + str(adjustableTick))
			elif command[0] == 'pattern':
				try: 
					log_event('Got pattern command')
					pattern = int(command[1].rstrip())
				except:
					log_event('Bad pattern input: ' + str(line))
				else:
					log_event('Pattern update:' + str(pattern))
					if useRunwayControl == False:
						Patterns.resetSharedVars()
			elif command[0] == 'light':
				try: 
					pass
					log_event('Got light command')
				except:
					log_event('Bad light input: ' + str(line))
				else:
					log_event('Light update:' + str(int(command[1].rstrip())))
					manualLight = int(command[1].rstrip())
					if useRunwayControl == False:
						Patterns.resetSharedVars()	
			elif command[0] == 'fire':
				try: 
					pass
					log_event('Got fire command')
				except:
					log_event('Bad fire input: ' + str(line))
				else:
					pass
					log_event('Fire update:' + str(int(command[1].rstrip())))				

	if time.time() > nextFixedTick:
		nextFixedTick = time.time() + fixedTick
		#log_event('Tick {0}'.format(debugTickCounter))
		#debugTickCounter += 1 #this should be commented out!
		
		if debugTickCounter < 2:
			if useRunwayControl == True:
				clearCounter += 1
				if clearCounter >= clearEveryNTicks:
					RunwayControl.clear()
					clearCounter = 0
			
				if pattern == 0:
					RunwayControl.showNode(debugNode)
				elif pattern == 1:
					RunwayControl.showLights()
				elif pattern == 2:
					RunwayControl.showFlames()
				elif pattern == 3:
					RunwayControl.showLeftSideAll()		
				elif pattern == 4:
					RunwayControl.showRightSideAll()
				elif pattern == 5:
					RunwayControl.chaseLights1()	
				elif pattern == 6:
					RunwayControl.chaseLights2()
				elif pattern == 7:
					RunwayControl.chaseLights3()
				elif pattern == 8:
					RunwayControl.chaseLights4(5) #chase every n
				elif pattern == 9:
					RunwayControl.chaseLights5(5, 3) #chase every n, with width
				else:
					#log_event('WARNING! bad pattern number {0}'.format(pattern))
					pattern = 1 #set to something sane
	
				RunwayControl.update(ledStrip)
		
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

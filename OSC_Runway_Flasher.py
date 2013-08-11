#attempt 5 - using queues... original source here:
#http://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python/437888#437888

#tweaks
nodes = 25
bpm = 120 #default bpm (not used)
fakeMode = True
noServer = True
oscServer = False
osc_client = None

#parameters
tick = 0.1 #initial tick rate (.1 = 1/10 sec between)
runwayPattern = 1 #1 = chase, 2 = chase2, 3 = randomize, 4 = all on, 5 = all off


import sys
import time
import OSC, osc_receive

running = True

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

#sends parameter data to the osc client that just connected
def send_osc_data_to_client(client_ip):
	global osc_client

	if (client_ip == None):
		return

	#print "Looking for OSC client", client_ip
	if (osc_client == None):
		print "Connecting to %s" % client_ip
		osc_client = OSC.OSCClient()
		osc_client.connect((client_ip, 9001))

	msg = OSC.OSCMessage()
	msg.setAddress("/mode/bpmLabel")
	msg.append("120")
	print "Sending OSC data"
	osc_client.send(msg) # now we dont need to tell the client the address anymore
	#osc_client.send("")

def osc_handler(addr, tags, stuff, source):
	global running, osc_client

	print "FLASHER OSC_HANDLER! ---"
	#print "received new osc msg from %s" % OSC.getUrlStr(source)
	print "with addr : %s" % addr
	print "typetags %s" % tags
	print "data %s" % stuff
	print "---"

	print "Looking for OSC client"

	if (osc_client == None):
		print "no record of client previously, sending client new data"
		send_osc_data_to_client(OSC.getUrlStr(source).split(':', 1)[0])

	if (addr.startswith("/mode/select/1/")):
		mode = addr.split('/')
		pattern = mode[len(mode)-1]
		print "MODE SELECT : " + pattern
		if (pattern == -1):
			tmp = 0
		elif pattern == 0:
			Patterns.simpleChaser(ledStrip)
		elif pattern == 1:
			Patterns.cylonChaser(ledStrip)
		elif pattern == 2:
			Patterns.stringBlink(ledStrip)
		elif pattern == 3:
			Patterns.stringRandom(ledStrip)
		elif pattern == 4:
			Patterns.stringPulsate(ledStrip)
		elif pattern == 5:
			Patterns.watery(ledStrip)
		elif pattern == 6:
			Patterns.blueWatery(ledStrip)
		elif pattern == 7:
			Patterns.stringBlink(ledStrip)
	elif (addr == "/mode/clear"):
		Patterns.clearAll(ledStrip)
	elif (addr == "/mode/startStop"):
		running = not running
		print "running: %d" % running
	else:
		print "unknown command : %s" % addr


def log_event(msg):
	f.write(sys.argv[0] + " - " + msg + "\n")
	print sys.argv[0] + " - " + msg	

#START
f = open('log','w')
log_event(' HELLO WORLD @ {0}'.format(time.time()))

if fakeMode == False:
	log_event(' starting in REAL mode')
	ledStrip = LedStrip_WS2801("/dev/spidev0.0", nodes)
else:
	print '*** WARNING: fakeMode is True ***'
	log_event('starting in FAKE mode')
	ledStrip = LedStrip_Fake(nodes)
	tick = .5

if len(sys.argv) > 1:
	try:
		pattern = int(sys.argv[1])
	except:
		log_event('WARNING! Bad pattern arg {0}'.format(sys.argv[1]))

if noServer == False and oscServer == False:
	log_event('starting SuperSimple.py @ {0}'.format(time.time()))
	p = Popen(['/home/pi/Flasher4/SuperSimple.py'], stdout=PIPE, bufsize=1, close_fds=ON_POSIX)
	q = Queue()
	t = Thread(target=enqueue_output, args=(p.stdout, q))
	t.daemon = True # thread dies with the program
	t.start()
	log_event('started SuperSimple.py @ {0}'.format(time.time()))
else:
	if oscServer == True:
		print("Starting OSC Server")
		osc_receive.startServer(osc_handler)


log_event('tick is {0}'.format(tick))

nextTick = time.time()

log_event('we have {0} ws2801 nodes'.format(ledStrip.nLeds))
log_event('clear strip @ {0}'.format(time.time()))
Patterns.clearAll(ledStrip)

RunwayControl.create(ledStrip)

try:
	while True:
		if (running):
			if time.time() > nextTick:
				#f.write(sys.argv[0] + ' tick: {0}\n'.format(time.time()))
				nextTick = time.time() + tick
				RunwayControl.chase2()
				RunwayControl.update(ledStrip)


except KeyboardInterrupt :
	osc_receive.cleanup()


try:
	while True:	
		if noServer == False:
			try:  line = q.get_nowait() # or q.get(timeout=.1)
			except Empty:
				tmp = 0
			else: # got line
				input = str(line).split(',')
				command = input[0].split('=')
				if command[0] == 'tick':
					try: 
						log_event('Got tick command')
						tick = float(command[1].rstrip())
					except:
						log_event('Bad tick input: ' + str(line))
					else:
						log_event('Tick update:' + str(tick))
				elif command[0] == 'bpm':
					try: 
						log_event('Got bpm command')
						bpm = float(command[1].rstrip())
					except:
						log_event('Bad bpm input: ' + str(line))
					else:
						log_event('Bpm update:' + str(float(command[1].rstrip())))
				elif command[0] == 'pattern':
					try: 
						log_event('Got pattern command')
						pattern = int(command[1].rstrip())
					except:
						log_event('Bad pattern input: ' + str(line))
					else:
						log_event('Pattern update:' + str(pattern))
				elif command[0] == 'light':
					try: 
						log_event('Got light command')
					except:
						log_event('Bad light input: ' + str(line))
					else:
						log_event('Light update:' + str(float(command[1].rstrip())))
				elif command[0] == 'fire':
					try: 
						log_event('Got fire command')
					except:
						log_event('Bad fire input: ' + str(line))
					else:
						log_event('Fire update:' + str(float(command[1].rstrip())))

		# if time.time() > nextTick:
		# 	#f.write(sys.argv[0] + ' tick: {0}\n'.format(time.time()))
		# 	nextTick = time.time() + tick
		# 	#print 'tick: {0}'.format(tick)
			
		# 	if useRunwayControl == True:
		# 		RunwayControl.chase2()
		# 		RunwayControl.update(ledStrip)


except KeyboardInterrupt :
	osc_receive.cleanup()

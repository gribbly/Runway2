RunwayLights
============

Requires
--------
* Occidentalis v0.2 (unless fakeMode == True)

Instructions
------------
Ensure LEDs are powered, then run **sudo python Flasher.py**

Flasher.py does the following:
* Starts SuperSimple.py (minimalist socket server) in a child thread (use noServer = True to disable)
* Connects to LED string via GPIO (use fakeMode = True to bypass)
* Writes to a log file (called 'log')
* Then loops indefinitely:
  * Checks to see if SuperSimple has written anything to stdout. If so, process this input (e.g., change tick time or pattern or whatever)
  * Update LED pattern(s) via either RunwayControl.py (default) or Patterns.py (testing only)

Note: You can pass pattern commands on the command line. Use pattern 0 to test specific nodes:

**sudo python Flasher.py 0 1** #turn on node 1
**sudo python Flasher.py 0 123** #turn on node 123

Other useful test patterns:
**sudo python Flasher.py 1** #turn on all light nodes
**sudo python Flasher.py 2** #turn on all flame nodes
**sudo python Flasher.py 3** #turn on all left side nodes (lights and flames)
**sudo python Flasher.py 4** #turn on all right side nodes (lights and flames)

To connect to the socket server
-------------------------------

1. Load websocket2.html in a browser on the client
2. Make sure Flasher.py is running on the pi (host)
3. If pi is in "home" mode, press "home" button to connect. If pi is in "playa" mode, press "playa" button to connect.
4. If successful you should see "connected" in the output
5. Use buttons to send preset commands
6. You can also type in arbitrary protocol commands (see below for list) and hit "Send"

Protocol
--------
**NEED TO UPDATE**

If we need to handle multiple parameters per message, comma separate them:

pattern=1,tick=0.5


Setting SPI clock speed:
----------------
Mega hack! Compile and run spidev_test.c:

sudo ./a.out -s 1900000 #max I can get away with!

Troubleshooting:
----------------
* If Flasher.py crashes you may need to kill the server manually before restarting. Get PID from **ps -A | grep Super** then do **sudo kill PID**.

Workflow Notes
--------------
Git:

**git pull origin master**

**git add FILE**

**git commit -a** (then save commit message via nano)

**git push**



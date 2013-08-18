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
**alive=1** //dead man's switch. If I don't get this within 15 seconds, I'll switch to "screensaver mode" (no fire)

**pattern=n**

**tick=n** //pattern tempo. Clamped to 0.01666666666667 - 20.0

**light=n** or **l=n** //specific light

**fire=n** //specific flame

**ld=n** //light duration. Clamped to 0.0005 - 10.0

**fd=n** //fire duration. Clamped to 0.005 - 3.0

**fadetime=n** //light fade duration. Set to 0 for no fade.

**lightgap=n** //(int) gap between lights (used in some patterns). Clamped to min = 1.

**color=<color>** //change lights to this color. Supported: default, blue, white, red, green, yellow, pink, random (picks a random color), eq (eq color scheme!)

**eq=n** //current EQ level (send volume from mic). Expects a number between 0 and 42 (number of lights on one side). Use with "fillUpLightsDualEq".

**clear=1** //send to instantly turn everything off

If we need to handle multiple parameters per message, comma separate them:

**light=1,light=2,light=3**

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



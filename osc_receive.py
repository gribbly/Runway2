
""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file 
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import OSC
import time, threading
from netifaces import interfaces, ifaddresses, AF_INET



# tuple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
#receive_address = '127.0.0.1', 9000
receive_address = '192.168.1.198', 9000


def default(addr, tags, stuff, source):
    print "DEFAULT HANDLER"

# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
    print "---"
    print "received new osc msg from %s" % OSC.getUrlStr(source)
    print "with addr : %s" % addr
    print "typetags %s" % tags
    print "data %s" % stuff
    print "---"


    #   start
    #   stop
    #   mode
    #   speed
    #   
    #   btn/1
    #   btn/2
    #   btn/3
    #   btn/4
    #   btn/5
    #   btn/6
    #   btn/7
    #   btn/8
    #
    #   slider/1
    #   slider/2
    #   slider/3
    #   slider/4
    #   slider/5
    #   slider/6
    #   slider/7
    #   slider/8
    #
    #   trigger/1
    #   trigger/2
    #   trigger/3
    #   trigger/4
    #   trigger/5
    #   trigger/6
    #   trigger/7
    #   trigger/8


def startServer(handler_def):

    #get my ip address
    
    receive_ip = ""
    port = 9000

    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        print '%s: %s' % (ifaceName, ', '.join(addresses))
        ipaddr = ','.join(addresses)
        if (ifaceName == "en0"):
            receive_ip = ipaddr

    receive_address = receive_ip, port

    print("OSC Server starting on IP: " + receive_ip + ":" + str(port))

    # OSC Server. there are three different types of server. 
    ##s = OSC.OSCServer(receive_address) # basic
    global s, st
    s = OSC.ThreadingOSCServer(receive_address) # threading
    ##s = OSC.ForkingOSCServer(receive_address) # forking

    # this registers a 'default' handler (for unmatched messages), 
    # an /'error' handler, an '/info' handler.
    # And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
    s.addDefaultHandlers()
    s.addMsgHandler("default", handler_def) # adding our function

    # just checking which handlers we have added
    print "Registered Callback-functions are :"
    for addr in s.getOSCAddressSpace():
        print addr


    # Start OSCServer
    print "\nStarting Runway lights OSC server. Use ctrl-C to quit."
    st = threading.Thread( target = s.serve_forever )
    st.start()


    #try :
    #    while 1 :
    #        time.sleep(5)

    #except KeyboardInterrupt :
    #     print "\nClosing OSCServer."
    #    s.close()
    #    print "Waiting for Server-thread to finish"
    #    st.join() ##!!!
    #    print "Done"

def cleanup():
    global s, st
        #except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"

        

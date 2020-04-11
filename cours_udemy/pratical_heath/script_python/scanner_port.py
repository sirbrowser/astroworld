#!/bin/python

import sys
import socket
from datetime import datetime

#Define our target
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1])
else:
	print("Invalid amount of arguments.\n")
	print("Usage : \"python3 scanner_port.py <ip>")


#banner
print("-"*50)
print("Scanning target " + target + "...")
print("Time started: " + str(datetime.now()))
print("-"*50) 


try:
	for port in range(1,443):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socket.setdefaulttimeout(1)
		result = s.connect_ex((target,port))
		if result == 0:
			print("Port {} is open".format(port))
		s.close()
except KeyboardInterrupt:
	print("\nExiting Program")
	sys.exit
except socket.gaierror:
	print("Hostname could not be resolved.")
	sys.exit()
except socket.error:
	print("\nCouldn't connect to server")

print("-"*50)
print("Scanning of " + target + " finished.")
print("Time finished: " + str(datetime.now()))
print("-"*50) 

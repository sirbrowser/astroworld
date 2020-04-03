# Scanning

## Tables des matière
 - [Nmap](#Nmap)
 - [Zenmap](#Zenmap)
 - [Curl](#Curl)
 - [Amap](#Amap)
 
### Nmap :

#### Uses for :

 -vulnerability scanning and network discovery
 
 -identify some devices that are running on a network
 
 -discorvering hosts and services which are online or offline and ports that they have opened
 
 -identify what version of software is running on the open ports

#### Interresting parameter:
 
 -The OS detection `-O `
 
 -The Service/Version info of an open port `-sV `
 
 -Skip if the specified host is down or up `-Pn `
 
 -Perform a three way handshake to see more informations `-sT` (very detectable)
 
 -Perform the first Syn of the three way handshake `-sS` (not detectable except the IBS)
 
 -Perform an UDP scan `-sU` --> of course, it list only the open UDP ports

 -If you try to perform an nmap on a machine that just allows Syn bitset of its internal network, you can bypass this by send the last ACK bitset with `-sA`. The machine thinks that you have already send the Syn bitset in the TCP packets.
 
 -Specify the source port `-g <source_port>`
 
 -Specify the length of the packet sends by nmap `--data-length <...>` (Nmap sending by default the same packet length every time and a administrator can block every packet with this particular size)
 
 -Spoof mac address `--spoof-mac <mac_address>`

 -Use script located in /usr/share/nmap/scripts/ `--script=<script_name>` (ssh-brute.nse ...)

 Scripts which have "vul" in their names refers to a certain vulnerability. The date is also include in theirs names. In order to get more scripts --> vulscan github, vulners github...  
		
### Zenmap :
 Graphical interface for nmapping

### Curl :
 `curl ipinfo.io/<ip_adress>` --> get some informations (location for example) of a server.

### Amap : 
 Another tool for scanning like nmap tool


# Scanning and enumeration

## Index 


- [Netdiscover](#Netdiscover)
- [Nikto](#Nikto)
- [Dirbuster](#Dirbuster)
- [Enumerating SMB](#Enumerating-SMB)
- [Searchsploit](#Searchspolit)
- [Masscan](#Masscan)
- [Scanning with metasploit](#Scanning-with-metasploit)
- [Scanning with Nessus](#Scanning-with-Nessus)


### Netdiscover

`netdiscover` allows us to see every machines connected to our local network and give some informations about them. (ip, mac adress, vendor, hosntame...)
--> `netdiscover -r 192.18.1.0/24` for example

### Nikto

`nikto` allows us to see if the machine is probably vulnerable to certains exploit and the version of services open on this machine.
`nikto -r 192.168.1.2` for example

#### Dirbuster

`dirbuster` is the graphical interface of `dirb`.

### Enumerating SMB

Search for metasploit exploit.
` smclient` allows us to connect to a file share supported by smb.
`smbclient -L \\\\<host>\\` to list the directories
`smbclient \\\\<host>\\<share_name>` 


### Searchsploit

`searchsploit>` is a database for exploit
`searchsploit Samba 2` for example


### Masscan

`masscan` is an Internet-scale port scanner. It can scan the entire Internet in under 6 minutes, transmitting 10 million packets per second, from a single machine. It's integrate in Kali linux.
github : https://github.com/robertdavidgraham/masscan 
`masscan -p1-65535 --rate <nb_thread(1000)> <host>`

### Scanning with metasploit

Open `msfconsole` --> `search portscan` --> there is bunch of scanner available --> set the rights options --> `exploit`

### Scanning with Nessus

`nessus` is a vulnerability scanner
go to `https://www.tenable.com/downloads/nessus` and download the .deb which corresponds to your architecture
depackage the file, start nessus with systemd and go the url it gives you. Create an account.
you have a bunch of specific scan. You can schedule the scan.
there is a graphical resume of your scans...




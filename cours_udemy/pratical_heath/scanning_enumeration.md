# Scanning and enumeration

## Index 


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





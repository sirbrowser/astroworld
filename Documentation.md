# Documentation

## Table des matières
- [Footprinting](https://github.com/sirbrowser/astroworld/blob/master/footprinting.md)
- [Scanning](https://github.com/sirbrowser/astroworld/blob/master/scanning.md)
- [Website Penetration Testing](https://github.com/sirbrowser/astroworld/blob/master/website_penetration_testing.md)
- [Man In The Middle Attack](https://github.com/sirbrowser/astroworld/blob/master/man_in_the_middle_attack.md)
- [System Hacking](https://github.com/sirbrowser/astroworld/blob/master/system_hacking.md)
- [WPA2 Cracking](https://github.com/sirbrowser/astroworld/blob/master/WPA2_Wireless_Cracking.md)
- [Advanced Backdoor](https://github.com/sirbrowser/astroworld/tree/master/advanced_backdoor)
- [Basic Authentication bruteforcer](https://github.com/sirbrowser/astroworld/tree/master/basic_authentication_bruteforcer)
- [Docker](https://github.com/sirbrowser/astroworld/blob/master/docker.md)
- [Docker compose](https://github.com/sirbrowser/astroworld/blob/master/docker_compose.md)
- [Python for pentest](https://github.com/sirbrowser/astroworld/blob/master/cours_udemy/python_pentest/reverse_http.md)



### Scanning

   #####   Nmap

    nmap -sV <host>     // version of services
    nmap -O <host>      // OS detection
    nmap -p <host>      // port range
    nmap -Pn <host>     // treat host as online
    nmap -A <host>      // OS detection, version, script, traceroute
    nmap -sT <host>     // full TCP handshake
    nmap -sS <host>     // SYN sent to target
    nmap -sU <host>     // UDP scan
    nmap -sA <host>     // last ACK sent to target
    
    nmap --spoof-mac <mac> <host>   //spoof mac
    
    nmap --script <scipt-name> <host> --> /usr/share/nmap/scripts
    
    ssh-brute.nse --> SSH bruteforce script
    
    nmap --script vulscan,nmap-vulners -sV -Pn <host>
    
    script http-methods.nse --> scan methods (GET, POST, ...)

### Website Penetration Testing

   ##### whatweb

`whatweb -v <host> --> many information running on the website`

   #####   dirb

`dirb <host> <bruteforce list> --> search directories`


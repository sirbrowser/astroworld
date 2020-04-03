# Documentation

## Table des matières
- [Scanning](#scanning)
- [Website Penetration Testing](#website-penetration-testing)

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


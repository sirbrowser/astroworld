# FootPrinting

## Tables des matière
 - [Google Hacking](#Google-Hacking)
 - [Whois Tool](#Whois-tool)
 - [Harvester](#Harvester)
 - [Shodan](#Shodan)
 - [Zone transfer with dig](#Zone-transfer-with-dig)

### **Google Hacking** :
 ##### *On firefox* :
   `inurl: "index.php?id="` --> looking for all the websites that have this in their urls
    use "google hacking database"
 ##### *On nikto* :
   `nikto -h <ip or domain> ?-p <port>`
   `/etc/nikto.conf` --> configs
   We can use a proxy which is set in /etc/nikto.conf

### **Whois tool** :
  `whois <domain_name>` --> gather company informations

### **Harvester** :
  `theHarvester -d <domain_name> -l <limits> -b <source (default : google)>`  --> gather emails and hosts (with ip 		address) of a company 

### **Shodan**: 
  Open Firefox and type Shodan
  Shodan is the world's first search engine for Internet-connected devices.
  Keep track of all the computers on your network that are directly accessible from the Internet. Shodan lets you understand your digital footprint.

### **Zone transfer with dig** :
`dig axfr @<global_server> host`
`dnsenum <domain_name>` might be interresting too.

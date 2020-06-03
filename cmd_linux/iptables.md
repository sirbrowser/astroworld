# IPTABLES

- IPTABLES est un firewall qui peut faire :
	- filtrage ip
	- filtrage ports
	- filtrage protocole
	- translations (changement ip ...)
	- modification de paquets
	
## IPTABLES --> 3 tables  

### La table NAT 
- translation de ports et d'ip
	- 2 locations :
		- PREROUTING : amont firewall
		- POSTROUTING : aval firewall
	- 3 targets :
		- DNAT : IP de destination
		- SNAT : IP source
		- MASQUERADE : simule une gateway
		
### La table FILTER 
- 3 chaines :
	- INPUT : les entrants
	- OUTPUT : les sortants
	- FORWARD : les passants
- 4 targets :
	- DROP : refus brut des paquets sans retour au client
	- ACCEPT : accepte les paquets
	- REJECT : rejet avec retour à l'expéditeur
	- DENY
	.... LOG : logger les paquets sur la sortie standard
		  
### La table MANGLE (modification des paquets)
- 5 targets :
	- TOS : type de service
	- TTL : durée de vie
	- MARK : marque les paquets
	- SECMARK : marquage de sécurité
	- CONNESECMARK : copie d'un cas de sécurité
		
## Principales options

-L --> lister les règles (--line-numbers : numéro des règles)

-t --> type de tables (NAT, filter, mangle)

- Type d'actions sur les chaines/règles (INPUT, OUTPUT, FORWARD) :
	- -A : ajout de règle à une chaine (-A INPUT)
	- -D : suppression de règle (-D INPUT 1)
	- -R : remplace la règle (-R INPUT)
	- -I : Insertion d'une règle (-I INPUT 1)
	- -F : flush les règles pour une chaine (-F INPUT)
	- -N : création de chaine
	- -X : drop de chaine
	- -P : définition de la policy d'une chaine (-P INPUT DROP)
	
- Caractéristiques :
	- -p : protocole (-p tcp)
	- -s : la source (ip, réseau)
	- -j : action à faire (DROP/ACCEPT)
	- -d : la destination (ip, réseau)
	- -i : interface d'entrée (eth0...)
	- -o : interface de sortie
	- --sport <port> : un port (80...)
	- -m multiport --sport <ports> : plusieurs ports
	- -t : type (NAT...)

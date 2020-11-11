# Questions entretien technique

## Index
- [Réseau](#réseau)
    + [Ports](#ports)
    + [Différence UDP/TCP](#différence-udptcp)
    + [Différence SFTP/FTPS](#différence-sftpftps)
    + [Le handshake](#le-handshake)
- [Système](#système)
  * [Linux](#linux)
    + [Structure du système de fichiers](#structure-du-système-de-fichiers)
    + [Quelle est la séquence de boot sous Linux ?](#quelle-est-la-séquence-de-boot-sous-linux-)
    + [Différence entre mémoire physique et virtuelle ?](#différence-entre-mémoire-physique-et-virtuelle-)
    + [Où retrouve-t-on les logs systèmes et users ?](#où-retrouve-t-on-les-logs-systèmes-et-users-)
    + [Comment connaitre la liste des fichiers ouverts ?](#comment-connaitre-la-liste-des-fichiers-ouverts-)
    + [Qu'est-ce qu'il y a dans /sys, /proc, /dev ? Comment on y ajoute des fichiers ?](#quest-ce-quil-y-a-dans-sys-proc-dev--comment-on-y-ajoute-des-fichiers-)
    + [Différence entre ext[234] et xfs ?](#différence-entre-ext234-et-xfs-)
    + [Que représente un inode ?](#que-représente-un-inode-)
    + [Qu'est-ce que sticky-bit ?](#quest-ce-que-sticky-bit-)
    + [Qu'est-ce qu'une crontab ?](#quest-ce-quune-crontab-)
    + [Quel champ retrouve-t-on dans /etc/passwd ?](#quel-champ-retrouve-t-on-dans-etcpasswd-)
  * [Windows](#windows)
    + [Qu'est-ce qu'un registre ?](#quest-ce-quun-registre-)
    + [Qu'est-ce qu'un eventid ?](#quest-ce-quun-eventid-)
    + [Différence entre NTFS et FAT16/32](#différence-entre-ntfs-et-fat1632)
- [Active Directory](#active-directory)
    + [Qu'est ce que l'AD ?](#quest-ce-que-lad-)
    + [Protocole par défaut des annuaires](#protocole-par-défaut-des-annuaires)
    + [Qu'est ce qu'une forêt ?](#quest-ce-quune-forêt-)
    + [Qu'est ce que Kerberos ?](#quest-ce-que-kerberos-)
- [Autre](#autre)
    + [Quel type de métadonnées ont les fichiers (exif) ?](#quel-type-de-métadonnées-ont-les-fichiers-exif-)
    + [Liste des processus et des processus au démarrage ?](#liste-des-processus-et-des-processus-au-démarrage-)
- [Forensic](#forensic)
    + [Attentes : connaissances des principaux artefacts et outils de collecte et d'analyse](#attentes--connaissances-des-principaux-artefacts-et-outils-de-collecte-et-danalyse)
    + [Qu'est-ce qu'une analyse forensique ? Comment procéder ?](#quest-ce-quune-analyse-forensique--comment-procéder-)
    + [Comment faire de l'acquisisition de mémoire ? De disque ? Avec quels outils ?](#comment-faire-de-lacquisisition-de-mémoire--de-disque--avec-quels-outils-)
    + [Quels sont les artefacts "classiques" à regarder ?](#quels-sont-les-artefacts-classiques-à-regarder-)
    + [Comment on fait une capture réseau et on l'analyse ?](#comment-on-fait-une-capture-réseau-et-on-lanalyse-)
    + [Qu'est-ce qu'un write blocker ?](#quest-ce-quun-write-blocker-)
    + [Comment récupérer des fichiers supprimés ?](#comment-récupérer-des-fichiers-supprimés-)
    + [Qu'est-ce que le carving ?](#quest-ce-que-le-carving-)
    + [Citer quelques moyens de persistance et de discretion ?](#citer-quelques-moyens-de-persistance-et-de-discretion-)
    + [Comment analyse-t-on un doc malveillant ?](#comment-analyse-t-on-un-doc-malveillant-)
    + [Citez quelques méthdodes d'analyses anti-forensique ?](#citez-quelques-méthdodes-danalyses-anti-forensique-)
    + [Qu'est-ce qu'un mutex et en quoi c'est intéressant pour un malware ?](#quest-ce-quun-mutex-et-en-quoi-cest-intéressant-pour-un-malware-)
- [Veille en forensic :](#veille-en-forensic-)

### Réseau 

##### Ports 
- 20 --> FTP
- 22 --> SSH
- 23 --> TELNET
- 25 --> SMTP
- 53 --> DNS
- 63 --> WHOIS??
- 67-68 --> DHCP Client/Server
- 80 --> HTTP
- 110 --> POP3
- 123 --> NTP
- 137 --> NETBIOS Name Service
- 138 --> NETBIOS Datagram service
- 139 --> NETBIOS Session Service
- 143 --> IMAP4
- 161 --> SNMP
- 389 --> LDAP
- 443 --> HTTPS
- 445 --> CIFS/SMB

##### Différence UDP/TCP
TCP : plus fiable qu'UDP car vérification de bonne livraison des paquets  
UDP : moins fiable mais plus rapide, (streaming)  

##### Différence SFTP/FTPS
SFTP (22) : SSH FTP, transfert FTP encapsulé dans un tunnel SSH, une seule connexion, connexion sécurisé des le depart  
FTPS (21) : FTP + couche SSL (utilisation de certificat), deux connexions, connexion pas sécurisée des le départ uniquement qd le serveur a recu la
demande de chiffrement et qu'il commence à chiffrer  

##### Le handshake
TCP handshake : client send SYN, serveur repond SYN-ACK, client repond ACK  

### Système

#### Linux

##### Structure du système de fichiers 
Enregistré dans /etc/fstab (file system table), contrairement a windows tous les fichiers sont regroupés dans une arboresence unique ("/")  

##### Quelle est la séquence de boot sous Linux ?

##### Différence entre mémoire physique et virtuelle ?
- Mémoire physique : RAM, systeme stocke de manière temporaire tous les fichiers et app utilisés, accès tres rapide car directement sur la carte mère  
- Mémoire virtuelle : espace du disque dur qu'on définit et reserve pour suppléer la RAM lorsque le volume de données a traiter est grand, plus lent  

##### Où retrouve-t-on les logs systèmes et users ?
/var/log/syslog et /var/log/kern.log || /var/log/user.log  

##### Comment connaitre la liste des fichiers ouverts ?
Commande lsof  

##### Qu'est-ce qu'il y a dans /sys, /proc, /dev ? Comment on y ajoute des fichiers ? 
As root  
- /sys : information sur le systeme et ses composants (hardware attachés et installé) dans une forme structuré  
- /proc : systeme de fichier virtuel, contient des infos systemes en cours d'execution  
- /dev : fichiers des perphériques  

##### Différence entre ext[234] et xfs ?
- ext2 : pas de journaling, individual file size 16Gb to 2Tb, file system size 2Tb to 32Tb 
- ext3 : journaling features, same sizes
- ext4 : individual file size 16Gb to 16Tb, file system size 1ExaByte = 1000 petabyte = 1,000,000 Tb
- xfs : file size 8Eb, file system size 8Eb

##### Que représente un inode ? 
Structure de données contenant des infos à propos d'un fichier répertoire, chaque fichier possède un seul numéro
d'inode, inodes contienennt le smétadonnées des fichiers, notamment les droits d'accès (commande ls -i <file> pour le numero d'inode du fichier)  

##### Qu'est-ce que sticky-bit ?
Modifiable mais pas suppression sauf pour le proprio du fichier, son flag est t est sa valeur octale est 1000  

##### Qu'est-ce qu'une crontab ?
Tache planifiée  

##### Quel champ retrouve-t-on dans /etc/passwd ? 
Username, un x dans le champ mot de passe (stocké dans /etc/shadow), userid, groupid, nom complet de l'user repertoire perso de l'user, 
le compte shell de l'user  

#### Windows
##### Qu'est-ce qu'un registre ?

##### Qu'est-ce qu'un eventid ?
Numéro pour identifier un type d'événement  
Les plus connus :  
- 4608 : Windows start up
- 4609 : Windows shut down
- 4624 : Succesful Logon
- 4625 : Failed Logon
- 4688 : Process creation
- 4698 : Schedule task was created
- 4720 : User creation
- 4739 : GPO changed
- 4771 : Kerberos pre-auth failed

##### Différence entre NTFS et FAT16/32
- FAT16 (File Allocation Table) : 16-bits, 2Go max, compatibilité entre les OS, filenames limited to 8.3 convention
- FAT 32 : 32-bits, 16To max, 255 characteres pour un nom de fichier, 4Go max par fichier
- NTFS : journaling, chiffrements symétrique (EFS), 256To max, 16To max par fichier
- ReFS : increase size over NTFS

### Active Directory

##### Qu'est ce que l'AD ?
Annuaire permettant de hierarchiser et stocker les informations realtifs au domaine et au réseau.

##### Protocole par défaut des annuaires
LDAP / 389  

##### Qu'est ce qu'une forêt ?
Utilisé pour définir un regroupement de domaines AD qui partage un même schéma  

##### Qu'est ce que Kerberos ?
Protocole réseau d'authentification. 

### Autre

##### Quel type de métadonnées ont les fichiers (exif) ?
Marque, date, exposition, objectif, coordonnes, copyright, ...  

##### Liste des processus et des processus au démarrage ?
ps aux  
ps aux | grep root  

### Forensic

##### Attentes : connaissances des principaux artefacts et outils de collecte et d'analyse

- Volatility : analyse

- Dump RAM :
	- Windows : magnet RAM, Winen, Forensic Toolkit (FTK) (volatile and non-volatile(hard disk))  
	- MacOS : Goldfish, Mac Memory Reader, OSXPMem  
	- Linux : LiME, fmem  
	
##### Qu'est-ce qu'une analyse forensique ? Comment procéder ?
Collecte, analyser, conclusion sur le deroulement d'un événement  

##### Comment faire de l'acquisisition de mémoire ? De disque ? Avec quels outils ?

- Dump RAM :
	- Windows : magnet RAM, Winen, Forensic Toolkit (FTK) (volatile and non-volatile(hard disk))
	- MacOS : Goldfish, Mac Memory Reader, OSXPMem
	- Linux : LiME, fmem
	
- Dump harddisk :
	- Windows : AOMEI Backupper
	- Linux : Clonezilla

##### Quels sont les artefacts "classiques" à regarder ?
IOC : Taches planifiées, Ip, url, hash, file_name, windows registry key

##### Comment on fait une capture réseau et on l'analyse ?
Wireshark  

##### Qu'est-ce qu'un write blocker ?
Hardware qui copie bit a bit une partition, pour prevenir la modification sur la preuve, read-only  

##### Comment récupérer des fichiers supprimés ?
Foremost, autopsy  

##### Qu'est-ce que le carving ?
Extraire fichier, sans l'assistance du systeme de fichier qui l'a créé, check for magic bytes for example
tools : scalpel, FTK, Encase, Foremost  

##### Citer quelques moyens de persistance et de discretion ?
- Persistance : Manipulation de compte, autorun at boot
- Discretion : Effacement du journal d'événement windows, supprimer les logs   

##### Comment analyse-t-on un doc malveillant ?
Strings, script, exiftool, binwalk, file  

##### Citez quelques méthdodes d'analyses anti-forensique ?
 
##### Qu'est-ce qu'un mutex et en quoi c'est intéressant pour un malware ?
Un objet pour empecher l'accès simultané a une ressource  
Utilisé par les malwares pour empecher l'infection du systeme cible par différentes instances du meme malware

### Veille en forensic :
Arsenal Image Mounter --> nouvelle fonctionnalité : DPAPI Bypass, mdp chrome without mdp of user, wifi passwords avec IaZagne, 
dechiffrer les bdd dropbox en extractant la clé dropbox avec DPAPI Bypass, dropbox key pour dechiffrer filecache.dbx en filecache.db  

MFT (windows)
fls (linux)
qu'est ce qu'une partition
table d'inode
comment fonctionne volatility
qu'est ce qu'un processus
quel est le deroulement quand je tape un fichier au niveau kernel et user mdoe

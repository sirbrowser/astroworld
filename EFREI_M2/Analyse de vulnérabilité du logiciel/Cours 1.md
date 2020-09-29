# Analyse de vulnérabilité du logiciel

## Index

- [Types de logiciels malveillants](#types-de-logiciels-malveillants)
- [Signatures](#signatures)
- [Analyse statique vs analyse dynamique](#analyse-statique-vs-anlayse-dynamique)
- [Portable Executable file format (PE)](#portable-executable-file-format-pe)
- [Structure d'un programme en mémoire centrale](#structure-dun-programme-en-mémoire-centrale)



#### Types de logiciels malveillants

- Virus  

Code en langage machine qui se greffent sur un programme utilisé sur la cible, afin d'en modifier le comportement.  
Une fois implanté sur son programme-hôte, le greffon possède aussi la capacité de se répliquer sur d'autres programmes.  

Virus de boot : le code du virus s'exécute avant le MBR (Master Boot Record) puis redonne la main au MBR.  
TPM = Trusted Platform Module = is an international standard for a secure cryptoprocessor, a dedicated microcontroller designed to secure hardware through integrated cryptographic keys. Can be use to secure boot.  

Stealth / Tunneling Virus : quand un antivirus demande un fichier pour l'analyser le virus lui donne le fichier original, cela est possible car le virus intercepte tous les appels système.  

Virus chiffré : chifrrement du code / une nouvelle clé de chiffrement par infection / l'antivirus ne pourra pas les détecter en utilisant une approche basée sur les signatures.  

Virus polymorphic : le code mute à chaque infection, mais pas l'algorithme originel.  

Virus metamorphic : le virus réécrit complétement son code à chaque infection. (ce type de virus n'est pas chiffré).  

- Ver  

Un ver (worm) est une variété de virus qui se propage par le réseau.  

- Cheval de Troie  

Logiciel qui se présente normal, légitime, et qui une fois installé sur un ordinateur y effectue des actions cachées, illégitime.  
Démarche d'infection :  
1) créer un nouveau paquet Trojan en utilisant un kit de construction de trojan (metasploit).  
2) créer un dropper à inclure dans le paquet qui a pour fonction d'installer le code malveillant sur le système cible.  

Shell distant (Bind shell) vs reverse shell :  
Shell distant : un listener écoute chez la victime et l'attaquant se connecte dessus pour obtenir un shell distant.  
Reverse shell : un listener écoute chez l'attaquant et la cible se connecte dessus avec un shell.  

- Rootkit  

C'est un malware qui modifie une fonctionnalité de l'OS afin de cacher son existence.  
Détection compliquée.  


#### Signatures

- Host based signature  
Identifie un fichier ou une clef de registre sur la machine de la victime  
Se focalise sur ce que le malware fait sur le système et non sur le malware lui-même  

- Network signature  
Détecte le malware en analysant le traffic réseau  

#### Analyse statique vs analyse dynamique

- analyse statique :  
Examiner la malware sans l'éxecuter  
outils : virustotal, strings, IDAPro radare 2 ...  

- analyse dynamique :  
executer le malmware et surveiller ses effets sur la machine et sur le réseau  
utilisation de machines virtuelles et réaliser des snapshots  
outils : regshot, process monitor, process hacker, immunity debugger ...  
analyse de la RAM : mandant redline et volatility  



#### Portable Executable file format (PE)

Chaîne de compilation :  
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/chaine_de_compilation.PNG>  

Le fait striper = le fait de supprimer le nom des variables, fonctions etc, dans le code assembleur tout se fait avec des zones mémoire afin de rendre l'étude du code plus compliquée.  

Dans un fichier PE la table des symboles n'est pas directement dans le code mais dans un fichier extérieur avec l'extension PDB.  
Dans un fichier ELF la table des symboles peut etre dans l'exe directement ou dans un fichier exterieur avec l'extension dwarf.  

Editions de liens statique :  
- rarement utilisé par les exe windows  
- courant dans UNIX et linux  
- tout le code de la librairie est copié dans l'exe principal  
- produit des exe de taille importante  

Edition de lien dynamique :  
- méthode la plus utilisée  
- l'OS recherche les librairies nécessaires au chargement du programme principal  

#### Structure d'un programme en mémoire centrale

<img src=https://github.com/sirbrowser/astroworld/blob/master/images/structure.PNG>  

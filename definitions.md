# Définitions

- [Load balancing](#load-balancing)
- [Reverse shell vs bind shell](#Reverse-shell-vs-bind-shell)
- [Staged payload](#Staged-payload)
- [Stageless payload](#Stageless-payload) 

## Load balancing

Le load balancing permets de répartir les charges sur différents appareils d'un même réseau. Il permet notamment aux serveurs de sites web à forte audience de ne pas se retrouver surchargés. Dans le load balancing, les multiples requêtes sont distribuées sur plusieurs serveurs. 

**Avantages :**<br>
- amélioration du temps de réponse
- toujours afficher les informations demandées par l'internaute, même en cas de panne de l'un des serveurs
- les données sont plus sécurisées étant donné que les fichiers se trouvent sur des appareils annexes, et que seul le load balancer est accesible depuis l'extérieur

**Inconvénients :**<br>
- complexité de mise en place
- interconnectabilité des appareils fait que les pb peuvent se transmettre de machine en machine

**Le load balancing est une technique de répartition des charges complexes, particulièrement intéressant en termes de sécurité, de coût et
d'amélioration du temps de réponse**<br>

## Reverse shell vs bind shell

Reverse shell : l'attaquant ecoute sur un port pour recevoir la connection depuis la victime
Bind : l'attaquant fait en sorte que la victime ecoute sur un port pour pouvoir s'y connecter

## Staged payload

Le staged payload classique de Metasploit est : `windows/meterpreter/reverse_tcp`.
Ce type de payload est généralement envoyé sur la machine de la victime en deux parties.
La première partie est un payload primaire (stage 0) qui crée une connexion entre la machine de la victime à celle de l’attaquant.
Un deuxième payload (stage 1) contenant l’exploit est ensuite envoyé à travers la connexion créée, puis exécuté sur la machine de la victime.

## Stageless payload 

L’équivalent du staged payload classique présenté plus haut (`windows/meterpreter/reverse_tcp`) dans la catégorie des stageless est: `windows/meterpreter_reverse_tcp`.
Notez la présence du _ au lieu du deuxième / au niveau du nom du payload.
Dans cette catégorie, le payload est envoyé entièrement sur la machine de la victime. Celui-ci contient tout ce qui est nécessaire pour obtenir un reverse shell vers la machine de l’attaquant. Aucun transfert supplémentaire à partir de la machine de l’attaquant n’est nécessaire.


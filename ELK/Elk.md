# ELK

## Introduction et principes

  - ELK : ElasticSearch + Logstash + Kibana
  - Stack ELK : 3 outils combinés (avec des variations possibles -> EFK ... )
  - Collecte d'informations et restitution (logs, métriques ...)
  - SIEM : Security  Information and Management
  - xpack = verson payante
  
### Rôle de chaque service

#### ElasticSearch

  - Base de données NoSQL (distribuées)
  - fortes volumétries
  - spécialiste recherche plain text
  - index/sharding/replicas
  - moteur Apache Lucene (limite à 2 Mds de docs par service)
  - api format rest (json)
  
#### Logstash

  - ETL (Extract Transform Load)
  - Input/Filter/Output
  - nombreux plugin d'entrée (nginx, postgres ...)
  - filtres et grok
  
#### Kibana

  - Visualisation et Requêtes
  - spécialiste des données ElasticSearch (management etc)
  - Création de Dashboard
  - Concurrence à Graphana
  
### Une chaine

LOGSTASH >> ELASTICSEARCH << KIBANA

On peut avoir des variation avant Logstash avec des beats (filebeat, metricbeat...)

## Installation ElasticSearch

ElasticSearch utilise NoSQL qui facilite l'utilisation d'un système distribué.

Les principaux conccurents :
  - Cassandra : Traitement de gros volumes
  - MongoDB : La plus polyvalente
  - Redis : Traitement *in memory* donc très rapide mais avec un requêtage limité
  
ElasticSearch permet d'indexer tous les documents qui lui parviennent. <br>
Sa qualité de recherche repose sur deux éléments :
  - TF (Terme Frequency) : fréquence des mots
  - IDF (Inverse Difference Frequency) : moins un mot est commun, plus il a de poids dans la recherche 
  
Pour plus d'informations sur ElasticSearch et son installation --> [ElasticSearch.md](Elasticsearch.md)

## Installation Kibana 

Kibana permet la visualisation et l'exploitation des datas d'ElasticSearch.

```
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.8.0-amd64.deb     | <-- dernière version le 06/27/2020
dpkg -i kibana-7.8.0-amd64.deb
```
Dans /etc/kibana/kibana.yml on spécifie (installation simple) :
```
server.host: "0.0.0.0"                                | <-- écouter sur toutes les interfaces
elasticsearch.hosts: ["http://localhost:9200"]        | <-- si elasticsearch est présent sur la même machine, sinon changer l'IP (déjà par défaut)

elasticsearch.username: "<username>"                  | <-- On peut spécifier un
elasticsearch.password: "<password>"                  | <-- user/pwd pour se connecter à l'interface kibana
```

Kibana écoute sur le port `5601`.

## Installation Logstash

```
apt-get install openjdk-11-jdk-headless
sudo wget https://artifacts.elastic.co/downloads/logstash/logstash-7.8.0.deb      | <-- dernière version le 06/27/2020
dpkg -i logstash-7.8.0.deb
```

## Monitoring de fichiers locaux

Imaginons qu'un nginx tourne sur la même machine que notre ELK, on va vouloir monitorer notre fichier `access.log`. <br>
Tout d'abord, il faut que logstash ait le droit de lecture sur ce fichier : `usermod -aG adm logstash`.<br>
On doit créer un repertoire où seront stockés tous nos patterns : `mkdir /etc/logstash/pattern`, `chmod 755 -R /etc/logstash/pattern`.<br>
Ici nous devons créer un pattern pour nginx(`/etc/logstash/pattern/nginx`), cela nous permet de récupérer un user dans un log nginx:<br>
```
NGUSERNAME [a-zA-Z\.\@\-\+_%]+
NGUSER %{NGUSERNAME}
```

Si on fait un `curl 127.0.0.1:80`, voici le log nginx : `127.0.0.1 - - [28/Jun/2020:12:22:06 +0200] "GET / HTTP/1.1" 200 612 "-" "curl/7.64.0"`<br>
Il faut maintenant travailler cette ligne de log avec grok pour faire correspondre un champ à une variable. Le site [grok_debug](https://grokdebug.herokuapp.com/) est très utile pour cela. Dans notre cas, cette ligne de log est associé au pattern suivant :
```
%{IPORHOST:clientip} %{NGUSER:ident} %{NGUSER:auth} \[%{HTTPDATE:timestamp}\] \"%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:response}
```

Maintenant il faut créer le fichier de conf `/etc/logstash/conf.d/nginx.conf` :
```
input {
  file {                                            | <-- type "file" puisque l'on est en local 
    path => "/var/log/nginx/access.log"             
    start_position => "beginning"                   | <-- on commence au début du fichier quoi qu'il arrive
    sincedb_path => "/dev/null"
  }
}
filter {
    grok {
      patterns_dir => "/etc/logstash/pattern"       
      match => { "message" => "%{IPORHOST:clientip} %{NGUSER:ident} %{NGUSER:auth} \[%{HTTPDATE:timestamp}\] \"%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:response}" }
    }
}
output {
  elasticsearch {                                   | <-- type elasticsearch
      hosts => ["127.0.0.1:9200"]                   | <-- l'elasticsearch est en local
      index => "nginx-%{+YYYY.MM.dd}"               | <-- création d'un index nginx en rajoutant un suffixe qui est la date
  }
}
```

On redémarre logstash `service logstash restart`.<br>
On se rend sur l'interface Kibana sur le port `5601`.<br>
On va créer un index Kibana à partir de celui qu'on a créé sur ElasticSearch. Pour cela, on se rend dans la partie "Management" -> "Stack Management". On peut voir dans la partie ElasticSearch --> "Index Management" que l'index a bien été créé. On se rend dans la partie Kibana -> "Index Pattern" et on créé un index à partir de celui créé avec ElasticSearch.<br>
On peut désormais voir dans la partie "Discover" de Kibana que l'index "nginx" est créé et on peut voir les logs.


## Installation Filebeat + Module Nginx

L'utilisation de Filebeat va permettre l'injection de data directement dans ElasticSearch (on passe par les modules pour le filtering). Il a donc une interaction avec ElasticSearch pour injecter ces data mais aussi avec Kibana puisqu'il peut directement créer des indexs dans ce dernier (correspondant au module activé).

Pour installer Filebeat sur une machine Linux :
```
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.8.0-amd64.deb
dpkg -i filebeat-7.8.0-amd64.deb

```
On se rend dans le fichier de configuration `/etc/filebeat/filebeat.yml` et on met à jour au moins 2 informations cruciale :
```
setup.kibana:
  host: "<IP_ELK>:5601"
  
output.elasticsearch:
  hosts: ["<IP_ELK>:9200"]
```

Sur l'interface Kibana, on peut retrouver dans la partie "Home" -> "Observability", les différents domaines que l'on peut monitorer (logs, métrics...).<br>
Sur la machine où est installé Nginx et Filebeat, on doit activer le module nginx : `filebeat modules enable nginx`.<br>
On peut lister tous les modules déjà existants : `filebeat modules list`. <br>
Pour activer les dashboards de Kibana : `filebeat setup`.<br>
Et on restart le service Filebeat : `service filebeat restart`.<br>
On peut voir directement en rafraîchissant Kibana, que le module est en place, que les indexs d'ElasticSearch et de Kibana ont été créés. On retrouve les logs dans le tab "Discover" de Kibana.

## Filebeat - Input files Output Logstash

On va utiliser des logs nginx pour l'exemple. On reprend donc les mêmes configurations que précédemment.<br>

Si le module nginx de filebeat est activé, on le désactive : `filebeat modules disable nginx`. Justement on cherche une méthode intermédiaire aux modules.<br>
Tout d'abord, on modifie le fichier /etc/filebeat/filebeat.yml :
```
filebeat.inputs:
- type: log
  enabled: true                     | <-- false par défaut 
  paths:
    - /var/log/nginx/access*.log    | <-- on veut envoyer le fichier access.log à logstash
    
--- 
Mettre en commentaire la partie sur l'ElasticSearch output puisque l'on veut envoyer des logs à Logstash 
---

output.logstash:
  hosts: ["<IP_ELK>:5044"]          | <-- Le port par défaut sur lequel logstash recoit les logs est 5044
```

Sur l'ELK, on a un fichier `/etc/logstash/conf.d/nginx.conf` comme celui ci (pour les configurations supplémentaires voir [Monitoring de fichiers locaux](#Monitoring-de-fichiers-locaux)):
```
input {
  beats {                 | <-- input de type beat
    port => 5044          | <-- on fait écouter logstash sur le port 5044
  }
}
filter {
    grok {
      patterns_dir => "/etc/logstash/pattern"
      match => { "message" => "%{IPORHOST:clientip} %{NGUSER:ident} %{NGUSER:auth} \[%{HTTPDATE:timestamp}\] \"%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:response}" }
    }
}
output {
  elasticsearch {
      hosts => ["127.0.0.1:9200"]
      index => "nginx-%{+YYYY.MM.dd}"
  }
}
```

On redémarre logstash `service logstash restart` sur l'ELK et Filebeat sur la machine Nginx `service nginx restart`.<br>
Avec l'interface Kibana, on voit qu'un index ElasticSearch a été créé. Il faut en créer un pour Kibana comme expliqué à la fin de la partie [Monitoring de fichiers locaux](#Monitoring-de-fichiers-locaux).

## Filebeat - Input de type log

On peut configurer plus spécifiquement les input de types logs avant des les envoyer à Logstash. Il existe plusieurs champs de configurations qui sont disponibles sur la [doc ElasticSearch](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html).<br>
On peut les rajouter dans le fichier `/etc/filebeat/filebeat.yml` :
```
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/nginx/access*.log
  exclude_lines: ["^127.0.0.1"]     | <-- exclut les lignes qui commence par "127.0.0.1"
  exclude_files: [".gz$"]           | <-- exclut les fichiers qui finissent par ".gz" (non intéressant dans cette configuration)
  ignore_older: 24h                 | <-- ignore les fichiers qui ont été modifié il y a plus de 24h
  tags: ["log"]                     | <-- rajoute "log" dans le champ "tag" déjà présent dans ElasticSearch
  fields:
    env: prod                       | <-- ajout d'un champ fields.env qui contiendra "prod"
    api: front                      | <-- ajout d'un champ fields.api qui contiendra "front"
```
Voici quelques exemples mais il en existe plein d'autres qui sont très intéressants voir la [doc ElasticSearch](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html).

## Filebeat - Input Container

On peut configurer plus spécifiquement les inputs de types containers avant des les envoyer à Logstash. Il existe plusieurs champs de configurations qui sont disponibles sur la [doc ElasticSearch](https://www.elastic.co/guide/en/beats/filebeat/master/filebeat-input-container.html).<br>
On peut modifier le fichier `/etc/filebeat/filebeat.yml` :
```
filebeat.inputs:
- type: container 
  paths: 
    - '/var/lib/docker/containers/*/*.log'
```
Les logs de tous les conteneurs sont présent dans le répertoire `/var/lib/docker/containers/`. On peut créer un nouveau IFO (input/filter/output) sur l'ELK dans `/etc/logstash/conf.d/` (par exemple `docker_nginx.conf`) -- Imaginons que c'est un conteneur nginx :
```
input {
  beats {
    port => 5044
  }
}
filter {
    grok {
      patterns_dir => "/etc/logstash/pattern"
      match => { "message" => "%{IPORHOST:clientip} %{NGUSER:ident} %{NGUSER:auth} \[%{HTTPDATE:timestamp}\] \"%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:response}" }
    }
}
output {
  elasticsearch {
      hosts => ["127.0.0.1:9200"]
      index => "docker-nginx-%{+YYYY.MM.dd}"        | <-- on crée un nouvel index Elastic-Search
  }
}
```
Il faudra créer un nouvel index Kibana à partir de celui d'ElasticSearch puis on pourra visualiser les logs du/des conteneurs.<br>

## Filebeat - Input TCP

On peut configurer plus spécifiquement les inputs de type TCP avant des les envoyer à Logstash. Il existe plusieurs champs de configurations qui sont disponibles sur la [doc ElasticSearch](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-tcp.html).<br>
On peut modifier le fichier `/etc/filebeat/filebeat.yml` :
```
filebeat.inputs:
- type: tcp         
  max_message_size: 10MiB             
  host: "<IP>:<port>"                         | <-- Interface et port d'écoute (par exemple localhost:9000)              
```
On peut créer un nouveau IFO (input/filter/output) sur l'ELK dans `/etc/logstash/conf.d/` (par exemple `tcp.conf`) :
```
input {
  beats {
    port => 5044
  }
}
filter {
    grok {
      match => { "message" => "%{WORD:champs1} %{WORD:champs2} %{WORD:champs3}" }   | <-- juste pour l'exemple qui va suivre, mais on pourrait mettre n'importe quoi 
    }
}
output {
    elasticsearch {
      hosts => ["localhost:9200"]
      index => "tcp-%{+YYYY.MM.dd}"
    }
}
```
Si Filebeat écoute sur localhost:9000, lors d'un `echo "pierre paul jacques" | nc 127.0.0.1 9000`, on devrait pouvoir le visualiser sur Kibana mais avant il faudra créer un nouvel index Kibana à partir de celui d'ElasticSearch. Trois champs custom seront donc créés : champ1, champ2 et champ3 avec leur valeur respective : pierre, paul et jacques.

## Logstash - Multi Input et Multi Index

On peut avoir différents inputs filebeat sur une même machine, par exemple si on veut envoyer les logs docker et les logs syslog. <br>
Dans le fichier `/etc/filebeat/filebeat.yml` :
```
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'
  tags: ["docker"]

- type: syslog
  protocol.udp:
    host: "localhost:9000"
```
Il faut activer le module syslog : `filebeat modules enable system`.<br>
Il faut aussi modifier le fichier de configuration du module : `/etc/filebeat/modules.d/system.yml[...]`. <br>
```
- module: system
  syslog:
    enabled: true
    var.paths: ["/var/log/syslog"]
  auth:
    enabled: false
    var.paths: ["/var/log/auth.log"]
filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false

setup.template.settings:
  index.number_of_shards: 1
```
On aura aussi les configurations de Kibana et Logstash mais pas d'ElasticSearch.<br>
Dans `/etc/logstash/conf.d/multibeats.conf`, on aura :
```
input {
  beats {
    port => 5044
  }
}
filter {
  if [fileset][name] == "syslog" {            | <-- Pour reconnaitre le log syslog
    grok {
      match => { "message" => "%{SYSLOGTIMESTAMP:syslog_timestamp} %{SYSLOGHOST:syslog_hostname} %{DATA:syslog_program}(?:\[%{POSINT:syslog_pid}\])?: %{GREEDYDATA:syslog_message}" }
      add_field => [ "received_at", "%{@timestamp}" ]
      add_field => [ "received_from", "%{host}" ]
    }
    syslog_pri { }
    date {
      match => [ "syslog_timestamp", "MMM  d HH:mm:ss", "MMM dd HH:mm:ss" ]
    }
    mutate {
      add_tag => ["syslog"]
    }
  }

  if [input][type] == "container" {           | <-- Pour reconnaitre le log docker
    grok {
      patterns_dir => "/etc/logstash/pattern"
      match => { "message" => "%{IPORHOST:clientip} %{NGUSER:ident} %{NGUSER:auth} \[%{HTTPDATE:timestamp}\] \"%{WORD:verb} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}\" %{NUMBER:response}" }
    }
  }
}
output {
  if "syslog" in [tags] {     
    elasticsearch {
      hosts => ["localhost:9200"]
      index => "syslog-%{+YYYY.MM.dd}"
    }
  }
  if "docker" in [tags] {
    elasticsearch {
      hosts => ["localhost:9200"]
      index => "docker-%{+YYYY.MM.dd}"
    }

  }
}
```
Pour les logs syslog, on peut directement activer le module system et activer l'output directement vers elasticsearch, puis `filebeat setup` pour créer directement les indexs et les dashboards.<br>

## Filebeat - Output type log

On peut directement créer un output de type log avec filebeat, on doit éditer le fichier de configuration filebeat `/etc/filebeat/filebeat.yml` :
```
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'

output.file:
  path: "/tmp/toto"                         | <-- si le répertoire n'est pas créer, il va se créer automatiquement
  filename: "toto"                          | <-- fichier qui répertorie les logs de l'input

processors:
  - add_host_metadata: ~                    | <-- pour avoir des métadata de l'hôte dans chaque log
  - add_cloud_metadata: ~
  - add_docker_metadata: ~                  | <-- pour avoir des métadata du conteneur docker dans chaque log
  - add_kubernetes_metadata: ~
``` 
## Filebeat - Output type console

On peut directement créer un output de type console avec filebeat, on doit éditer le fichier de configuration filebeat `/etc/filebeat/filebeat.yml` :
On doit d'abord stopper le service filebeat : `systemctl stop filebeat`.
```
filebeat.inputs:
- type: container
  paths:
    - '/var/lib/docker/containers/*/*.log'

output.console:
  pretty: true                              | <-- mettre en format json (pareil qu'avec la commande "jq")

processors:
  - add_host_metadata: ~
  - add_docker_metadata: ~
```
Si on lance la commande `filebeat -e`, on va avoir accès à la console filebeat en foreground et les logs vont apparaître au fur et à mesure.

## Filebeat Communiquer en TLS avec Logstash

La communication TLS entre Filebeat et Logstash permet d'éviter les injections de systèmes qui n'aurait pas le bon certificat (un attaquant par exemple).<br>
Sur le serveur logstash, on va créer un nouveau fichier identique au fichier `/etc/ssl/openssl.cnf`, on peut faire un `cp /etc/ssl/openssl.cnf /tmp/custssl.conf`.<br>
On va lui rajouter l'adresse IP du serveur logstash en dessous de la catégorie `[ v3_ca ]` :
```
[ v3_ca ]
subjectAltName = IP: <IP_Logstash>
```
Ensuite il faudra créer un certificat à partir de ce fichier de configuration : 
```
mkdir /etc/ssl/logstash/    | <-- pour stocker le certificat et la clé privée
openssl req -x509 -batch -nodes -days 3650 -newkey rsa:2048 -keyout /etc/ssl/logstash/logstash.key -out /etc/ssl/logstash/logstash.crt -config /tmp/custssl.conf | <-- génére le certificat avec la config
chown -R logstash /etc/ssl/logstash/ 
chgrp -R logstash /etc/ssl/logstash/ 
chmod -R 500 /etc/ssl/logstash/logstash.*
```
Dans les IFO de logstash dans `/etc/logstash/conf.d/*`, chaque input devra comporté trois paramètres en plus : 
```
input {
  beats {
    port => 5044
    ssl => true
    ssl_certificate => "/etc/ssl/logstash/logstash.crt"
    ssl_key => "/etc/ssl/logstash/logstash.key"
  }
}
```
On peut restart logstash : `systemctl restart logstash`.<br>
Sur la machine avec Filebeat, on copie le même certificat qui a été généré précédemment. Gérer aussi les droits sur ce fichier (si c'est root qui lance Filebeat, `chown root /etc/ssl/filebeat/logstash.crt` ...). <br>
On peut dès à présent voir si la configuration est bonne en lancant la commande `curl -v --cacert /etc/ssl/filebeat/logstash.crt https://<IP_Logstash>:5044` depuis la machine avec le service Filebeat.<br>
Maintenant pour l'intégrer à output logstash, il faut modifier le fichier /etc/filebeat/filebeat.yml :
```
output.logstash:
  hosts: ["<IP_Logstash>:5044"]
  ssl:
    certificate_authorities: ["/etc/ssl/filebeat/logstash.crt"]     | <-- intégration du certificat
```
On peut restart filebeat : `systemctl restart filebeat`.

## Metricbeats Module System

On peut gérer les metrics system d'un hôte. Il faut télécharger Metricbeat et l'installer : 
```
curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-7.8.0-amd64.deb     | <-- dernière version le 06/30/2020
dpkg -i metricbeat-7.8.0-amd64.deb
```
Il faudra modifier le fichier de configuration `/etc/metricbeat/metricbeat.yml` :
```
setup.kibana:
  host: "<IP_Kibana>:5601"
output.elasticsearch:
  hosts: ["<IP_ElasticSearch>:9200"]
```
On peut modifier le fichier `/etc/metricbeat/modules.d/system.yml` :
```
- module: system
  period: 10s                 |     <-- periode d'envoi des metrics à ElasticSearch
  metricsets:
    - cpu                     |     <--
    - load                    |     <--
    - memory                  |     <--
    - network                 |     <--
    - process                 |     <--
    - process_summary         |     <--   À commenter ou décommenter selon ce que l'on veut monitorer
    - socket_summary          |     <--   Attention, certains systèmes ne sont pas capables de remonter 
    #- entropy                |     <--   certains metrics ce qui fait planter metricbeat
    #- core                   |     <--
    #- diskio                 |     <--
    #- socket                 |     <--
    #- service                |     <--
```
On peut lancer la commande `metricbeat setup` pour mettre en place les indexs ElasticSearch et Kibana et les Dashboards, puis lancer le service metricbeats : `systemctl start metricbeat`.

## Metricbeats - Module Docker

On peut monitorer les metrics de conteneurs docker de la même manière que pour le [module system](#Metricbeats-Module-System).

## Logstash - Input File

Les inputs de file peuvent être configurer très finement avec des paramètres spécifiques. <br>
Les inputs vont prendre des fichiers plats et vont les mettre sous format json. Ceux que le fichier contiendra fera partie du champ "message", il y aura en plus le champ "path", "@timestamp", "host" et "version".<br>
Par exemple imaginons un fichier `/etc/logstash/conf.d/file.conf` :
```
input {
        file {
        path => "/etc/myfiles/*.log"
        }
}
output {
        file {
        path => "/tmp/output.log"
        }
}
```
On peut rajouter les paramètres suivants :
```
id => "<id>"                          | <-- pour différencier les inputs (par exemple id => "hugo")
delimiter => "<delimiter>"            | <-- chaque message ne sera plus délimité par un saut de ligne mais par le delimiter qu'on chosit (par exemple delimiter => ";")
mode => "<read,tail>"                 | <-- Soit Logstash est en mode "read" et dès qu'il a finit de lire il ferme le fichier et réouvre etc, soit il reste à l'écoute avec "tail"
close_older => "<time>"               | <-- Logstash ferme le fichier au bout d'un certain temps (par exemple close_older => "1 hour")
stat_interval => "<time>"             | <-- Gère la fréquence entre les check des fichiers (par exemple stat_interval => "1 second") en sachant qu'il a déjà une valeur par défaut
discover_interval => "<time>"         | <-- Gère la fréquence entre la découverte de fichiers (par exemple discover_interval => "10") en sachant qu'il a déjà une valeur par défaut
exclude => "<path>"                   | <-- Permet d'exclure le check de certains fichiers (par exemple exclude => "/var/log/syslog.log*" pour exclure les logrotate)

file_completed_action => "delete"     | <-- 
start_position => "beginning"         | <-- EN MODE READ SEULEMENT, permet de supprimer un fichier dès que Logstash l'a traité

sincedb_path => "<path>"              | <-- localisation du fichier où Logstash stocke son pointeur de fichier, en sachant qu'il a déjà une valeur par défaut
sincedb_clean_after => "<time>"       | <-- fréquence de néttoyage des timestamp
add_field => { "<field>" => "value" } | <-- permet d'ajouter un champ (par exemple add_field => { "env" => "prod" }
codec => "plain"                      | <-- permet de ne pas générer l'output en json mais en plain text
type => "<type>"                      | <-- permet de créer des types qui sont réutilisable pour la partie filter... (par exemple type => "apache") 
```

## Logstash Input Beat

Logstash peut être en écoute de producteur de data de type beat :
  - filebeat		: fichiers
  - metricbeat	: métriques
  - packetbeat	: réseau
  - winlogbeat	: évènements windows
  - auditbeat		: données d'audit (login...)
  - heartbeat 	: disponibilité
  - ...
  
Logstash écoute sur un choisi port en attendant de recevoir des data de type beat.<br>
Le modèle de base se présente comme ceci : 
```
input {
  beats {
    port => 5044      | <-- champ obligatoire, logstash écoute sur le port 5044
  }
}
output {
   file {
      path => "/tmp/output.log"
   }
}
```

On peut rajouter différents paramètre à l'input (cf [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-beats.html), voici quelques exemples :
```
host => "<IP>"                            | <-- IP en écoute (par défaut "0.0.0.0")
add_field => { "<field>" => "<value>" }   | <-- permet d'ajouter un champ (par exemple add_field => { "env" => "prod" }
id => "<id>"                              | <-- permet d'ajouter un ID. Cela peut être pratique quand on a plusieurs ID de même type, pour les différencier.
type => "<type>"                          | <-- permet l'ajout d'un type Logstash (par exemple type => "mybeat")
tags => ["<tag1>","<tag2>",...]
```
On peut aussi rajouter du [ssl entre beats et logstash](#Filebeat-Communiquer-en-TLS-avec-Logstash)

## Logstash Input Stdin

On peut ajouter un input de type `stdin` qui va pouvoir récupérer des messages de la console quand on lance la commande logstash `/usr/share/logstash/bin/logstash` en foreground. On peut rajouter différents paramètre à l'input (cf [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-stdin.html)).

## Logstash Input Exec

On peut lancer des scripts à des intervalles de temps donné afin de récupérer l'output :
```
input {
   exec {
     command => "/tmp/test.sh"
     interval => "10"
   }
}
output {
  ....
}
```
On peut rajouter différents paramètre à l'input (cf [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-exec.html)).

## Logstash Input TCP

On peut écouter sur une interface réseau et un port et logger tous les messages qui y passent avec l'input tcp.<br>
Il existe deux modes :
  - "serveur" --> Logstash va écouter sur un port spécifique de sa machine
  ```
  input {
    tcp {
      mode => "server"      | <-- écoute sur toutes ses interfaces (sinon rajouter le paramètre "host => "<IP>" pour écouter sur une interface en particulier)
      port => <port>        | <-- écoute sur le port spécifié 
   }
  ouput {
    ....
  }
  ``` 
  - "client"  --> Logstash va écouter sur un port spécifique d'un hôte distant
  ```
  input {
    tcp {
      mode => "client"          | <-- écoute sur une interface distante
      host => "<IP_distante>    | <-- écoute sur cette interface
      port => <port>            | <-- écoute sur le port spécifié 
   }
  ouput {
    ....
  }
  ```
Pour tester chaque mode, on peut faire un `nc <IP_Logstash> <port_écoute>` puis envoyer des messages.<br>
On peut rajouter différents paramètre à l'input (cf [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-tcp.html)).

## Logstash Input ElasticSearch

On peut directement prendre des informations d'un ElasticSearch avec l'input "elasticsearch" :
```
input {
  elasticsearch {
    hosts => "<IP_Elastic>"       
    index => "<index>"            | <-- index(s) à prendre en compte (par exemple index => "metricbeat*")
    docinfo => true               | <-- récupérer les metadata de chaque doc (index,type,id,...) !!! très important !!!
  }
}
output {
  ....
}
```
On peut rajouter des paramètre à l'input "elasticsearch" (cf [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-elasticsearch.html)). Voici quelques uns :
```
docinfos_fileds => ["<field>",...]      | <-- permet de filter les informations de "docinfo"
schedule => "<type cron>"               | <-- permet de gérer l'intervalle de temps avec un cron (type linux)
size => <nombre>                        | <-- nombre de documents ramenés
add_field / tags / type ...
```` 

### Input/Output ElasticSearch

Attention pour un output de type `file`, Logstash ne reconnait pas où il s'est arrêté. De ce fait, il va refaire les requêtes entières et il y aura des doublons à chaque intervalle de temps donnés.
Pour un output de type elasticsearch, on va pouvoir récupérer les données d'un elasticsearch avec l'input et le réinjecter dans le même ou un autre elasticsearch. Cela peut être intéressant par exemple lorsqu'on veut faire de la redondance. On peut filtrer ces données pour créer un nouvel index à partir de celui qu'on récupère pour en créer un autre qui contiendra donc des données filtrées. Voici un exemple :
```
input {
  elasticsearch {
    hosts => "127.0.0.1"
    index => "metricbeat*"
    codec => "json"                        | <-- pas nécessaire car c'est la valeur par défaut
    query => '{
      "query":{
        "match":{
          "system.process.cgroup.cpuacct.id" : "docker.service"
        }
      }
    }'
    size => 1000
    docinfo => true
  }
}
output {
  elasticsearch {
    hosts => "127.0.0.1"                                        | <-- Ip de l'elasticsearch dans lequel on va réinjecter les données
    index => "extract-metricbeat.%{[@metadata][_index]}"        | <-- Indice à partir de celui qu'on retrouve dans "docinfo"
    document_type => "%{[@metadata][_type]}"                    | <-- Type de document à partir de celui qu'on retrouve dans "docinfo"
    document_id => "%{[@metadata][_id]}"                        | <-- ID de document à partir de celui qu'on retrouve dans "docinfo"
  }
}
```

## Logstash Input HTTP

L'input HTTP peut aussi être intéressant :
```
input {
  http {
    host => "<IP>"                  | <-- "0.0.0.0" pour écouter sur toutes les interfaces
    port => <port1>
    tags => ["TypeA"]
  }
  http {
    host => "<IP>"                  | <-- "0.0.0.0" pour écouter sur toutes les interfaces
    port => <port2>
    tags => ["TypeB"]
  }
}
output {
  if "TypeA" in [tags] {
    elasticsearch {
      hosts => ["<IP_Elastic>:9200"]
      index => "typea-%{+YYYY.MM.dd}"
    }
  }
  if "TypeB" in [tags] {
    elasticsearch {
      hosts => ["<IP_Elastic>:9200"]
      index => "typeb-%{+YYYY.MM.dd}"
    }
  }
}

```
On peut rajouter beaucoup de paramètre à l'input comme le response code, les response headers, chiffré la commnication avec tls, max_content_lenght... (cf [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-http.html)).<br>
On peut tester la configuration avec simplement par exmple :
```
curl -H "content-type: application/json" -d '{"champs1": "test1",champs2": "test2"}' <IP_Logstash>:<port1>/<path1>/<path2>/...
curl -H "content-type: application/json" -d '{"champs1": "test3",champs2": "test4"}' <IP_Logstash>:<port2>/...
```

## Logstash Filter

Le principe du filter Logstash est de processer de la data (venant de l'input) donc de la manipuler, de la mettre dans une forme souhaitée, de la compléter...<br>
Le bloc `filter` se trouve au milieu de la pipeline, entre l'input et l'output (INPUT >> FILTER >> OUTPUT).<br>
Les filters permettent beaucoup de choses dont voici les principales :
  - parser les éléments => à partir d'une ligne, extraire des champs
  - conversion de type => spécifié qu'un champ va être d'un type particulier (<champ1> -> date, <champ2> -> interger,...), pratique avec un ElasticSearch en output par exemple car chaque champ va être vu comme une "string".
  - extraire/checker des IPs
  - répliquer des lignes/événements
  - parser selon des délimiteurs (ou non), pratique avec un format csv par exemple
  - géolocalisation
  - erichissement de datas via d'autres sources
  - faire du parsing connus : csv, json, xml, ...
  - faire de l'aggrégation
  - faire des modification
  - ...

## Logstash Filter CSV

La documentation sur le filter de type `csv` est disponible sur la [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-filters-csv.html).
Dans un cas tout simple, on peut avoir de type de fichier (`/etc/logstash/conf.d/csv.conf`) :
``` 
input {
  file {
    path => "/tmp/input.log"
  }
}
filter {
  csv {
    columns => ["prénom", "nom", "age"]         | <-- va reconnaitre 3 champs 
    separator => ";"                            | <-- qui doivent être tous les 3 séparés par un ";"
    remove_field => [ "message" ]               | <-- falculatif mais pratique pour éviter d'avoir un doublon d'infos puisque les infos seront déjà dans leurs champs respectifs
  }
}
output {
  file {
      path => "/tmp/output.log
  }
}
```
On peut donc tester cette configuration, par exemple, avec un fichier `/tmp/input.log` comme ceci :
```
jean;dupond;25
marie;dubois;30
patrick;le gall;35
```
Il peut être intéressant d'envoyer ces datas dans ElasticSearch après avoir fait des modification grâce au filter, voici un exemple de fichier de configuration Logstash :
```
input {
  file {
    path => "/tmp/input.log"
  }
}
filter {
  csv {
    columns => ["prénom", "passion", "fonction", "ville", "age"]
    separator => ";"
    convert => {
      "age" => "integer"                                          | <-- on converti l'âge en interger.
    }
    add_field => {"env" => "production"}
    add_field => {"dc" => "paris"}
    remove_field => [ "message" ]
  }
}
output {
  elasticsearch {
      hosts => ["localhost:9200"]
      index => "csv-%{+YYYY.MM.dd}"
  }
}
```

## Logstash Filter Date

Le filter date permet d'analyser un champ qui correspond à une date et à l'utiliser comme timestamp de l'évènement (cf [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-filters-date.html#plugins-filters-date-timezone)).<br>
Par exmple on pourrait avoir un fichier `/tmp/input.log` comme ceci :
```
12/07/1998;1ere coupe du monde
15/07/2018;2eme coupe du monde
```
Avec un `/etc/logstash/conf.d/date.conf` :
```
input {
  file {
    path => "/tmp/input.log"
  }
}
filter {
  csv {
    columns => ["mydate", "action"]
    separator => ";"
    }
  date {
    match => [ "mydate", "dd/MM/yyyy" ]     | <-- remplace le timestamp par la date qui a été prise au format "dd/MM/yyyy" dans le champ mydate. Attention voir la doc pour les différents formats
    timezone => "UTC"
  }
}
output {
  file {
    path => "/tmp/output.log"
  }
}
```
On aura donc un output.log comme ceci :
```
{"@version":"1","@timestamp":"1998-07-12T00:00:00.000Z","action":"1ere coupe du monde","host":"elas1","mydate":"12/07/1998","path":"/tmp/input.log","message":"12/07/1998;1ere coupe du monde"}
{"@version":"1","@timestamp":"2018-07-15T00:00:00.000Z","action":"2eme coupe du monde","host":"elas1","mydate":"15/07/2018","path":"/tmp/input.log","message":"15/07/2018;2eme coupe du monde"}
```
Si on injecte ces données dans un ElasticSearch, le timestamp de l'évenement sera bien égal à la date mentionnée dans le `@timestamp`.

## Logstash Filter Mutate

Le filter mutate permet de renommer, supprimer, remplacer et modifier les datas en input, voici les paramètres que l'on peut passer :
  - coerce
  - rename
  - update
  - replace
  - convert
  - gsub
  - uppercase
  - capitalize
  - lowercase
  - strip
  - remove
  - split
  - join
  - merge
  - copy
  
Par exemple on peut avoir un fichier de test `/tmp/input.log` :
```
02/07/2020;github - c'est - la - frappe ?;github.astroworld.com;MAJUSCULE;champ1;champ2;;billyr00t;null
```
Et un fichier de configuration `/etc/logstash/conf.d/config.conf` comme ceci :
```
input{
  file {
    path => "/tmp/input.log"
  }
}

filter {
  csv {
    columns => ["mydate", "action", "split","minuscule","merge1","merge2","coerce","rename","replace"]
    separator => ";"
    remove_field => [ "message" ]
  }
  date {
    match => [ "mydate", "dd/MM/yyyy" ]
  }
  mutate {
    copy => { "[@timestamp]" => "mydate" }                | <-- copie le champ "@timestamp" dans le champ "mydate"
    gsub => ["action", "[?-]", ""]                        | <-- remplace soit les caractère "?" et "-" par rien dans le champ "action"
    split => { "split" => "." }                           | <-- split les différents champs dans un array en fonction du caractère "."
    lowercase => [ "minuscule" ]                          | <-- remplace toutes les majuscules par des minuscules
    merge => { "merge1" => "merge2" }                     | <-- merge dans un array la valeur du champ merge1 avec celle du champ merge2
    coerce => { "coerce" => "default_value" }             | <-- si il y une valeur nulle dans le champ "coerce", "default_value" est inscrit dans ce dernier 
    rename => { "rename" => "apres_rename" }              | <-- renomme le nom du champ "rename" par "apres_rename"
    replace => { "replace" => "%{host}" }                 | <-- remplace la valeur du champ "remplace" par la valeur contenu dans le champ "host"
  }
}
output {
  file {
    path => "/tmp/output.log"
  }
}
```
On aura donc un fichier de sortie comme celui ci :
```
{"merge1":["champ1","champ2"],"mydate":"2020-07-01T22:00:00.000Z","@version":"1","host":"elas1","path":"/tmp/input.log","split":["github","astroworld","com"],"@timestamp":"2020-07-01T22:00:00.000Z","minuscule":"majuscule","merge2":"champ2","coerce":"default_value","replace":"elas1","apres_rename":"billyr00t","action":"github  c'est  la  frappe "}
```
Plus d'infos sur la [doc de Logstash](https://www.elastic.co/guide/en/logstash/current/plugins-filters-mutate.html).

## Logstash Filter Aggregate 

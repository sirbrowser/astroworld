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
Tout d'abord, il faut que logstash est le droit de lecture sur ce fichier : `usermod -aG adm logstash`.<br>
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
On va créer un index Kibana à partir de celui qu'on a créer sur ElasticSearch. Pour cela, on se rend dans la partie "Management" -> "Stack Management". On peut voir dans la partie ElasticSearch --> "Index Management" que l'index a bien été créé. On se rend dans la partie Kibana -> "Index Pattern" et on créé un index à partir de celui créer avec ElasticSearch.<br>
On peut désormais voir dans la partie "Discover" de Kibana que l'index "nginx" est créer et on peut voir les logs.


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
Sur la machine où est installé Nginx et Filebeat, on doit activé le module nginx : `filebeat modules enable nginx`.<br>
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
Voici quelques exemples mais il en existe plein d'autres qui sont très intéressant voir la [doc ElasticSearch](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-input-log.html).

## Filebeat - Input Container

On peut configurer plus spécifiquement les input de types containers avant des les envoyer à Logstash. Il existe plusieurs champs de configurations qui sont disponibles sur la [doc ElasticSearch](https://www.elastic.co/guide/en/beats/filebeat/master/filebeat-input-container.html).<br>
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

On peut configurer plus spécifiquement les input de types TCP avant des les envoyer à Logstash. Il existe plusieurs champs de configurations qui sont disponibles sur la [doc ElasticSearch](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-tcp.html).<br>
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
Si Filebeat écoute sur localhost:9000, lors d'un `echo "pierre paul jacques" | nc 127.0.0.1 9000`, on devrait pouvoir le visualiser sur Kibana mais avant il faudra créer un nouvel index Kibana à partir de celui d'ElasticSearch. Trois champs custom seront donc créer : champ1, champ2 et champ3 avec leur valeur respective : pierre, paul et jacques.

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
Pour les logs syslog, on peut directement activer le module system et activer l'output directement vers elasticsearch, puis `filebeat setup` pour créer directement les index et les dashboards.<br>

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

## Filebeat - Communiquer en TLS avec Logstash

La communication TLS entre Filebeat et Logstash permet d'éviter les injections de systèmes qui n'aurait pas le bon certificat (un attaquant par exemple).<br>
Sur le serveur logstash, on va créer un nouveau fichier identique au fichier `/etc/ssl/openssl.cnf`, on peut faire un `cp /etc/ssl/openssl.cnf /tmp/custssl.conf`.<br>
On va lui rajouter l'adresse IP du serveur logstash en dessous de la catégorie `[ v3_ca ]` :
```
[ v3_ca ]
subjectAltName = IP: <IP_Logstash>
```
Ensuite il faudra créer un certificat à partir de se fichier de configuration : 
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

## Metricbeats | Module System

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

On peut monitorer les metrics de conteneurs docker de la même manière que pour le [module system](#Metricbeats-|-Module-System).



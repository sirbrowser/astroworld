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

## Fichiers locaux

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






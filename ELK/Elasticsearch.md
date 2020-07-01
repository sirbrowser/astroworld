# ElasticSearch

## Intérêts

ElasticSearch est un outil de base de données NoSQL (facilité à disposer d'un système distribué). 

Les principaux moteurs NoSQL :
  - elasticsearch : capacité/qualité d'indexation et donc de recherche
  - cassandra : gros volumes
  - mongodb : la plus polyvalente
  - redis : in memory donc très rapide (requêtage limité)
  
ElasticSearch :
  - indexation de tous les mots du documents
  - qualité de la recherche
    - TF (Terme frequency) : fréquence des mots
    - IDF (Inverse Difference Frequency) : moins un mot est commun, plus il a de poids dans la recherche
  - intérêt important dans l'ELK : analyse de logs

## Installation via docker

ElasticSearch est disponible sur le port 9200.
Le port 9300 permet l'échange de données entre cluster ElasticSearch.

### docker 

`docker run -d --name elasticsearch -v /srv/elas1:/usr/share/elasticsearch/data -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:latest`

### docker-compose

```  
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.8.0    | <-- dernière version dispo le 06/25/2020
    container_name: elasticsearch
    environment:
      - node.name=elas1
      - cluster.name=docker-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - /srv/elas1/:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
      - 9300:9300                                                 | <-- pas forcément nécessaire puisqu'on travaille juste avec un noeud
    networks:
      - esnet

networks:
  esnet:

```

Pour vérifier que l'installation s'est bien déroulée : `curl -X GET "localhost:9200"`. Cette commande restera intéressante pour "ping" le service.<br>

La [doc d'ElasticSearch](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html) propose un docker-compose très bien aussi pour commencer. 

## Création d'index et ajout de datas

ElasticSearch est intérrogeable par requêtes HTTP. On va pouvoir utiliser `curl` pour cela avec plusieurs méthodes :
  - GET : récupérer de la data
  - PUT : création de la data
  - POST : mise à jour
  - bulk : enchainer les insertions
  
Un index peut être vu comme une database. Quand on créé un index, on doit ensuite créer son mapping (= la structure des données qu'il va contenir).
Un type peut être vu comme une table.
Une propriété peut être vu comme un champ.

**Depuis la version 7 d'Elastic, il n'y a plus de type**.

```
curl -X PUT "localhost:9200/database1" -H 'Content-Type: application/json' -d'
{
    "mappings" : {
        "properties" : {
            "nom" : { "type" : "text" },
            "prenom" : { "type" : "text" },
            "ville" : { "type" : "text" }
        }
    }
}
'
```
Ici on va créer un index `database1` et on va créer son mapping en lui renseignant des champs et leurs types respectifs.

Pour l'insertion de datas multiples, on utilise `_bulk` :

```
curl -X POST 'http://localhost:9200/_bulk' -H 'Content-Type: application/json' --data-binary '
{ "create" : { "_index" : "database1", "_id": 1 } }
{"nom": "Dupond", "prenom": "Jean", "ville" : "Caen"}
{ "create" : { "_index" : "database1", "_id": 2 } }
{"nom": "Michu", "prenom": "Paul", "ville" : "Lyon"}
{ "create" : { "_index" : "database1", "_id": 3 } }
{"nom": "Michalon", "prenom": "Pierre", "ville" : "Marseille"}'
```
  
Sinon on peut utiliser une requête POST simple :

```
curl -X POST 'http://localhost:9200/database1/_create/4' -H 'Content-Type: application/json' --data-binary '
{"nom": "Boy", "prenom": "Billy", "ville" : "Paris"}'
```

Si on relance la même commande, il y aura conflit. Pour update des champs d'un même id, on utilise `_doc` au lieu de `_create`.
```
curl -X POST 'http://localhost:9200/database1/_doc/4' -H 'Content-Type: application/json' --data-binary '
{"nom": "Boy", "prenom": "Billyboy", "ville" : "Paris"}'
```

Pour request de la data, on utilise la méthode `GET` : `curl -X GET 'http://localhost:9200/database1/_doc/4' -H 'Content-Type: application/json'`
  
## Recherches

### Simples

On utilise le paramètre `_search` pour fait des recherches dans la database que l'on souhaite : 

On spécifie l'index dans lequel on va vouloir rechercher les datas (ici `database1`), si on veut requêter toutes les datas de l'index  :<br>
`curl -X GET "localhost:9200/database1/_search" | jq`
 
On peut ajouter le paramètre `q` qui fait office de filtre :<br>
`curl -X GET "localhost:9200/database1/_search?q=Michu" | jq` 

On peut ajouter plusieurs filtres :<br>
`curl -X GET "localhost:9200/database1/_search?q=Michu+Boy" | jq`

On peut aussi pousser le filtre sur un champ en particulier :<br>
`curl -X GET "localhost:9200/database1/_search?q=nom:Michu" | jq`

On peut aussi rechercher dans plusieurs indexs :<br>
`curl -X GET "localhost:9200/database1,database2/_search?q=nom:Michu" | jq`<br>
`curl -X GET "localhost:9200/_all/_search?q=nom:Michu" | jq`

On peut rechercher des données puis filtrer l'ouput pour n'avoir que certaines properties, voici des exemples :<br>
`curl localhost:9200/database1/_search?_source_includes=messages | jq`<br>
`curl localhost:9200/database1/_search?_source_includes=@timestamp | jq`

On peut retrouver tous les indexes d'ElasticSearch :<br>
`curl 127.0.0.1:9200/_cat/indices`<br>

On utilise la commande `jq` pour **présenter** le résultat en json.

### Complexes

On peut faire des recherches plus complexes en passant des données sous formats json :<br>
Le cas d'un match simple sur une properties :<br>
``` 
curl -X GET "localhost:9200/database1/_search" -H 'Content-Type: application/json' -d '
{
  "query" :{
     "match" :{
        "prenom" : "BillyBoy+blog"
     }
  }
}' | jq
```

Sur plusieurs properties :<br>
```
curl -X GET 'http://127.0.0.1:9200/database1/_search' -H 'Content-Type: application/json' -d '
{
    "query": {
        "multi_match" : {
            "query" : "paul+xavier",
            "fields" : ["prenom", "nom"]
        }
    }
}' | jq
```

On peut augmenter la pondération d'un properties :<br>
Cela va jouer sur le **score** qu'a obtenu le match en question.<br>
```
curl -X GET 'http://127.0.0.1:9200/database1/_search' -H 'Content-Type: application/json' -d '
{
    "query": {
        "multi_match" : {
            "query" : "paul+xavier",
            "fields" : ["prenom^3", "nom"]
        }
    }
}' | jq
```

On peut limiter le nombre de properties en output :<br>
```
curl -X GET 'http://127.0.0.1:9200/database1/_search' -H 'Content-Type: application/json' -d '
{
    "query": {
        "multi_match" : {
            "query" : "paul+xavier",
            "fields" : ["prenom^3", "nom"]
        }
    },
    "_source": ["prenom", "nom"]
}' | jq
```

## Mettre en place des clusters

On peut avoir différents types de serveur :
  - data node : stock les datas, recherche, agrégation
  - master node : en charge du cluster (configuration...)
  - client node : transmet les requêtes (master et noeuds de datas)
  - ingest node : preprocessing

Un serveur peut être de plusieurs types.

On installe ElasticSearch (7.8.0) sur 2 machines distinctes (2 Debian 10): <br>
``` 
apt-get install -y default-jre apt-transport-https
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.0-amd64.deb
dpkg -i elasticsearch-7.8.0-amd64.deb
```
Avant de lancer le service, changeons la configuration :

### elasticsearch.yml

On aura au minimun :
```
cluster.name: <nom_du_cluster>
node.name: <nom_de_la_machine>
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
discovery.seed_hosts: ["<IP_machine>", "<IP_machine2>", ....]
network.bind_host: 0.0.0.0                                      | <-- Pour que le service écoute sur tous les interfaces
node.master: true                 
node.data: true
network.host: <IP_machine>
```

### jvm.options

On peut fixer une limite (ici 500Mo) à la mémoire allouée pour elastic (1Go par défaut) :<br>
```
-Xms500m
-Xmx500m
``` 

On peut s'assurer de la bonne configuration du cluster avec la commande : `curl <node_IP>:9200/_cluster/health | jq` qui retourne un certain nombre d'informations.<br>
On peut aussi voir l'état du cluster (même chose avec elasticsearch-hq) avec la commande : `curl -X GET "<node_IP>:9200/_cat/nodes?v&pretty"`

## Définitions d'architecture

**Cluster** : ensemble de serveurs (noeuds ayant elasticsearch / même id de cluster)
  - communication via port 9300
  - haute dispo : perfomance et redondance

**Noeuds** : serveur ayant un service elastic
  - différents types : master, data, client...

**Index** : une instance de base de données 
  - un à plusieurs par serveur (et cluster) 
  
**Shards** : découpage logique d'un index (un à plusieurs shards)
  - répartition des shards sur plusieurs noeuds (répartir un index)
  - joue sur les performances
	- ajout d'un noeud = réaffectation des shards
	- important pour déterminer nb max de noeuds
  
**Réplicas** : réplicas de shards d'un index
  - redondance
	- mais aussi performance (interrogeables)
  
**Requête** : via API et somme des résultats de tous les shards

## Définitions d'index

**Type** (table) : regroupement de documents
	- structure n'est pas fixe mais évolutive
	- on peut la définir par un mapping

**mapping** : définition de les propriétés du type
  - par exemple : les noms des champs, leur caractéristiques

**Document** : élément le plus fin (équivaut à une ligne en sql)
  - un objet d'un type
	- composé des propriétés du type
  
## Plug-in Elastic

Pour installer des plug-in ElasticSearch :<br>
`/usr/share/elasticsearch/bin/elasticsearch-plugin install list`

Le plug-in elastic-hq permet d'avoir une interface graphique d'elastic très pratique pour la gestion de cluster. <br>
Il est disponible avec docker (à faire sur la machine qui fait tourner un service elastic) :
`docker run -d -p 5000:5000 elastichq/elasticsearch-hq`





  
  
  
  
  

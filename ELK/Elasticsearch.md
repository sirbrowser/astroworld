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

Pour vérifier que l'installation s'est bien déroulée : `curl -X GET "localhost:9200"`
Cette commande restera intéressante pour "ping" le service.

## Création d'index et ajout de datas

ElasticSearch est intérrogeable par requêtes HTTP. On va pouvoir utiliser `curl` pour cela avec plusieurs méthodes :
  - GET : récupérer de la data
  - PUT : création de la data
  - POST : mise à jour
  - bulk : enchainer les insertions
  
Un index peut être vu comme une database. Quand on créé un index, on doit ensuite créer son mapping (= la structure des données qu'il va contenir).
Un type peut être vu comme une table.
Une propriété peut être vu comme un champ.

Depuis la version 7 d'Elastic, il n'y a plus de type.

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
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

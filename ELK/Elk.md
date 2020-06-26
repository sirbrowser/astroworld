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

## Installation d'ElasticSearch

### Théorie

ElasticSearch utilise NoSQL qui facilite l'utilisation d'un système distribué.

Les principaux conccurents :
  - Cassandra : Traitement de gros volumes
  - MongoDB : La plus polyvalente
  - Redis : Traitement *in memory* donc très rapide mais avec un requêtage limité
  
ElasticSearch permet d'indexer tous les documents qui lui parviennent. <br>
Sa qualité de recherche repose sur deux éléments :
  - TF (Terme Frequency) : fréquence des mots
  - IDF (Inverse Difference Frequency) : moins un mot est commun, plus il a de poids dans la recherche 
  
Pour plus d'informations sur ElasticSearch voir [ElasticSearch.md](ElasticSearch.md)


  





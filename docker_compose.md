# Docker Compose

### Index
- [What is docker compose?](#what-is-docker-compose)
- [Deploiement d'une application avec plusieurs services](#deploiement-dune-application-avec-plusieurs-services)
- [Networks](#networks)
- [Volumes](#volumes)
- [Traefik](#traefik)
- [Dockprom](#dockprom)
- [Scaling](#scaling)
- [Portainer](#portainer)
- [Stack wordpress/mysql](#stack-wordpressmysql)
- [Phpmyadmin](#Phpmyadmin)
- [Prometheus et graphana](#Prometheus-et-graphana)
- [Jenkins](#Jenkins)
- [Gitlab](#Gitlab)
- [Postgresql](#Postgresql)
- [Cassandra](#Cassandra)
- [Mariadb](#Mariadb)


#### What is docker compose?

**Why ?**
- Coordination des conteneurs
- Meilleure gestion des dépendances (réseau, volumes...)
- C'est un orchestrateur docker
- partage facile et versionning

**Princiales commandes**
- un répertoire avec docker-compose.yml
- commandes similaires à docker
- `docker-compose build` --> construction uniquement des images
- `dokcer-compose up` --> build et run des images
- `docker-compose up -d` --> en mode detached

`docker-compose scale <service_name>=3` --> lance 3 instances de service<br>

Exemple d'un docker-compose.yml :
```
version: '3'
services:
  myfirstservice:
    image: alpine
    restart: always
    container_name: MyAlpine
    entrypoint: ps aux
```

`docker-compose logs` --> resultats de la commande passé dans l'entrypoint<br>

#### Deploiement d'une application avec plusieurs services

Dans un répertoire :
- docker-compose.yml
- Dockerfile --> creation de l'image applicative
- app.py --> contient l'applicatif
- requirements.txt --> contient la liste des modules pip pour l'image
- script shell de test

Redis is an open-source data structured store used as a database, cache and message broker. It works on Linux and OSX systems.
Flask is an open-source framework in python used as development server and debugger and template engine for HTML. It is very light under BSD license.

*dockercompose.yml :*
```
version: '3'
services:
  app:      --> first service
    build: .
    image: flask-redis:1.0 --> image_name + version that we want to create
    environment:
      - FLASK_ENV=development
    ports:
      - 5000:5000
  redis:    --> second service
    image: redis:4.0.11-alpine
```
    
*Dockerfile (used by dockercompose.yml in app to create the image flask-redis) :*
```
FROM python:3.7.0-alpine3.8
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .    --> copy host directory to /usr/src/app
ENV FLASK_APP=app.py
CMD flask run --host=0.0.0.0
```

*requirements.txt :*
```
flask
redis
```

*app.py :*
```python
from flask import Flask, request, jsonify
from redis import Redis

app = Flask(__name__)
redis = Redis(host="redis", db=0, socket_timeout=5, charset="utf-8", decode_responses=True)

@app.route('/', methods=['POST', 'GET'])
def index():
  
  if request.method == 'POST':
    name = request.json['name']
    redis.rpush('students', name)             --> if the method is POST we do an insert or update in table students
    return jsonify({'name': name})
    
  if request.method == 'GET':
    return jsonify(redis.lrange('students', 0, -1))     --> if the method is GET we get back all data in table students
```

Then we need to do :
`docker-compose up -d`    --> -d for the detach mode<br>

*post-get.sh* To test :
```sh
#!/bin/bash

echo "GET on database before POST:"
curl localhost:5000

echo "POST..."
curl --header "Content-Type: application/json" --request POST --data '{"name": "browser"}' localhost:5000

echo "GET on database after POST"
curl localhost:5000
```

`docker-compose down`     --> supprime les docker qui ont été lancés en une seule commande<br>

#### Networks

Dans *docker-compose.yml* on peut specifier :
```
version: '3'
services:
  app:
    build: .
    image: flask-redis:1.0
    environment:
      - FLASK_ENV=development
    ports:
      - 5000:5000
    networks:     |
      - backend   | --> uses backend and frontend networks
      - frontend  | 
  redis:
    image: redis:4.0.11-alpine
    networks:
      - backend   --> uses backend network
      
 networks:        |
   backend:       | --> create 2 networks 
   frontend:      |
```

#### Volumes

Avec docker dans *Dockerfile* :
```
redis:
  image: redis:4.0.11-alpine
  networks:
    - backend
  volumes:
    - dbdata:/data
  
volumes:
  dbdata:
```
Ici on laisse docker gérer les volumes, or on veut pouvoir définir plus précisément nos volumes en utilisant docker-compose.
Avec docker-compose dans *docker-compose.yml* :
```
version: '3'
services:
  app:
    build: .
    image: flask-redis:1.0
    environment:
      - FLASK_ENV=development
    ports:
      - 5000:5000
    networks:
      - backend
      - frontend
  redis:
    image: redis:4.0.11-alpine
    networks:
      - backend
    volumes:
      - dbdata: /data  --> uses volume dbdata
      
networks:
  backend:
  frontend:

volumes:
  dbdata:
    driver: local
    driver_opts:
      type: 'none'
      o: 'bind'
      device: '/srv/redis' --> host volume
```

`docker-compose up -d --build` --> to apply volume information and mount it<br>

To test it we can do a `docker-compose down` and then `docker-compose up -d` and with running the script *./post-get.sh* we can see that our data have been saved by the volume even if we down the docker.<br>

#### Traefik

Traefik est un reverse proxy pour conteneurs, il permets de :
- ne pas utiliser les ip des conteneurs
- valable pour plusieurs url et plusieurs conteneurs
- maintenir des url
- maintenir du service traefik (toujours up)
- load balancing si scaling

Il est lui même un conteneur!

[Présentation de Traefik](https://www.youtube.com/watch?v=QvAz9mVx5TI)

Sans Traefik :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/Capture.PNG><br>

Avec Traefik :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/with-traefik.png><br>

**Example d'utilisation** 
Le *docker-compose.yml* de Traefik:
```
version: "3"
services:
  traefik:
    image: traefik    ===> METTRE traefik:v1.7.16 SINON CA MARCHE PAS
    command: --web --docker --docker.domain=docker.localhost --loglevel=DEBUG
    ports:
      - "80:80"
      - "8080:8080"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock   --> traefik a besoin de la socket docker
      - /dev/null:/etc/traefik/traefik.toml     --> traefik.toml = fichier de conf de traefik qu'on partage avec la machine host
    networks:
      - webgateway
networks:
  webgateway:             --> traefik a besoin de son propre réseau docker
    driver: bridge
```

Le *docker-compose.yml* global :
```
version: '3'
services:
  app:
    build: .
    image: flask-redis:1.0
    environment:
      - FLASK_ENV=development
    expose:
      - "80"
    networks:
      - traefik
    labels:
      - "traefik.docker.network=traefik"      --> on spécifie le réseau qu'on doit utiliser
      - "traefik.backend=browser"             --> on donne un nom à l'interface graphique de traefik
      - "traefik.frontend.rule=Host:browser.localhost"    --> on précise l'host sur lequel trafeik va tourner
      - "traefik.port=80"
    redis:
      image: redis:4.0.11-alpine
      networks:
        - traefik
networks:
  traefik:
    external:
      traefik_webgateway   --> nom du réseau défini dans le docker-compose.yml de Traefik
```

Le dashboard de Traefik :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/traefik-dashboard.png><br>

#### Dockprom

[Github de dockprom](https://github.com/stefanprodan/dockprom)

Dockprom c'est :
- prometheus (serveur de supervision)
- grafana (data visualisation métriques)
- cAdvisor (collecte de métriques sur conteneurs)
- alertmanager (gestion d'alertes)
- nodeexporter (export de métriques)
- pushgateway (pousser des métriques personnalisées)
- caddy (reverse proxy pour conteneurs)

Installation de dockprom :
```
git clone https://github.com/stefanprodan/dockprom
cd dockprom
docker-compose up -d
```

- Prometheus (peu utilisé) dashboard (port 9090 par défaut) :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/prometheus-dashboard.png><br>

- Grafana (port 3000 par défaut) :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/grafana-dashboard.png><br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/grafana-dashboard1.png><br>

To increase traffic and watch grafana running we can run :
`while True; do ./post-get.sh; done`<br>
As a result we can see that there is an increase in network traffic for example in grafana :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/grafana-dashboard2.png><br>

#### Scaling

Permets d'avoir plusieurs conteneurs applicatifs sur la même base de données<br>
Sans scaling :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/without-scaling.png><br>

Avec scaling :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/with-scaling.png><br>

`docker-compose up -d scale <servie_name>=2`<br>
On a beaucoup plus d'options en utilisant le cluster docker swarm.<br>

#### Portainer
Permet :
- interface graphique de gestion docker
- d'effectuer des actions sur les conteneurs y compris la création
- détails sur les conteneurs
- métrique de conteneur
- logs des conteneurs
- console du conteneur
- gestion des images
- réseaux
- volumes
- template de conteneurs
- visualisation de Swarm (nodes)
- gestion des services (compose et swarm)
- gestion des endpoints (ajout de serveur à portainer)

`docker -H tcp://0.0.0.0:2375 ps -a` --> mise en place de la socket d'ecoute sur tous les conteneurs

Mise en place :
`mkdir portainer`<br>
Dans le *docker-compose.yml* :
```
version: '2'
services:
  portainer:
    image: portainer/portainer
    expose:
      - "9000"
    networks:
      - traefik
    labels:
      - "traefik.docker.network=traefik"
      - "traefik.frontend.rule=Host:portainer.localhost"
      - "traefik.port=9000"
      - "traefik.backend=portainer"
      - "traefik.frontend.entryPoints=http"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"

networks:
  traefik:
    external:
      name: traefik_webgateway
```

`docker-compose up -d`<br>

Dashboard portainer :<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/portainer.png><br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/portainer2.png><br>
Then we select the network related to that ip and :<br>
`ifconfig | grep 172.18.0`
Then the result is the endpoint url in portainer.

Un exemple de page du dashboard, enormément d'options sont disponibles :
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/portainer3.png><br>

#### Stack wordpress/mysql
The *docker-compose.yml* is :
```
version: '3.3'

services:
  db:
    container_name: mysql
    image: mysql:5.7
    volumes:
      - wp_db:/var/lib/mysql/		--> where mysql store data
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    networks:
      - wp

  wordpress:
    depends_on:
      - db				--> start only if db is already running
    container_name: wordpress
    image: wordpress:latest
    volumes:
      - wp_statics:/var/www/html
    ports:
      - 8000:80
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306	--> default port of mysql
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
    networks:
      - wp

networks:
  wp:

volumes:
  wp_db:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/wordpress/db
  wp_statics:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/wordpress/statics
```
Then we need to create or directory that we specified in volumes (/srv/wordpress/db & /srv/wordpress/statics)<br>

We can then go on port 8000 which is the interface of wordpres to setup configuration of it.
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/wordpress.png><br>

And we have the dashboard of wordpress:<br>
<img src=https://github.com/sirbrowser/astroworld/blob/master/images/wordpress1.png><br>


#### Phpmyadmin

```
phpmyadmin:
     depends_on:
       - db							| <-- nom du service qui porte le conteneur de la base de donnees
     container_name: phpmyadmin
     image: phpmyadmin/phpmyadmin
     restart: always
     ports:
       - 7777:80
     environment:
       PMA_HOST: db						| <-- nom du service qui porte le conteneur de la base de donnees
       MYSQL_ROOT_PASSWORD: password				| <-- password qui a ete instancie dans le service qui porte le conteneur de la base de donnees
     labels:
      - "traefik.docker.network=traefik"			|
      - "traefik.backend=phpmyadmin"				| labels obligatoires lors de l'utilisatation de traefik si on l'utilise
      - "traefik.frontend.rule=Host:phpmyadmin.localhost"	|
      - "traefik.port=80"					|
     networks:
     - wp							| <-- meme reseau de la base de donnees et le service web
     - webgateway						| <-- on peut specifier le reseau de traefik si on l'utilise 
```

#### Prometheus et graphana

Pour utiliser traeafik avec prometheus , il faut l'instance le service comme ceci

```
traefik:
     image: traefik:v1.7.16
     container_name: traefik
     command: --web --web.metrics.prometheus --web.metrics.prometheus.buckets="0.1,0.3,1.2,5.0" --docker --docker.domain=docker.localhost --logLevel=DEBUG	| <-- les metrics de prometheus + buckets
     ports:
       - "80:80"
       - "8080:8080"
       - "443:443"
     volumes:
       - /var/run/docker.sock:/var/run/docker.sock
       - /dev/null:/etc/traefik/traefik.toml
     networks:
       - webgateway
       
```

Pour prometheus :

``` 
prometheus:
     image: quay.io/prometheus/prometheus:v2.0.0
     container_name: prometheus
     volumes:
      - prom:/etc/prometheus/
      - prom_data:/prometheus/
     command: "--config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/prometheus"	| <-- Le fichier de configuration et les data de prometheus
     ports:
      - 9090:9090
     labels:
      - "traefik.docker.network=traefik"			|
      - "traefik.backend=prometheus"				| Les labels obligatoires si on veut utiliser traefik
      - "traefik.frontend.rule=Host:prometheus.localhost"	|
      - "traefik.port=9090"					|
     networks:
      - webgateway						| Le reseau de traefik
     
```


Pour graphana :

```
grafana:
     image: grafana/grafana
     container_name: grafana
     ports:
      - 3000:3000
     volumes:
      - graf_data:/var/lib/grafana				| Les datas de graphana
      - graf:/etc/grafana/provisioning/				| L'approvisionnement de grapaha
     labels:
      - "traefik.docker.network=traefik"			| Les labels obligatoires si on veut utiliser traefi
      - "traefik.backend=grafana"				|
      - "traefik.frontend.rule=Host:grafana.localhost"		|
      - "traefik.port=3000"
     networks:
      - webgateway						| Le reseau de traefik
     depends_on:
      - prometheus
```

##### Ne pas oublier les volumes 

Il faut s'assurer que chaque directory present dans la section device est bien cree sur la machine hote

```
prom:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/wordpress/prometheus		
  prom_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/wordpress/prometheus_data
  graf:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/wordpress/grafana
  graf_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/wordpress/grafana_data
```

### Jenkins 

"Jenkins est un outil logiciel d’intégration continu. Il s’agit d’un logiciel open source, développé à l’aide du langage de programmation Java. Il permet de tester et de rapporter les changements effectués sur une large base de code en temps réel. En utilisant ce logiciel, les développeurs peuvent détecter et résoudre les problèmes dans une base de code et rapidement. Ainsi les tests de nouveaux builds peuvent être automatisés, ce qui permet d’intégrer plus facilement des changements à un projet, de façon continue. L’objectif de Jenkin est en effet d’accélérer le développement de logiciels par le biais de l’automatisation. Jenkins permet l’intégration de toutes les étapes du cycle de développement." (cf. https://www.lebigdata.fr/jenkins-definition-avantages)
Tutoriel utilisation Jenkins : https://www.ionos.fr/digitalguide/sites-internet/developpement-web/tutoriel-jenkins/


**Attention a bien creer chaque directory, present dans les volumes, sur la machine hote.**

```
version: '3'
services:
  jenkins:
    image: 'jenkins/jenkins:lts'
    container_name: jenkins
    user: 0:0
    ports:
      - '8080:8080'
      - '443:8443'
      - '50000:50000'
    volumes:
      - 'jenkins_data:/var/jenkins_home/'
    networks:
     - generator
volumes:
  jenkins_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: srv/jenkins/                          | --< il faut creer ce dossier sur la machine hote
networks:
  generator:
   driver: bridge
   ipam:
     config:
       - subnet: 192.168.168.0/24                   | <-- on peut configurer la plage d'adresse du reseau
```
Le service jenkins met environ 15 secondes a se lancer. Il demandera un **token d'administration**, il est present dans les logs du conteneur jenkins

#### GitLab

```
version: '3.0'
services:
  gitlab:
   image: 'gitlab/gitlab-ce:latest'
   container_name: gitlab
   hostname: 'gitlab.example.com'                             | <-- important pour le fonctionnement
   environment:
     GITLAB_OMNIBUS_CONFIG: |                                 |
       external_url 'https://gitlab.example.com'              | <-- url qui permet l'acces au gitlab
   expose: 
   - 5000
   ports:
   - 80:80
   - 443:443
   - 5000:5000
   volumes:
   - gitlab_config:/etc/gitlab/
   - gitlab_logs:/var/log/gitlab/
   - gitlab_data:/var/opt/gitlab/
   networks:
   - generator     
volumes:
  gitlab_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: srv/gitlab/data
  gitlab_logs:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: srv/gitlab/logs
  gitlab_config:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: srv/gitlab/config
networks:
  generator:
   driver: bridge
   ipam:
     config:
       - subnet: 192.168.168.0/24
```

#### Postgresql

"PostgreSQL is a powerful, open source object-relational database system" --> more informations here : https://www.postgresql.org/
```
version: '3.0'
services:
  postgres:
   image: postgres:latest
   container_name: postgres
   environment:
   - POSTGRES_USER=myuser                           | <-- 
   - POSTGRES_PASSWORD=myuserpassword               | <-- on peut directement mettre des identifiants du compte root 
   - POSTGRES_DB=mydb                               | <-- nom de la database
   ports:
   - 5432:5432
   volumes:
   - postgres_data:/var/lib/postgresql/
   networks:
   - generator     
volumes:
  postgres_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: srv/postgres                          | <-- Attention a bien creer ce directory sur la machine hote
networks:
  generator:
   driver: bridge
   ipam:
     config:
       - subnet: 192.168.168.0/24                   | <-- On configure une plage reseau
```

On peut acceder au command prompt du service avec la commande `psql -h <ip_du_conteneur> -U <nom_user_cree> <nom_de_la_base_creee>`

#### Cassandra

"Apache Cassandra est un système de gestion de base de données (SGBD) de type NoSQL conçu pour gérer des quantités massives de données sur un grand nombre de serveurs, assurant une haute disponibilité en éliminant les points individuels de défaillance. Il permet une répartition robuste sur plusieurs centres de données, avec une réplication asynchrone sans master et une faible latence pour les opérations de tous les clients"

```
version: '3'
services:
  cassandra:
    image: bitnami/cassandra:latest
    container_name: cassandra
    volumes:
    - cassandra_data:/bitnami
    ports:
    - 9042:9042 # cqlsh
    - 7199:7199 # jmx
    - 7000:7000 # internode communication
    - 7001:7001 # tls internode
    - 9160:9160 # client api
    networks:
    - generator
volumes:
  cassandra_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/cassandra/                               
networks:
  generator:
   driver: bridge
   ipam:
     config:
       - subnet: 192.168.168.0/24
```

Pour se connecter au command prompt de cassandra : `docker exec -ti cassandra cqlsh -u cassandra -p cassandra`.
cassandra/cassendra est l'utilisateur par defaut a la creation.

#### Mariadb

```
version: '3'
services:
  mariadb:
    container_name: mariadb
    image: mariadb/server:latest
    volumes:
     - mariadb_data:/var/lib/mysql/                       | <-- la ou mariadb stock les datas
    environment:
      MYSQL_ROOT_PASSWORD: myrootpassword                 | <-- mot de passe root
      MYSQL_DATABASE: mydatabase                          | <-- nom de la database que l'on cree
      MYSQL_USER: myuser                                  | <-- nom du user
      MYSQL_PASSWORD: myuserpassword                      | <-- password du user
    ports:
    - 3306:3306
    networks:
    - generator
volumes:
  mariadb_data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: /srv/mariadb/                                                     
networks:
  generator:
   driver: bridge
   ipam:
     config:
       - subnet: 192.168.168.0/24
```

Pour se connecter a la database mariadb `mysql -h <ip_du_conteneur> -u <user> -p`







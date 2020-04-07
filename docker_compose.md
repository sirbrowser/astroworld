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

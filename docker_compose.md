# Docker Compose

### Index
- [What is docker compose?](#what-is-docker-compose)
- [Deploiement d'une application avec plusieurs services](#deploiement-dune-application-avec-plusieurs-services)
- [Networks](#networks)
- [Volumes](#volumes)
- [Traefik](#traefik)




#### What is docker compose?

**Why ?**
- Coordination des conteneurs
- Meilleure gestion des dépendances (réseau, volumes...)
- C'est un orchestrateur docker
- partage facile et versionning

**Princiales commandes**
- un répertoire avec docker-compose.yml
- commandes similaires à docker

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

Il est lui même un docker!

[Présentation de Traefik](https://www.youtube.com/watch?v=QvAz9mVx5TI)

Sans Traefik :<br>

[logo]: https://github.com/sirbrowser/astroworld/blob/master/images/Capture.PNG


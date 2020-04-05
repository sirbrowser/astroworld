# Docker Compose

### Index
- [What is docker compose?](#what-is-docker-compose)
- [Deploiement d'une application avec plusieurs services](#deploiement d'une application avec plusieurs services)






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
```

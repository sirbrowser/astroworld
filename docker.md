# Docker    

### Index
- [Commandes docker de base](#commandes-docker-de-base)
- [Volumes](#volumes)
- [Images](#images)
- [Dockerfile and Layers](#dockerfile-and-layers)
- [Cache](#cache)
- [Networks](#networks)
- [Sécurité](#securite)
- [Docker registry](#docker-registry)
    
    
#### Commandes docker de base
`docker ps` --> list dockers running<br>
    
`docker run -tid -p <port source>:<port destination> --name <docker_name> <image>:<img_version>` --> run a docker with port redirection<br>
    
`docker exec -ti <docker_name> sh` --> enter in a docker with shell bash<br>
    
`docker inspect <docker_name>` --> information about docker<br>
    
`docker start <docker_name>` --> start a docker which was stopped in docker ps -a<br>
    
`docker rm -f <docker_name>` --> force deletion of a docker<br>
    
`docker run ... --env <MYVARIABLE>="1234"` --> set an environment variable in a docker<br>
`docker run ... --env-file <variable_file>`<br>
`docker run ... --hostname <hostname>` --> set an hostname for the docker<br>
    
#### Volumes
`docker run ... -v <local_path_to_share>:<docker_path>` --> share local volume to docker<br>
    
    docker volume create <myvolume><br>
    docker volume inspect <myvolume><br>
    
    docker run ... --mount source:<myvolume>,target=<target_path><br>
    
#### Images
`docker image ls` --> list pulled images
`docker commit <container_ID> <image_name>:<version>` --> create image from a docker

#### Dockerfile and Layers
Dockerfile permets de : 
- créer une image
- relancer une création d'image à tout moment
- partager facilement et giter facilement

Il y a deux couches sur docker :
  - Read only
  - Read-Write
  
**En Read only :**
Dans Dockerfile :
    FROM <image>:<version>
`RUN apt-get update` --> couche 1
`RUN apt-get install -y nano` --> couche 2
`RUN apt-get install -y git` --> couche 3

`docker history <myimage>:<myversion>`   --> list layers

**En Read-Write :**
    docker run ... <docker_name> ...
    docker exec -ti <docker_name> sh
    touch toto
    rm -rf srv/
    
`docker diff <docker_name>` --> A for append, D for drop ...

`docker run --volumes-from <other_docker>` --> share volume from an other docker

#### Cache 
Le cache docker permets de construire plus vite les images et de permettre le partage de couches
Il faut faire attention à l'ordre de définition dans le Dockerfile et utiliser la commande *--no-cache* pour des commandes telles que *apt-get update*

#### Networks
Par défaut le réseau docker est en bridge sur l'interface *docker0* ce qui permets la communication inte-docker
Il faut faire attention au fait qu'il n'y a pas d'IP fixes et donc si un docker est supprimé puis restart il se peut qu'il ne possède pas la même IP.

`docker network create -d bridge --subnet <IP+mask> <mynetwork>` --> create a network
`docker run ... --network <mynetwork>` --> connect the docker to that network
    
#### Sécurité
L'image *docker bench* permets de detecter des failles présentes sur un docker

`docker push login`  --> pour dockerhub
`docker push registry.github.com/...` --> pour github, gitlab ect
    
Dans */etc/systemd/system/docker.service.d/startup_options.conf* :
    [Service]
    ExecStart=
    ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
puis
`systemctl daemon-reload
systemctl restart docker`

Ceci permets de créer une socket d'écoute pour gérer docker en remote
**Le port 2375 si pas de certif / le port 2376 avec certif**

-----------------------------------------------------------------------

Docker multi-stage --> plusieurs FROM dans un seul Dockerfile

-----------------------------------------------------------------------

#### Docker registry
1) Generate auto-signed cert --> `openssl req -x509 -newkey rsa:4096 -nodes -keyout certs/myregistry.key -out certs/myregistry.crt -days 365 -subj /CN=myregistry.my`
2) Create user/password --> `docker run ... --entrypoint htpasswd registry:2 -Bbn <username> <password> > <path_to_file>`
3) Write a docker compose (docker-compose.yml)

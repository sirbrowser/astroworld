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
- [Launch dockers with systemd](#launch-dockers-with-systemd)

    
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

Pour debuger on peut utiliser :
`docker logs <container_name>`<br>    
#### Volumes
`docker run ... -v <local_path_to_share>:<docker_path>` --> share local volume to docker<br>
    
    docker volume create <myvolume>
    docker volume inspect <myvolume>
    
    docker run ... --mount source:<myvolume>,target=<target_path>
    
#### Images
`docker image ls` --> list pulled images<br>
`docker commit <container_ID> <image_name>:<version>` --> create image from a docker<br>
`docker save -o <output_name>.tar <image_name>:<version>` --> create a .tar file of an image, in addtition we can compress the file with gzip.<br>
`docker load < <file_name>.tar.gz` or `docker load --input <file_name>.tar` --> load an image from a .tar file or .tar.gz file 

#### Dockerfile and Layers
Dockerfile permets de : <br>
- créer une image<br>
- relancer une création d'image à tout moment<br>
- partager facilement et giter facilement<br>

Il y a deux couches sur docker :<br>
  - Read only<br>
  - Read-Write<br>
  
**En Read only :**
Dans Dockerfile :<br>
    FROM <image>:<version><br>
`RUN apt-get update` --> couche 1<br>
`RUN apt-get install -y nano` --> couche 2<br>
`RUN apt-get install -y git` --> couche 3<br>

`docker history <myimage>:<myversion>`   --> list layers<br>

**En Read-Write :**

```    
    docker run ... <docker_name> ...
    docker exec -ti <docker_name> sh
    touch toto
    rm -rf srv/
```

`docker diff <docker_name>` --> A for append, D for drop ...<br>

`docker run --volumes-from <other_docker>` --> share volume from an other docker<br>

#### Cache 
Le cache docker permets de construire plus vite les images et de permettre le partage de couches<br>
Il faut faire attention à l'ordre de définition dans le Dockerfile et utiliser la commande *--no-cache* pour des commandes telles que *apt-get update*<br>

#### Networks
Par défaut le réseau docker est en bridge sur l'interface *docker0* ce qui permets la communication inte-docker<br>
Il faut faire attention au fait qu'il n'y a pas d'IP fixes et donc si un docker est supprimé puis restart il se peut qu'il ne possède pas la même IP.<br>

`docker network create -d bridge --subnet <IP+mask> <mynetwork>` --> create a network<br>
`docker run ... --network <mynetwork>` --> connect the docker to that network<br>
    
#### Sécurité
L'image *docker bench* permets de detecter des failles présentes sur un docker<br>

`docker push login`  --> pour dockerhub<br>
`docker push registry.github.com/...` --> pour github, gitlab ect<br>
    
Dans */etc/systemd/system/docker.service.d/startup_options.conf* :

```
    [Service]
    ExecStart=
    ExecStart=/usr/sbin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
```
<span style="color: #26B260"> ATTENTION CES CONNARD DE DEVS ONT MIS /usr/bin dans la doc alors que c'est /usr/sbin!!!!!!</span>
Mdrrr askip ils ont voulu que niquer Benjamin moi c'est bien dans /usr/bin, mettez du respect sur le nom des devs bordel


puis<br>
`systemctl daemon-reload
systemctl restart docker`

Ceci permets de créer une socket d'écoute pour gérer docker en remote<br>
**Le port 2375 si pas de certif / le port 2376 avec certif**<br>

-----------------------------------------------------------------------

Docker multi-stage --> plusieurs FROM dans un seul Dockerfile<br>

-----------------------------------------------------------------------

#### Docker registry
1) Generate auto-signed cert --> `openssl req -x509 -newkey rsa:4096 -nodes -keyout certs/myregistry.key -out certs/myregistry.crt -days 365 -subj /CN=myregistry.my`<br>
2) Create user/password --> `docker run ... --entrypoint htpasswd registry:2 -Bbn <username> <password> > <path_to_file>`<br>
3) Write a docker compose --> in docker-compose.yml :

```
    version: "3.5"
    services: 
     registry:
      restart: always
      image: registry:2
      container_name: registry
      ports:
       - 5000:5000
      environment:
       REGISTRY_HTTP_TLS_CERTIFICATE: /certs/myregistry.crt
       REGISTRY_HTTP_TLS_KEY: /certs/myregistry.key
       REGISTRY_AUTH: htpasswd
       REGISTRY_AUTH_HTPASSWD_PATH: /auth/htpasswd
       REGISTRY_AUTH_HTPASSWD_REALM: Registry Realm
      volumes:
       - ./data:/var/lib/registry
       - ./certs:/certs
       - ./passwd:/auth
```

Ensuite<br>
`docker-compose up -d`<br>
`docker login 127.0.0.1:5000`<br>

#### Launch dockers with systemd
Cela permets de : 
    - formaliser les lancements
    - utiliser les orchestrateurs et leurs modules systemd (ansible)
    - améliorer les logs dans syslog

Exemple avec un docker-compose:
1) Dans docker-compose.yml :

```
    version: "3.0"
    services:
      mynginx:
        image: nginx:latest
        container_name: mynginx
        ports:
         - 80:80
```

2) `docker-compose up -d`<br>
3) Creation d'un fichier de service dans */etc/systemd/system/* ici *mynginx.service* :

```
    [Unit]
    Description=My nginx
    Requires=docker.service
    After=docker.service
    
    [Service]
    Restart=always
    User=root
    Group=docker
    ExecStartPre=/usr/bin/docker-compose -f /root/docker-compose.yml down -v
    ExecStart=/usr/bin/docker-compose -f /root/docker-compose.yml up
    ExecSopt=/usr/bin/docker-compose -f /root/docker-compose.yml down -v
    SyslogIdentifier=mynginx
    
    [Install]
    WantedBy=multi-user.target
```

4) `docker rm -f mynginx`<br>
5) `service mynginx start` et on verifie avec `service mynginx status` ainsi que dans les logs syslog <br>

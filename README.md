# REGISTRATOR API
## Commands
### Create models from config
```
./manage.py create_models_via_config $path_to_config.json
```
config example main/data/models.json

---

# Deploy

**Install Postgresql**

```
#!bash

docker run --name postgres --restart=always -p 5432:5432 -v /data/postgres:/var/lib/postgresql/data -e    POSTGRES_PASSWORD=ololo -d mdillon/postgis:9.4
```

**Create database**


```
#!bash

docker exec -it postgres bin/bash
psql -U postgres
CREATE DATABASE registrator;
\connect registrator;
CREATE EXTENSION postgis;
\q

```

**Build and run registrator API.**


*Build image.*

```
#!bash

#clone repository before
docker build -t registrator-api .
```

*Run container.*
```
#!bash

docker run --name registrator-api -d -p 8008:80 -v /data/registrator/media:/env/www/media --link postgres:db -e DATABASE_URL=postgis://postgres:ololo@db/registrator winsent/registrator-api

```

# Generate public RSA key

```
#!bash
ssh-keygen -y -f docker/id_rsa

```
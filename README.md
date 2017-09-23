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

**Build and run registrator API**


*Build image*

```
#!bash

#clone repository before
docker build -t registrator-api .
```

*Run container*
```
#!bash

docker run --name registrator-api -d -p 8008:80 -v /data/registrator/media:/env/www/media --link postgres:db -e DATABASE_URL=postgis://postgres:ololo@db/registrator winsent/registrator-api

```

# Generate public RSA key

```
#!bash
ssh-keygen -y -f docker/id_rsa

```

# Filtering

Show objects with `is_onmap=True` 
```
http://registrator.serv.icdo.org/userlayers/api/v1/tablesdata/61/data/?is_onmap=True
```

Valid filtering values are: [Django ORM filters](https://docs.djangoproject.com/en/dev/ref/models/querysets/#field-lookups) (e.g. startswith, exact, lte, etc.) 
```
/userlayers/api/v1/myresource/?slug=myslug
/userlayers/api/v1/myresource/?slug__startswith=test
```
We can filter using any standard GeoDjango [spatial lookup](https://docs.djangoproject.com/en/dev/ref/contrib/gis/geoquerysets/#spatial-lookups) filter.
```
/userlayers/api/v1/myresource/?polys__contains={"type": "Point", "coordinates": [-122.475233, 37.768617]}
```

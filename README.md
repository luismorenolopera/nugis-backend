# Nugis
<img src="https://image.ibb.co/n8C5De/image_1.png" alt="nugis_logo" width="200"/>

Nugis is a personal app of audio streaming

### Set your ENV
#### Postgres

```sh
$ touch config/postgres/.env
```

in config/postgres/.env

```txt
POSTGRES_USER=postgres_role
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db
```

#### Django

```sh
$ touch config/django/.env
```

in config/django/.env

```txt
DEBUG=ON
SECRET_KEY=wu$!2-h800e^p5gw(1gwe-=iwri8$2_j)903+^c6)k8eo4wl1-
ALLOWED_HOST=167.99.149.8
```

### Docker
using nugis with docker is very simple, you need docker and docker-compose, by default it will run on port 80

```sh
$ git clone https://github.com/luismorenolopera/nugis-backend.git
$ cd nugis-backend
$ docker-compose up --build
$ docker-compose run gunicorn python nugis/manage.py makemigrations
$ docker-compose run gunicorn python nugis/manage.py migrate
$ docker-compose run gunicorn python nugis/manage.py createsuperuser
```

check 'localhost'

### Aditional configurarion
You need to get the path to media_volume and grant read and write permissions

```sh
$ docker volume ls
DRIVER              VOLUME NAME
local               nugis-backend_media_volume
local               nugis-backend_postgres_volume
local               nugis-backend_static_volume
```
use nugis-backend_media_volume

```sh
$ docker inspect volume nugis-backend_media_volume
[
    {
        "CreatedAt": "2018-10-02T09:20:18Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "nugis-backend",
            "com.docker.compose.version": "1.22.0",
            "com.docker.compose.volume": "media_volume"
        },
        "Mountpoint": "/var/lib/docker/volumes/nugis-backend_media_volume/_data",
        "Name": "nugis-backend_media_volume",
        "Options": null,
        "Scope": "local"
    }
]

```

use Mountpoint
```sh
# chmod -R 777 /var/lib/docker/volumes/nugis-backend_media_volume/_data
```

### Authors

- Luis Moreno

License
----

MIT

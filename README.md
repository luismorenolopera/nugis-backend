# Nugis
<img src="https://image.ibb.co/n8C5De/image_1.png" alt="nugis_logo" width="200"/>

Nugis is a personal app of audio streaming

### Set your ENV
#### Postgres

```sh
$ touch config/postgres/.env
$ vim config/postgres/.env
```

in config/postgres/.env

```txt
POSTGRES_USER=postgres_role
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres
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
local               nugisbackend_media_volume
local               nugisbackend_static_volume
```
use nugisbackend_media_volume

```sh
$ docker inspect volume nugisbackend_media_volume
[
    {
        "CreatedAt": "2018-09-29T21:58:46Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "nugisbackend",
            "com.docker.compose.volume": "media_volume"
        },
        "Mountpoint": "/var/lib/docker/volumes/nugisbackend_media_volume/_data",
        "Name": "nugisbackend_media_volume",
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

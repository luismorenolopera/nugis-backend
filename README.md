# Nugis
Nugis is a personal app of audio streaming

### Docker
```sh
$ git clone https://github.com/luismorenolopera/nugis-backend.git
$ cd nugis-backend
$ docker-compose up --build
$ docker-compose run gunicorn python nugis/manage.py makemigrations
$ docker-compose run gunicorn python nugis/manage.py migrate
$ docker-compose run gunicorn python nugis/manage.py createsuperuser
# chmod -r 777 /var/lib/docker/volumes/nugis-backend_media_volume/_data
```

### Authors

- Luis Moreno

License
----

MIT

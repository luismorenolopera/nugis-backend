# Nugis
<img src="https://image.ibb.co/n8C5De/image_1.png" alt="nugis_logo" width="200"/>

Nugis is a personal app of audio streaming

### Set your ENV
#### Postgres

in .envs/.production/.postgres

```txt
POSTGRES_USER=postgres_role
POSTGRES_PASSWORD=postgres_password
POSTGRES_DB=postgres_db
```

#### Django

in .envs/.production/.django

```txt
SECRET_KEY=wu$!2-h800e^p5gw(1gwe-=iwri8$2_j)903+^c6)k8eo4wl1-
ALLOWED_HOST=167.99.149.8
SENTRY_DSN=https://cc0ac12d9ac94e5c223bd0a3eab5361c@sentry.io/2011301
```

### Docker
using nugis with docker is very simple, you need docker and docker-compose, by default it will run on port 80

```sh
$ git clone https://github.com/luismorenolopera/nugis-backend.git
$ cd nugis-backend
$ docker-compose -f production.yml up --build
$ docker-compose -f production.yml run django nugis/manage.py migrate
$ docker-compose -f production.yml run django nugis/manage.py createsuperuser
```

check 'localhost'

note:

for local development change production.yml for local.yml
and localhost for localhost:8000

### Authors

- Luis Moreno

License
----

MIT

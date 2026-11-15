# Nugis
<img src="https://image.ibb.co/n8C5De/image_1.png" alt="nugis_logo" width="200"/>

Nugis is a personal audio streaming app. This repo is the REST API
(Django + Django REST Framework). The web client lives in
[nugis-frontend](https://github.com/luismorenolopera/nugis-frontend).

## Stack

- Python 3.12, Django 5.2 LTS, Django REST Framework
- PostgreSQL 16
- yt-dlp + ffmpeg for importing audio from YouTube
- gunicorn + nginx in production (Docker Compose)

## Environment

Never commit real secrets. Create these files (they are git-ignored for
production):

`.envs/.production/.postgres`

```txt
POSTGRES_USER=nugis
POSTGRES_PASSWORD=<a long random password>
POSTGRES_DB=nugis
```

`.envs/.production/.django`

```txt
SECRET_KEY=<generate one: python -c "import secrets; print(secrets.token_urlsafe(50))">
ALLOWED_HOSTS=api.example.com
CORS_ALLOWED_ORIGINS=https://nugis.example.com
CSRF_TRUSTED_ORIGINS=https://api.example.com
# optional
SENTRY_DSN=
# set to off only if you are NOT behind https
SECURE_COOKIES=on
```

| Variable | Default | Notes |
| --- | --- | --- |
| `DEBUG` | `off` | `on` only for local development |
| `SECRET_KEY` | required when `DEBUG=off` | |
| `ALLOWED_HOSTS` | `*` in debug, empty otherwise | comma separated |
| `CORS_ALLOWED_ORIGINS` | empty (all origins in debug) | the frontend URL(s) |
| `DATABASE_URL` | unset | overrides the `POSTGRES_*` variables |
| `MAX_TRACK_SIZE` | `10485760` | bytes |
| `SENTRY_DSN` | unset | enables Sentry |

## Docker

```sh
git clone https://github.com/luismorenolopera/nugis-backend.git
cd nugis-backend
docker compose -f production.yml up --build -d
docker compose -f production.yml run --rm django python nugis/manage.py migrate
docker compose -f production.yml run --rm django python nugis/manage.py createsuperuser
```

For local development use `local.yml` and open `http://localhost:8000`.

### Upgrading an old (2018) install

The database moved from PostgreSQL 10 to 16, which cannot read the old data
directory. Dump before upgrading and restore after:

```sh
# with the OLD code still checked out
docker compose -f production.yml exec postgres pg_dumpall -U <user> > nugis.sql
docker compose -f production.yml down
docker volume rm nugis-backend_postgres_volume
# update the code, then
docker compose -f production.yml up -d postgres
cat nugis.sql | docker compose -f production.yml exec -T postgres psql -U <user> -d postgres
docker compose -f production.yml up --build -d
docker compose -f production.yml run --rm django python nugis/manage.py migrate
```

## API

Interactive docs: `/` (ReDoc) and `/swagger/`. Authenticate with
`Authorization: Token <token>` from `POST /api-token-auth/`.

| Endpoint | |
| --- | --- |
| `POST /users/user` | sign up |
| `GET/PATCH /users/me` | current user |
| `GET/POST /music/tracks/` | list (`?search=`, `?upload_by=`) / upload mp3 |
| `GET/PATCH/DELETE /music/tracks/<id>/` | only the uploader can change or delete |
| `GET/POST /music/yt_upload` | preview / import a YouTube video |
| `GET/POST /music/playlists/` | your playlists |
| `GET/POST /music/playlists/track` | which of your playlists contain a track |
| `/music/albums/`, `/music/artists/`, `/music/genres/` | catalog (staff can edit) |

## Tests

```sh
pip install -r requirements-dev.txt
cd nugis
DEBUG=on DATABASE_URL=sqlite:////tmp/nugis.db python manage.py test
```

### Authors

- Luis Moreno

License
----

MIT

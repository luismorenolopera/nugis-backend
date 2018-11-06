FROM python:3.6-alpine
MAINTAINER Luis Moreno "l.david1929@gmail.com"

RUN mkdir /app
WORKDIR /app
COPY . /app/

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # youtube_dl dependencies
  && apk add ffmpeg

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

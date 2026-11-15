FROM python:3.12-slim
LABEL maintainer="Luis Moreno"

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ffmpeg is needed by yt-dlp to extract mp3 audio
RUN apt-get update \
  && apt-get install -y --no-install-recommends ffmpeg \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/services/djangoapp/src
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./

# collectstatic only needs a throwaway key at build time
RUN cd nugis \
  && SECRET_KEY=build-only python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", \
     "--chdir", "nugis", \
     "--bind", ":8000", \
     "--workers", "3", \
     "--timeout", "300", \
     "nugis.wsgi:application" \
]

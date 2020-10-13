FROM python:3
RUN apt-get update &&\
 apt-get install -y postgresql-client &&\
 rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED 1
WORKDIR /srv/
ADD requirements.txt /srv/
RUN pip install -r requirements.txt
COPY . /srv/
WORKDIR /srv/movies/
CMD ../bin/wait postgres --\
 python manage.py migrate &&\
 uwsgi --http 0.0.0.0:8000 --wsgi-file movies/wsgi.py --master --processes 32 --threads 8

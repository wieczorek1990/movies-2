# Repositories

## Envs

Create `/envs/` directory using `/envs.example/` as template.

```bash
# django
DJANGO_DEBUG # 0 or 1 for disabled/enabled
DJANGO_SECRET_KEY # 50 characters
OMDB_API_KEY # 8 characters

# postgres
POSTGRES_USERNAME # username
POSTGRES_PASSWORD # password
```

## Running

After creating envs run:

```bash
docker-compose up
```

This starts with failure when database is yet not created.

## Database

Setting up database, e.g. for local instance:

```bash
docker-compose up
docker-compose exec postgres bash
psql -h postgres -U postgres
CREATE DATABASE movies WITH OWNER postgres ENCODING 'utf-8';
```

Now run `docker-compose up` again for backend to start without failure.

## Tests

Running tests:

```bash
docker-compose up
docker-compose exec django bash
./manage.py test
```

## Deployment

Deploy to production:

* create configuration (look into /docker-compose.yml and /Dockerfile)
    * generate envs (look into /envs/)
    * generate OMDb API key: http://www.omdbapi.com/apikey.aspx
    * generate Djago secret with `pwgen -sy 50 1`


## Project decisions

I decided to use PostgreSQL because it's popular and available on Heroku.

On the `/top/` route I decided not to include movies with 0 comments.

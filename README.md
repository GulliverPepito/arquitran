# Alquitrán Web Payments © REST API

> Built with Python 3.5 and Django :snake:

[![Build Status](https://travis-ci.org/mrpatiwi/arquitran.svg?branch=travis)](https://travis-ci.org/mrpatiwi/arquitran)

## Development

Clone this repository:

```sh
git clone ...
```

### Prepare virtualenv:

```sh
pip install -U virtualenv
virtualenv --python=python3.5 arquitranenv
source ./arquitranenv/bin/activate

# To stop using this virtualenv:
deactivate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

### Setup Postgres database:

```sh
psql
```
```sql
CREATE DATABASE arquitran;
CREATE USER arquitranuser WITH PASSWORD 'password';
ALTER USER arquitranuser CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE arquitran TO arquitranuser;
```

Make migrations:

```
python manage.py migrate
```

### Run server

Start the app at [`http://localhost:8000/`](http://localhost:8000/) with:

```sh
python manage.py runserver
```

## Production

> Make sure you have Docker and Docker-compose installed.

Create Docker volume:

```sh
docker volume create --name=alquitran-data
```

Setup environment variables:

```sh
# Keep this secret
export POSTGRES_PASSWORD=SECRET_AND_LONG_HASH
export SECRET_KEY=SECRET_AND_LONG_HASH
```

Run Docker-compose:

```sh
docker-compose up -d
```

Run migrations:

```sh
docker-compose exec django python manage.py migrate
```

Update app with short downtime:

```sh
docker-compose up -d --build
```

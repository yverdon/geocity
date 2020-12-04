# geomapshark - a geocyberadministration tool for cities

Discover geocity features and usage [here](https://project.mapnv.ch/projects/geocity-wiki/wiki/geocity)

## Getting started with the full Docker demo version

### Step by step guide to the working full docker non persistent DEMO

This will bring up a demo instance with preset fixtures served by the
Django developpment server in reload mode.

```bash
git clone git@github.com:yverdon/geocity.git && cd geocity
cp -n env.demo .env
docker-compose -f docker-compose-dev.yml build
docker-compose -f docker-compose-dev.yml down --remove-orphans && docker-compose -f docker-compose-dev.yml up
```

This process will create the .env file only if it does not already exist

The demo application is now running on _localhost:9095_

To debug and view the resulting `docker-compose-dev.yml` file use (uses the `.env` file for variables substitution):

```bash
docker-compose -f docker-compose-dev.yml config
```

## Setup for full Docker persistent instance served by gunicorn webserver

#### Create new PostGIS DB

1. Create a geocity user
2. Create a geocity schema owned by geocity user
3. Edit DB connexion in .env file
4. Create and edit pg_service.conf file in qgisserver directory

### Setup your Environment file

Edit the variables in `.env` according to your environment.    
Set the global environment switcher to `ENV=DEV` in the `.env` file.

Keep in mind that you are in a Docker environment. Thus you might need to set, on Linux environment something like:

```
PGHOST="172.17.0.1"
```

So that the Django container can reach your `postgres` user on the host machine.

## Production containers administrations

```
git clone git@github.com:yverdon/geocity.git && cd geocity
cp -n env.demo .env
docker-compose build
docker-compose down --remove-orphans && docker-compose up
```

#### Open the application to the world

Use your favorite webserver to proxypass localhost:9095 to the outside world

#### Demo accounts

Administrator role (Django superuser):
_admin:admin_

Backoffice role:
_secretariat-yverdon:admin_

Validatation role A:
_validator-yverdon:admin_

Validatation role B:
_eaux-yverdon:admin_

### Generic Docker hints

In case you get and error similar to this: `E: You don't have enough free space in /var/cache/...`,
run the following commands to clear them all:

```
docker system prune -a
```

## QGIS-server for map generation

_Prerequisite_

A dummy feature must drawn otherwise qgis will raise an error.

_Modify print template_

Simply open the print/print.qgs project

_Capabilities of the print server_

```
http://localhost:9096?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
```

## Dependency management

Dependencies are managed with [`pip-tools`](https://github.com/jazzband/pip-tools).

### Installing packages

To install a new package, add it to `requirements.in`, without pinning it to a
specific version unless needed. Then run:

```
docker-compose exec web pip-tools compile requirements.in
docker-compose exec web pip install -r requirements.txt
```

Make sure you commit both the `requirements.in` and the `requirements.txt` files.

### Upgrading packages

To upgrade all the packages to their latest available version, run:

```
docker-compose exec web pip-tools compile -U requirements.in
docker-compose exec web pip install -r requirements.txt
```

To upgrade only a specific package, use `pip-tools compile -P <packagename>`.
The following commands will upgrade Django to its latest version, making sure
it's compatible with other packages listed in the `requirements.in` file:

```
docker-compose exec web pip-tools compile -P django requirements.in
docker-compose exec web pip install -r requirements.txt
```

## Migrations

To run a migration, for example when the model has changed, execute
`manage.py makemigrations` from inside the docker service of the web app.
Then execute `manage.py migrate`.

```
docker-compose exec web python3 manage.py makemigrations <app_label>
docker-compose exec web python3 manage.py migrate <app_label> <migration_name>
```

For more information about django's migrations, help is available at:

```
docker-compose exec web python3 manage.py makemigrations --help
docker-compose exec web python3 manage.py migrate --help
```

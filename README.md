# Geocity - a (geo)cyberadministration tool for public administrations ![Geocity CI](https://github.com/yverdon/geocity/workflows/Geocity%20CI/badge.svg?branch=main)

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

### Run the tests from within the docker container

List running containers:

```bash
$ docker ps -a

CONTAINER ID        IMAGE                         COMMAND                  CREATED             STATUS              PORTS                    NAMES
de8f58bf2e2c        gms_web                       "/code/entrypoint_de…"   16 hours ago        Up 16 hours         0.0.0.0:9095->9000/tcp   geocity_web_1
ab542f438d62        camptocamp/qgis-server:3.10   "/usr/local/bin/star…"   16 hours ago        Up 16 hours         0.0.0.0:9096->80/tcp     geocity_qgisserver_1
ffaa9f6c1b21        camptocamp/postgres:11        "docker-entrypoint.s…"   16 hours ago        Up 16 hours         0.0.0.0:9097->5432/tcp   geocity_postgres_1
```

Enter the container:

```bash
$ docker exec -it de8f58bf2e2c bash
```

Run the tests:

```
root@de8f58bf2e2c:/code# ./run_tests.sh
```

Example to run a single test in container

```bash
coverage run --source='.' ./manage.py test --settings=geomapshark.settings_test permits.tests.test_permit_request.PrivateDemandsTest
stCase
```

## Linting

We use [Black](https://github.com/psf/black) as code formatter. Just use the following command to automatically format your code:

```
$ docker-compose exec web black .
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

## Permissions

The user belonging to backoffice group can be granted specific permissions:
- ```see_private_requests```, "Voir les demandes restreintes": allows the user to make requests that are not visible by standard user. Typically during the setup stage of a new form configuration
- ```amend_permit_request```,"Traiter les demandes de permis": allow the user the process (amend) the requests (fill the backoffice fields), require validation for other departments and print the documents
- ```validate_permit_request```,"Valider les demandes de permis": allow the user to fill the validation form
- ```classify_permit_request```,"Classer les demandes de permis" allow the user to accept/reject the requests if validations services have all accepted it. 
- ```edit_permit_request```, "Éditer les demandes de permis": allow the user to edit de requests filled by another person

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

### QGISSERVER LOGS

Use ```docker-compose logs -f --tail=20 qgisserver``` to see qgisserver logs

## Two factor authentification

You can enable 2FA by setting the variable `ENABLE_2FA` to `true`. Defaults to `false`.

### Access to admin views under 2FA

Super users require to enable 2FA to have access to the admin app.

Follow the following steps:

1. Go to the `/account/login/` and sign in with your super user credentials.
2. Follow the steps to activate 2FA
3. Open `/admin/`

Next time you sign in, you will be asked for a token.
Once you provided your token go to `/admin/` to access the admin app.

## Dependency management

Dependencies are managed with [`pip-tools`](https://github.com/jazzband/pip-tools).

### Installing packages

To install a new package, add it to `requirements.in`, without pinning it to a
specific version unless needed. Then run:

```
docker-compose exec web pip-compile requirements.in
docker-compose exec web pip install -r requirements.txt
```

Make sure you commit both the `requirements.in` and the `requirements.txt` files.

### Upgrading packages

To upgrade all the packages to their latest available version, run:

```
docker-compose exec web pip-compile -U requirements.in
docker-compose exec web pip install -r requirements.txt
```

To upgrade only a specific package, use `pip-compile -P <packagename>`.
The following commands will upgrade Django to its latest version, making sure
it's compatible with other packages listed in the `requirements.in` file:

```
docker-compose exec web pip-compile -P django requirements.in
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

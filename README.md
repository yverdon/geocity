# geomapshark - a geocyberadministration tool for cities

## Getting started with the full Docker demo version

### Step by step guide to the working full docker non persistent demo

This will bring up a demo instance with preset fixtures served by the
Django developpment server in reload mode.

```
mkdir geocity
git init
git remote add upstream https://github.com/yverdon/geocity
git fetch upstream
git checkout upstream/master
chmod a+rwx entrypoint.sh
docker-compose -f docker-compose-dev.yml build
docker-compose down --remove-orphans && docker-compose -f docker-compose-dev.yml up
```

This process will create the .env file only if it does not already exist

The demo application is now running on *localhost:9095*

### Setup for full docker persistent instance served by gunicorn webserver

#### Create new postgis DB

1. Create a geocity user
2. Create a geocity schema owned by geocity user
3. Edit DB connexion in .env file
3. Create and edit pg_service.conf file in qgisserver directory


#### Build and start the composition

```
docker-compose -f docker-compose-prod.yml build
docker-compose down --remove-orphans && docker-compose -f docker-compose-prod.yml up -d
```

#### Open the application to the world

Use your favorite webserver to proxypass localhost:9095 to the outside world



#### demo accounts

Administrator role (django superuser):
    *admin:admin*

Backoffice role:
    *secretariat-yverdon:admin*

Validatation role A:
    *validator-yverdon:admin*

Validatation role B:
    *eaux-yverdon:admin*

### Configuration: Environment variables

Rename `env.demo` to `.env` and modifiy it according to your specific configuration.

### Generic Docker hints

In case you get and error similar to this: E: You don't have enough free space in /var/cache/...,
run the following commands to clear them all:

```
docker system prune -a
```


## QGIS-server for map generation

*Prerequisite*

A dummy feature must drawn otherwise qgis will raise an error.

*Modify print template*

Simply open the print/print.qgs project

*Capabilities of the print server*

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

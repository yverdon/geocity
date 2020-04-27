# geomapshark - a geocyberadministration tool for cities

## Getting started with the full Docker demo version (the less painfull way)

### Step by step guide to the working full docker non persistent demo

This will bring up a demo instance with preset fixtures served by the
Django developpment server in reload mode.

```
mkdir geocity
git init
git remote add upstream https://github.com/yverdon/geocity
git fetch upstream
git checkout upstream/demo-docker
chmod a+rwx entrypoint.sh
docker-compose -f docker-compose-dev.yml build
docker-compose down --remove-orphans && docker-compose -f docker-compose-dev.yml up
```

This process will create the env.yaml file only if no env.yaml file is present

The demo application is now running on localhost:9095

#### demo accounts

Administrator role (django superuser):
    *admin:demo2020*

Backoffice role:
    *demo-backoffice:demo2020*

Validatation role:
    *demo-validator:demo2020*

### Environment variables

Rename `sample.env.yaml` to `env.yaml` and modifiy it according to your specific configuration.

### Generic Docker hints

In case you get and error similar to this: E: You don't have enough free space in /var/cache/...,
run the following commands to clear them all:

```
docker rmi $(docker images -q)
docker rm -v $(docker ps -qa
```

### Generic Django hints

*install requirements*
```
pip install -r requirements.txt
```

*setup database*
```
CREATE USER geomapshark WITH LOGIN SUPERUSER INHERIT CREATEDB CREATEROLE NOREPLICATION;
alter user geomapshark with password 'xxxx';
CREATE SCHEMA geomapshark AUTHORIZATION "geomapshark";
```

*Collect static files*
```
python manage.py collectstatic
```

*Setup protected files *
```
mkdir geomapshark/protected-static/
```

And copy required files (for printing) here. For now: xxx.png

Same in docker:

```
sudo -u sigdev docker-compose run web  python manage.py collectstatic
```

*Generate translation files ignoring venv*
```
python manage.py makemessages -l fr -i venv
```
*Compile translation files for useful locales*
```
python manage.py compilemessages -l fr
```

Same in docker:

```
sudo -u sigdev docker-compose run web  python manage.py compilemessages -l fr
```

## QGIS-server for map generation

*Modify print template*

Simply open the print/print.qgs project

*Test the print server*

```
http://localhost:9050?&SERVICE=WMS&VERSION=1.3.0&REQUEST=GetPrint&FORMAT=pdf&TRANSPARENT=true&SRS=EPSG:2056&DPI=300&TEMPLATE=permis-fouilles&map0:extent=2538470,1180743,2540100,1181848&LAYERS=mapnv
```

*Capabilities of the print server*

```
http://localhost:9050?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
```

## Getting started without Docker (the hard, not recommended way)

Clone the repository.

For windows using pipenv:

`python -m pipenv install`


For windows using pip:

```virtualenv venv
   pip install -r requirements.txt
```

### Special notes on Weasyprint dependencies configuration

You MUST install GTK-3 from here: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

And you MUST add it on TOP of your path. If you don't, it will hurt.

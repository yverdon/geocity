# geomapshark - a powerful geoform tool built with django

## Getting started

Clone the repository.


For windows using pipenv:

`python -m pipenv install`


For windows using pip:

```virtualenv venv
   pip install -r requirements.txt
```

*Install on c2c server*
```
cd ~
mkdir venv
cd ~/venv
python3 -m venv <projectname> --without-pip
source <projectname>/bin/activate
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
deactivate
source <projectname>/bin/activate
pip --version
pip install -r requirements.txt
```

## Documentation

Rename `sample.env.yaml` to `env.yaml` and modifiy it according to your specific configuration.

### Django Update

Apply migration in venv "pip install -U <package-name>"

```
pip install -U django
pip install -U django-filters==2.0.0
pip install -U django-bootstrap4
pip install -U django-bootstrap4-datepicker
pip install -U django-tables2
pip install -U django-fontawesome

```

### Setup database

`psql -U postgres -p PORTNUMBER`

```sql
DROP DATABASE geomapshark;
CREATE DATABASE geomapshark;
\c geomapshark
CREATE EXTENSION postgis;
CREATE SCHEMA geomapshark AUTHORIZATION geomapshark;
\q
```

Create migrations

`python .\manage.py makemigrations`

Apply migrations

`python .\manage.py migrate`

Create a superuser to administrate you application:

`python .\manage.py createsuperuser`

### Populate database

Dump and restore existing data:

```
pg_dump -p PORTNUMBER -h HOSTNAME -U USERNAME -F c --no-privileges -f temp.sql -n geomapshark DATABASE
pg_restore -U postgres -d geomapshark -p PORTNUMBER --no-owner -a temp.sql
rm temp.sql
```

And reset sequences:

```
psql -p PORTNUMBER -U USERNAME -Atq -f reset_sequences.sql -o temp
psql -p PORTNUMBER -h HOSTNAME -U USERNAME -f temp
rm temp
```

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

*Production setup with apache mod_wsgi in a virtual host*
```
https://docs.djangoproject.com/fr/2.0/howto/deployment/wsgi/modwsgi/
```

*Collect static files*
```
python manage.py collectstatic
```

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

*Start QGIS Server for report generation*
```
cd print
docker-compose up -d
```

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

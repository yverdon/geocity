#!/bin/bash

cd /code
# setup app using the django tools
python3 manage.py migrate
# django-constance models
python3 manage.py migrate database

mkdir /code/geomapshark/static/
echo yes | python3 manage.py compilemessages -l fr
echo yes | python3 manage.py collectstatic

# update integrator permissions
python3 manage.py update_integrator_permissions


exec $@

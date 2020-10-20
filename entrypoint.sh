#!/bin/bash

cd /code
# setup app using the django tools
python3 manage.py migrate
mkdir /code/geomapshark/static/
echo yes | python3 manage.py compilemessages -l fr
echo yes | python3 manage.py collectstatic



exec $@

#!/bin/bash

cd /code
python3 manage.py migrate
echo yes | python3 manage.py compilemessages -l fr
echo yes | python3 manage.py collectstatic
gunicorn geomapshark.wsgi -b :9000 --error-logfile gunicorn_log.log

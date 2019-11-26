#!/bin/bash

while :
do
    echo > /dev/tcp/postgres/5432
    if [[ $? -eq 0 ]]; then
        break
    else
      echo waiting for db...
    fi
    sleep 1
done

cd /code
python3 manage.py migrate
echo yes | python3 manage.py compilemessages -l fr
echo yes | python3 manage.py collectstatic
#gunicorn geomapshark.wsgi -b :9000 --error-logfile gunicorn_log.log
exec $@

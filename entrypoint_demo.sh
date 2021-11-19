#!/bin/bash

echo **************applying entrypoint*******************
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
# create demo pg_service.conf file if not exist
cp -n qgisserver/pg_service.conf_demo qgisserver/pg_service.conf

python3 manage.py migrate
# django-constance models
python3 manage.py migrate database
mkdir -p /code/geomapshark/static/
echo yes | python3 manage.py compilemessages -l fr
echo yes | python3 manage.py collectstatic

# python3 manage.py fixturize_demo

exec $@

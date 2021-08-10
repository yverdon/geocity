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
# create demo env file if not exist
cp -n env.demo .env
# create demo pg_service.conf file if not exist
cp -n qgisserver/pg_service.conf_demo qgisserver/pg_service.conf
# setup app using the django tools

if [ "$INITIAL" = "1" ]; then
    mkdir -p /code/geomapshark/static/
    echo yes | python3 manage.py compilemessages -l fr
    python3 manage.py fixturize
fi

exec $@

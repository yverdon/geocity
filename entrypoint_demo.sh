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

# python3 manage.py migrate
# django-constance models
# python3 manage.py migrate database
# mkdir -p /code/geomapshark/static/
# echo yes | python3 manage.py compilemessages -l fr
# echo yes | python3 manage.py collectstatic

# python3 manage.py fixturize_demo

exec $@

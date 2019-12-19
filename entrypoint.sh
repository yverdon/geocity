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
# rename demo env file
cp -n env.yaml_demo env.yaml
# setup app using the django tools
python3 manage.py migrate
echo yes | python3 manage.py compilemessages -l fr
echo yes | python3 manage.py collectstatic

python3 manage.py loaddata db.json


exec $@

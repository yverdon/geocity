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
python3 manage.py migrate
echo yes | python3 manage.py compilemessages -l fr
echo yes | python3 manage.py collectstatic

python3 manage.py shell -c "from django.contrib.auth.models import User; \
                           User.objects.filter(username='admin').exists() or \
                           User.objects.create_superuser('admin',
                           'admin@exampletoto.com', 'admin2020')"


exec $@

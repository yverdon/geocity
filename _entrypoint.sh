#!/bin/bash

echo "**************applying entrypoint*******************"

if [[ $ENV = "DEV" || $ENV = "DEMO" ]]; then
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
fi

cd /code || exit

if [ "$INITIAL" = "1" ]; then
    echo "**************Setting up database*******************"
    if [[ "$ENV" = "DEV" ]]; then
        # create demo .env file if not exist
        cp -n env.demo .env
    fi

    python3 manage.py migrate
    # django-constance models
    python3 manage.py migrate database
    mkdir -p /code/geocity/static/
    echo yes | python3 manage.py compilemessages -l fr

    if [[ "$ENV" = "PROD" || "$ENV" = "DEMO" ]]; then
        echo yes | python3 manage.py collectstatic
    fi

    if [[ "$ENV" = "DEV" ]]; then
        python3 manage.py fixturize
    elif [[ "$ENV" = "DEMO" ]]; then
        python3 manage.py fixturize_demo
    fi
fi

exec "$@"

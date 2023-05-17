#!/bin/bash

set -e

# Ensuire we have connection to the database.
# If not will, the container will fail and restart.
python3 manage.py shell -c "import django; django.db.connection.ensure_connection();"

# On PROD, we run migrations on startup.
if [ "$ENV" == "PROD" ]; then
    scripts/migrate.sh
fi

if [ "$ENV" == "DEV" ]; then
    cp -R /static_root/libs/js/advanced-geometry-edition /code/geocity/apps/core/static/libs/js
fi

# Run the command
exec $@

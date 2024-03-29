#!/bin/bash

set -e

# Ensuire we have connection to the database.
# If not will, the container will fail and restart.
python3 manage.py shell -c "import django; django.db.connection.ensure_connection();"

if [ "$ENV" == "PROD" ]; then
    # On PROD, we run migrations at startup unless explicitly disabled.
    # If disabled, this command must be run manually for the application to function correctly after a model update.
    if [ "${DISABLE_MIGRATION_SCRIPT_ON_PRODUCTION}" != "true" ]; then
        python3 manage.py migrate
    fi
    python3 manage.py collectstatic --no-input
elif [ "$ENV" == "DEV" ]; then
    python3 manage.py migrate
fi

python3 manage.py compilemessages -l fr
python3 manage.py update_integrator_permissions

# Run the command
exec $@

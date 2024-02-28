#!/bin/bash

set -e

# Ensuire we have connection to the database.
# If not will, the container will fail and restart.
python3 manage.py shell -c "import django; django.db.connection.ensure_connection();"

# On PROD, we run migrations at startup unless explicitly disabled.
# If disabled, this command must be run manually for the application to function correctly after a model update.
if [ "$ENV" == "PROD" ] && [ "${DISABLE_MIGRATION_SCRIPT_ON_PRODUCTION}" != "true" ]; then
    python3 manage.py migrate
fi

# On PROD, we always collect statics
if [ "$ENV" == "PROD" ]; then
    python3 manage.py collectstatic --no-input
    python3 manage.py compilemessages -l fr
    python3 manage.py update_integrator_permissions
elif [ "$ENV" == "DEV" ]; then
    python3 manage.py migrate
    python3 manage.py update_integrator_permissions
fi


# Run the command
exec $@

#!/bin/bash

set -e

# Ensuire we have connection to the database.
# If not will, the container will fail and restart.
python3 manage.py shell -c "import django; django.db.connection.ensure_connection();"

# On PROD, we run migrations at startup unless explicitly disabled. If disabled,
# this commands must be run manually
if [ "$ENV" == "PROD" ] && [ "${DISABLE_MIGRATION_SCRIPT_ON_PRODUCTION}" != "false" ]; then
    python3 manage.py migrate
    python3 manage.py update_integrator_permissions
fi

# On PROD we always collect statics
if [ "$ENV" == "PROD" ]; then
    python3 manage.py compilemessages -l fr
    python3 manage.py collectstatic --no-input
fi

# Run the command
exec $@

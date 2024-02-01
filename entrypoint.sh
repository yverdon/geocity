#!/bin/bash

set -e

# Ensuire we have connection to the database.
# If not will, the container will fail and restart.
python3 manage.py shell -c "import django; django.db.connection.ensure_connection();"

# On PROD, we run migrations at startup unless explicitly disabled.
if [ "$ENV" == "PROD" ] && [ "${DISABLE_MIGRATION_SCRIPT_ON_PRODUCTION}" != "true" ]; then
    scripts/migrate.sh
fi

# Run the command
exec $@

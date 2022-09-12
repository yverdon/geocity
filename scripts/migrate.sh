#!/bin/bash

# Migration script (database migrations, collectstatic, etc.). This must be run
# on startup if changes have been made to the models, the static files, etc.

set -e

python3 manage.py migrate
python3 manage.py compilemessages -l fr
python3 manage.py collectstatic --no-input
python3 manage.py update_integrator_permissions

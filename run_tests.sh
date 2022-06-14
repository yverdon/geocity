#!/bin/sh
set -e
# Save env variables
if [ -f .env ]; then
  cp -f .env env.backup
fi
cp -f env.demo .env

# test with 2FA
sed -i -e 's/ENABLE_2FA\=false/ENABLE_2FA\=true/g' .env
coverage run --source='.' ./manage.py test --settings=geomapshark.settings_test
coverage report -m

# test without 2FA
sed -i -e 's/ENABLE_2FA\=true/ENABLE_2FA\=false/g' .env
coverage run --source='.' ./manage.py test --settings=geomapshark.settings_test
coverage report -m

# test formatting (disabled, this is treated in CI with pre-commit)
# black . --check

# Restore env variables
# FIXME: Not restoring on test failure !
if [ -f env.backup ]; then
  cp -f env.backup .env
  rm env.backup
fi

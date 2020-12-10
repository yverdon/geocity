#!/bin/sh

cp -f env.demo .env
# test with 2FA
coverage run --source='.' ./manage.py test --settings=geomapshark.settings_test
coverage report -m

# test without 2FA
sed -i -e 's/ENABLE_2FA\=true/ENABLE_2FA\=false/g' .env
coverage run --source='.' ./manage.py test --settings=geomapshark.settings_test
coverage report -m

# put it back to true
sed -i -e 's/ENABLE_2FA\=false/ENABLE_2FA\=true/g' .env\

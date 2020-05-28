#!/bin/sh

DJANGO_SETTINGS_MODULE=geomapshark.settings_test ./manage.py test $@

#!/bin/bash
################################################################################
#                      DO NOT USE IN PRODUCTION!                               #
################################################################################
# This script is meant to reset the development stack from scratch.
# It re-initialize the database, run the migrations and the fixures
# and display the docker logs.
# Use with caution.

docker compose down -v --remove-orphans
docker system prune -y
docker compose build --progress plain
docker compose up -d
docker compose exec web python3 manage.py makemigrations
docker compose exec web python3 manage.py migrate
docker compose exec web python3 manage.py fixturize

docker compose logs --tail 200 -tf

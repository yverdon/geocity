#!/bin/bash
################################################################################
#                      DO NOT USE IN PRODUCTION!                               #
################################################################################
# This script is meant to reset the development stack from scratch.
# It re-initialize the database, run the migrations and the fixures
# and display the docker logs.
# Use with caution.

printf "Shutting down docker containers...\n"
docker compose down --volumes --remove-orphans

printf "Pruning down docker objects...\n"
docker system prune --force

printf "Building project...\n"
docker compose build --progress plain

printf "Spinning up project...\n"
docker compose up --detach

printf "Making migrations...\n"
docker compose exec web python3 manage.py makemigrations

printf "Applying migrations...\n"
docker compose exec web python3 manage.py migrate

printf "Applying fixtures...\n"
#docker compose exec web python3 manage.py fixturize

printf "Logging...\n"
docker compose logs --follow

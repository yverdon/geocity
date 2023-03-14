#!/bin/bash

echo "Restarting the application..."

docker compose down --remove-orphans \
&& docker compose build --progress plain \
&& docker compose up -d \
&& docker compose logs --tail 64 -tf web


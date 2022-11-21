#!/bin/bash

echo "Restarting the application..."

docker compose down --remove-orphans \
&& docker compose up --build -d \
&& docker compose logs --tail 64 -tf web


#!/bin/bash

echo "Resetting the application..."

docker compose down --volumes --remove-orphans \
&& docker compose up --build -d \
&& docker compose logs --tail 64 -tf web


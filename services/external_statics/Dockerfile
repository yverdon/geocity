FROM node:slim

RUN apt-get update -y && apt-get -y install git

WORKDIR /app
RUN echo "cloning advanced map plugin..."
RUN git clone https://github.com/MediaComem/geocity-wc-map.git

WORKDIR /app/geocity-wc-map

RUN npm ci
RUN npm build

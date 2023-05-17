FROM node:slim

WORKDIR /app

RUN apt-get -yq update \
  && apt-get -yq upgrade \
  && DEBIAN_FRONTEND=noninteractive apt-get -yq install \
  --fix-missing \
  --no-install-recommends \
  ca-certificates \
  git

RUN echo "cloning advanced map plugin..." \
  && git clone https://github.com/yverdon/geocity-wc-map.git

RUN cd /app/geocity-wc-map \
  && npm ci \
  && npm run build

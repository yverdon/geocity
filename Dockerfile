FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.3

RUN apt-get -y update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing \
  --no-install-recommends \
  build-essential \
  gettext \
  python3-pip \
  libcairo2-dev \
  poppler-utils \
  python3-dev \
  python3-setuptools \
  python3-wheel \
  python3-cffi \
  libcairo2 \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 \
  libffi-dev \
  shared-mime-info \
  tzdata \
  && ln -fs /usr/share/zoneinfo/Europe/Zurich /etc/localtime \
  && dpkg-reconfigure -f noninteractive tzdata

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV PYTHONUNBUFFERED 1

ARG ENV

# Copy files in another location to solved windows rights issues
# These files are only used during build process and by entrypoint.sh for dev

WORKDIR /code
COPY requirements_dev.txt requirements_dev.txt
COPY requirements.txt requirements.txt

RUN if [ "$ENV" = "DEV" ] ; \
    then \
    echo "Installing development dependencies..." \
    && pip3 install -r requirements_dev.txt \
    && echo "########################################" \
    && echo "# Installed development dependencies   #" \
    && echo "########################################"; \
    else \
    pip3 install -r requirements.txt \
    && echo "########################################" \
    && echo "# Installed production dependencies    #" \
    && echo "########################################"; \
    fi

COPY . /code/

FROM osgeo/gdal:ubuntu-small-3.1.0

RUN apt-get update
RUN apt-get install gettext python3-pip -y && \
    apt-get install libcairo2-dev -y && \
    apt-get install build-essential python3-dev python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info -y


# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/app_data && \
    mkdir -p /code/tempfiles

VOLUME /code/app_data
VOLUME /code/tempfiles

# Copy files in another location to solved windows rights issues
# These files are only used during build process and by entrypoint.sh for dev

#For production
COPY . /code/

WORKDIR /code

# Required to fix rights when used on windows
RUN chmod 777 entrypoint.sh \
    && ln -s entrypoint.sh /

RUN pip3 install -r requirements.txt

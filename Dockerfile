FROM python:3.8-buster

# Update base container install
# Existing binutils causes a dependency conflict, correct version will be installed when GDAL gets intalled
RUN echo deb http://ftp.uk.debian.org/debian unstable main contrib non-free >> /etc/apt/sources.list && \
    apt-get update && apt-get upgrade -y && \
    apt-get remove -y binutils && \
    apt-get -t unstable install -y libgdal-dev g++ && \
    apt-get install -y gettext && \
    apt-get clean

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/app_data && \
    mkdir -p /code/tempfiles

VOLUME /code/app_data
VOLUME /code/tempfiles
VOLUME /postgresdata

WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install GDAL


# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ADD . /code/

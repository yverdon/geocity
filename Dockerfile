FROM python:3.6-stretch

# Update base container install
RUN apt-get update
RUN apt-get upgrade -y

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

# Add unstable repo to allow us to access latest GDAL builds
RUN echo deb http://ftp.uk.debian.org/debian unstable main contrib non-free >> /etc/apt/sources.list
RUN apt-get update

# Existing binutils causes a dependency conflict, correct version will be installed when GDAL gets intalled
RUN apt-get remove -y binutils

# Install GDAL dependencies
RUN apt-get -t unstable install -y libgdal-dev g++

# Install gettext
RUN apt-get install -y gettext

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal


RUN pip install -r requirements.txt
ADD . /code/

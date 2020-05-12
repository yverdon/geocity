FROM osgeo/gdal:ubuntu-small-latest

RUN apt-get install python3-pip -y

# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code/app_data && \
    mkdir -p /code/tempfiles

VOLUME /code/app_data
VOLUME /code/tempfiles

WORKDIR /code

COPY . /code/
RUN pip3 install -r requirements.txt



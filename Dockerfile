FROM osgeo/gdal:ubuntu-small-3.1.0

ARG dev_dependencies

RUN apt-get update
RUN apt-get install gettext python3-pip -y \
    && apt-get install libcairo2-dev -y \
    && apt-get install build-essential python3-dev python3-setuptools \
    python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi-dev shared-mime-info -y


# Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV PYTHONUNBUFFERED 1

# Copy files in another location to solved windows rights issues
# These files are only used during build process and by entrypoint.sh for dev

COPY . /code/
WORKDIR /code

RUN if [ "$dev_dependencies" = "true" ] ; \
    then \
    DEBUG=True \
    && echo "Installing development dependencies..." \
    && pip3 install -r requirements_dev.txt \
    && echo "########################################" \
    && echo "# Installed development dependencies   #" \
    && echo "########################################"; \
    else \
    DEBUG=False \
    && pip3 install -r requirements.txt \
    && echo "########################################" \
    && echo "# Installed production dependencies    #" \
    && echo "########################################"; \
    fi

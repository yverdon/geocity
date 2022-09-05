FROM sitdocker/geocity-base:v1.3.2.2021

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

FROM sitdocker/geocity-base:3.3.0

ARG dev_dependencies

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

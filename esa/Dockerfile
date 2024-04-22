# Scalene produces SIGSEGV on the alpine-normal-3.8.2 image, so we use the
# ubuntu-small-3.8.2 image instead, which actually produces a smaller image.
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.5

# Update package lists and install necessary packages
# g++ is required for installing a recent version of scalene from source since
# the latest binary available is only 1.1.x.
RUN apt update \
    && apt install -y g++ python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Add application
RUN pip install --no-cache-dir "sardem~=0.11" "scalene~=1.5.38" "numpy~=1.26"

COPY ./esa/build/entrypoint.sh /opt
COPY ./get_dem.py /opt/get-dem/get_dem.py

RUN chmod +x /opt/entrypoint.sh && chmod -R +x /opt/get-dem


# Set the entry point or command if needed
ENTRYPOINT ["/opt/entrypoint.sh"]

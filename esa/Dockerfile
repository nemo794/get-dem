FROM ghcr.io/osgeo/gdal:alpine-normal-3.8.2

# Update package lists and install necessary packages
RUN apk add py3-pip


# Add application
RUN pip install sardem

COPY ./esa/build/entrypoint.sh /opt
RUN chmod +x /opt/entrypoint.sh

RUN mkdir -p /opt/get-dem
COPY ./get_dem.py /opt/get-dem/get_dem.py
RUN chmod -R +x /opt/get-dem


# Set the entry point or command if needed
ENTRYPOINT ["/opt/entrypoint.sh"]

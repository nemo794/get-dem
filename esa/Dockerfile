# Scalene produces SIGSEGV on the alpine-normal-3.x image, so we use the
# ubuntu-small-3.x image instead, which actually produces a smaller image.
FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.5

SHELL ["/bin/bash", "-c"]

# Update package lists and install necessary packages
# g++ is required for installing a recent version of scalene from source since
# the latest binary available is only 1.1.x.
RUN apt-get update \
    && apt-get install -y --no-install-recommends g++ python3-pip wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget -qO Miniforge3.sh "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" \
    && bash Miniforge3.sh -b -p "/root/conda" \
    && rm Miniforge3.sh \
    && source "${HOME}/conda/etc/profile.d/conda.sh" \
    && conda update conda -y \
    && :

COPY environment.yml /opt/get-dem/

RUN : \
    && source "${HOME}/conda/etc/profile.d/conda.sh" \
    && conda env update -n base -f /opt/get-dem/environment.yml \
    && :

COPY ./esa/build/entrypoint.sh /opt
COPY ./*.py /opt/get-dem/

RUN chmod +x /opt/entrypoint.sh && chmod -R +x /opt/get-dem

# Set the entry point or command if needed
ENTRYPOINT ["/opt/entrypoint.sh"]

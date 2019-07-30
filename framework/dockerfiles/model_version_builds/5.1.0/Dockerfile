FROM aaraney/wrf-hydro_base
MAINTAINER aaraney@crimson.ua.edu

# Version 5.1.0 of Wrf-Hydro
# Alias version 2.0 of NWM

USER root

ENV NWM=/model

RUN mkdir ${NWM} \
    && cd ${NWM} \
    && apk update --no-cache \
    && apk add --no-cache \
    subversion make \
    g++ gfortran \
    m4 bash \
    && svn export https://github.com/aubreyd/wrf_hydro_nwm_public/branches/v5.1.0/trunk/NDHMS \
    && mv NDHMS/* . \
    && sed -i 's/SPATIAL_SOIL=0/SPATIAL_SOIL=1/' template/setEnvar.sh \
    && bash \
    && ./configure 2 \
    && ./compile_offline_NoahMP.sh template/setEnvar.sh \
    && exit \
    && apk del -r \
    subversion make \
    g++ gfortran \
    m4 bash

WORKDIR ${NWM}

ENTRYPOINT ["sh"]
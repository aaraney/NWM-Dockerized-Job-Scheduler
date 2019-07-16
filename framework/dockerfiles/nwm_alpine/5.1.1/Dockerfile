FROM nwm_base
MAINTAINER aaraney@crimson.ua.edu

USER root

ENV NWM=/nwm

ARG NWM=/nwm

RUN apk add \
    sudo subversion

RUN mkdir /nwm
WORKDIR /nwm

RUN cd ${NWM} && \
    svn checkout https://github.com/aubreyd/wrf_hydro_nwm_public/branches/v5.1.1/trunk/NDHMS \
    && mv NDHMS/* . \
    && sed -i 's/SPATIAL_SOIL=0/SPATIAL_SOIL=1/' template/setEnvar.sh \
    && ./configure 2 \
    && ./compile_offline_NoahMP.sh template/setEnvar.sh

ENTRYPOINT ["bash"]
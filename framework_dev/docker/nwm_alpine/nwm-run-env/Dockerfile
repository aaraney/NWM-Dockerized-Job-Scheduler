# FROM should be changed to the version
# of the nwm that you want to run
# see aaraney docker hub
FROM aaraney/nwm:2.0
MAINTAINER aaraney@crimson.ua.edu

USER root

RUN mkdir /master /slave
WORKDIR /slave

COPY nwm_container_run.sh /usr/local/bin

ENTRYPOINT ["nwm_container_run.sh"]
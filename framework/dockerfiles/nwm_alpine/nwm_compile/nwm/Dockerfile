FROM nwm:2.0
MAINTAINER aaraney@crimson.ua.edu

USER root

ARG USER=water-boy

#WORKDIR /home/${USER}
WORKDIR /home/

#RUN adduser -G wheel -D -S -s /bin/bash ${USER}
#USER ${USER}

#ARG DOMAIN=https://github.com/aaraney/PBenJ/branches/framework-dev/framework_dev/SIPSEY_WILDERNESS_DOMAIN/
# ARG DOMAIN_DIRNAME=$(realpath $(basename ${DOMAIN}))

#RUN svn checkout ${DOMAIN}
#    && cp /nwm /home/${USER}/

# Personal setup
#RUN echo "set -o vi" >> /home/${USER}/.bash_profile \
#    && echo "set completion-ignore-case On" >> /home/${USER}/.inputrc \
#    && echo "alias nwm=$(cd ${NWM})" >> /home/${USER}/.bash_profile

ENTRYPOINT ["bash"]
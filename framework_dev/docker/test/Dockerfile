FROM alpine:3.10
USER root
RUN apk add --no-cache bash
#RUN adduser -G wheel -s /bin/bash -D araney
#RUN mkdir /home/docker/

# make a user
#RUN useradd -ms /bin/bash docker
#RUN usermod -aG sudo docker
#RUN chmod -R 777 /home/docker/
#
#USER araney
#WORKDIR /home/araney
ENTRYPOINT ["bash"]

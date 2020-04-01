# NWM/WRF-Hydro Dockerfiles

### Note: 
- WRF-Hydro version numbers are used instead of the NWM version numbering scheme for the dockerfiles
located in this repo, however on [docker hub](hub.docker.com/u/aaraney) both the NWM and WRF-Hydro
version numbers are used as tags. For example, version 5.0.3 of WRF-Hydro is equivalent to NWM v1.2
and is tagged as both on [docker hub](hub.docker.com/u/aaraney).
- Each version of the model is compiled with the **spatial soils** environment variable turned **on**.

### Dockerfile layering scheme
To cut down on the number of completely unique dockerfiles, each model version
build file is based on a base image, `aaraney/wrf-hydro_base`. `aaraney/wrf-hydro_base` is based on an alpine
linux version 3.10 image. This dockerfile is where all dependencies necessary to compile any version of the NWM or
WRF-Hydro. As mentioned, each docker image version of the model is based (FROM) on this base image.
A third layer of images with tag, `aaraney/nwm-djs` are simply versions of the NWM/WRF-Hydro that have been setup to
be used with the Dockerized Job Scheduler (DJS). They use a shell script `run.sh` as an entry point
instead of a shell.

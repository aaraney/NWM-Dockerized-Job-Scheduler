# Framework Test Case

The test case domain, Pocono PA, was borrowed and adapted from
an NCAR WRF-Hydro training that can be found [here](https://github.com/NCAR/wrf_hydro_docker/tree/master/training/Pocono). 

## Requirements
- Docker
- Python 3
- Docker Python SDK

## How to Run
1. Open Docker Preferences, select advanced. Consider increasing the
   number of allotted CPUs that the docker daemon has access to. In our
experience the NWM is not RAM intensive, so this option needs not be
changed.
1. `docker pull aaraney/nwm-run-env:2.0`
1. `git clone https://github.com/aaraney/NWM-Docker-Ensemble-Framework.git nwm-run-env-pocono`
1. `cd nwm-run-env-pocono/framework_dev/JobScheduler`
1. `time python3 scheduler.py`

### Options
Currently a CLI has not been implemented to wrap runtime
options. However, to adjust the overall number of containers running
at any given time, adjust the parameter `self._MAX_JOBS` found in
`scheduler.py.` It should also be noted, the docker image
tag is currently hard coded in the variable `self._image_tag` also
found in `scheduler.py`. Additionally, within the docker container the
mpi hostfile number of processes has been set to 2. This along with
the previously mentioned issues will be addressed in future releases.

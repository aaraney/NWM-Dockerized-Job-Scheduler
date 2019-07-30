# Dockerized Job Scheduler (DJS) Test Case

The test case domain, Pocono PA, was borrowed and adapted from
an NCAR WRF-Hydro training that can be found [here](https://github.com/NCAR/wrf_hydro_docker/tree/master/training/Pocono). 

This test case show cases the two current ways to run the DJS, using a yaml file
or using file name lists within a python script. Respectively they are, yml_run.py
and list_run.py.

## Requirements
- Docker
- Python 3
- Docker Python SDK

## How to Run
1. Open Docker Preferences, select advanced. Consider increasing the
   number of allotted CPUs that the docker daemon has access to. In our
experience the NWM is not RAM intensive, so this option needs not be
changed.
1. `docker pull aaraney/nwm-djs:2.0`
1. `git clone https://github.com/aaraney/NWM-Docker-Ensemble-Framework.git NWM-Docker-Ensemble-Framework`
1. `cd NWM-Docker-Ensemble-Framework/pocono_test_case`
1. Two options to run DJS
    - 'time python3 yml_run.py'
    - 'time python3 list_run.py'

### Options
Currently a CLI has not been implemented to wrap runtime
options. However, class methods have been used to easily
interface with DJS. Also, it would be fairly trivial to
implement other class methods for example, from a csv file.
If these methods are of interest to you, please either create
pull request after adding in the feature or contact me at
[aaraney@crimson.ua.edu](mailto:aaraney@crimson.ua.edu).

#### fromYaml Test Case
Yaml is a format based on the JSON format that is much easier to read
and format. There are 2 required key value parameters to use the
`fromYaml` class method, `primary` and `alternative-files`. 
* `primary`'s value is a string path to the primary domain directory that holds all of
the model setup files (e.g, geo_em.d01.nc, Fulldom_hires.nc, etc.).
* `alternative-files` is a list of file names that can be specified as either
absolute or relative paths.

There are 4 other optional key values for the `fromYaml` implementation,
`cpus`, `max-jobs`, `mpi-np`, and `image`.

* `cpus` is a string denoting the cpu threads that the containers have access to (i.e., '0-4').
See the docker python api documentation regarding containers and the `run` method. Specifically
the `cpuset_cpus` option from more detail. 
* `max-jobs` is an integer value that sets the maximum number of containers (jobs) to be running
at a given time.
* `mpi-np` is an integer value that sets the number of mpi processes each container will run.
* `image` is a string that will determine what docker image is used to run the containers. 

#### fromList Test Case
An alternative way of interfacing with DJS is through using the class method
fromList. This method requires two parameters, `primary_directory` and `altered_domain_files`.

* `primary_directory` is a path to the primary directory. Currently, it is advised to use the
absolute path to that directory instead of the relative path. 

* `alterned_domain_files` is a list of paths to perturbed (non-default) domain parameter files. 

Altering which docker image to use, the number of cpus, and the number of max jobs should be set
by the user within the script used for calling DJS. These attributes can be set via their properties:
image_tag, max_jobs, max_cpus, mpi_np.

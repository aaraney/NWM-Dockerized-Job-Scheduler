# DJS Documentation

## Prelude
The Dockerized Job Scheduler (DJS) is capable of automating, managing, and
executing numerous NWM simulations simultaneously. All code and tools used
in the creation of this framework are open-source, capable of running agnostic 
to a given operating system.
This framework was designed with the intent of removing the overhead
of model setup and compilation, thereby lowering the barrier for entry
without limiting performance. In doing so, facilitating an environment
for scientists to more easily test hypotheses.

## Overview
In short, DJS replicates a primary directory and places an alternative domain file in the replicated domain and spins-up
a docker container that contains the national water model (NWM) configuration of WRF-Hydro (It also works for non-NWM
configurations of WRF-Hydro). DJS is designed to preform the aforementioned task numerous times in succession so
that multiple NWM simulations can easily be run concurrently.

Interfacing with DJS is made easier through the use of python class methods.
In short, a class method allows for creation of a class instance without explicitly
calling the classes `__init__` method. Examples of this style of implementation are:
```python
df_csv = pandas.read_csv(foo.csv)
df_html = pandas.read_html("https://www.google.com")
```
For information on python class method decorators, check out [this](https://stackabuse.com/pythons-classmethod-and-staticmethod-explained/) resource.

DJS currently supports two class methods, `fromYaml` and `fromList`. `fromYaml` requires the user
supply a yaml file to easily run the framework, options and examples of usage of this method can be found [here](#using-fromyaml).
This way of interfacing with DJS is suggested, as it is fully featured and limits the amount of code
to get the framework operational. However, the method `fromList` allows for a user to specify the locations
of necessary files using the built-in list python data-structure. `fromList` also requires a user
to write more code and be more familiar with the class attributes of the `Scheduler` class. Options and
example usage of the method can be found [here](#using-fromlist).

## Using DJS
#### Quicklinks:
- [Primary Directory Requirements](#primary-directory-requirements)
- [`fromYaml`](#using-fromyaml)
- [`fromList`](#using-fromlist)

### Primary Directory Requirements
Before delving into using DJS, it's imperative to understand what needs
to be included in the primary directory that will be replicated (using hard links)
for each consecutive model simulation. Inside the primary directory it is best
practice to retain the following file system structure and only include the following files 
and directories:
```bash
# Note that "./" indicates the path starts 
# from your current working directory
./primary/
    namelist.hrldas
    hydro.namelist
    DOMAIN/
        Fulldom_hires.nc
        GEOGRID_LDASOUT_Spatial_Metadata.nc
        geo_em.d01.nc
        GWBUCKPARM.nc
        hydro2dtbl.nc
        LAKEPARM.nc
        nudgingParams.nc
        Route_Link.nc
        soil_properties.nc
        spatialweights.nc
        wrfinput_d01.nc
    RESTART/
        # If you are starting the model warm
        HYDRO_RST.YYYY-MM-DD_HH-MM_DOMAIN1
        RESTART.YYYYMMDDHH_DOMAIN1
    FORCING/
        # E.g., if you are using NLDAS hourly forcings
        YYYYMMDDHH.LDASIN_DOMAIN1
```

The path the the directory, `primary` is the location a user will input. Not the
location of `DOMAIN`.

Domain files can be easily obtained from the [CUAHSI subsetter for NWM 1.2](http://subset.cuahsi.org).

Please see the WRF-Hydro [technical docs](https://ral.ucar.edu/projects/wrf_hydro/technical-description-user-guide) for 
detail regarding setting up the namelist files, as well as, acquiring forcing data.

### Using fromYaml
Yaml is a format based on the JSON format that is much easier to read
and format. There are 2 required key value parameters to use the
`fromYaml` class method, `primary` and `alternative-files`. 
- `primary`'s value is a string path to the primary directory that holds the fortran namelist's, `namelist.hrldas` and
 `hydro.namelist` along with the sub-folders, DOMAIN, FORCING, and RESTART that contain model setup files, input forcings, and preexisting
 conditions.
- `alternative-files` is a list of file names that can be specified as either
absolute or relative paths to DOMAIN files (i.e, Fulldom_hires.nc, Route_link.nc, etc.).

Below are example yaml files and a python script for using them with DJS:
```yaml
primary: '/home/username/primary'
alternative-files:
  - '/home/username/Route_Link.nc'
  - '/home/username/Route_Link_1.nc'
  - '/home/username/Route_Link_2.nc'
  - '/home/username/Route_Link_3.nc'
  - '/home/username/Route_Link_4.nc'
```

```yaml
primary: 'primary'
alternative-files:
  - 'Route_Link.nc'
  - 'Route_Link_1.nc'
  - 'Route_Link_2.nc'
  - 'Route_Link_3.nc'
  - 'Route_Link_4.nc'
cpus: '0-7'
max-jobs: 3
mpi-np: 2
image: 'aaraney/nwm-djs:2.0'
```

```python
#!/usr/bin/python3
import sys
sys.path.append('../framework/JobScheduler')
from scheduler import *

schedule = Scheduler.fromYaml('setup.yml')
schedule.startJobs()
```

#### Yaml Key Value Options
There are 4 additional optional key values for the `fromYaml` class method,
`cpus`, `max-jobs`, `mpi-np`, and `image`.
- `cpus` is a _string_ denoting the cpu threads that the containers have access to (i.e., '0-4').
See the docker python api documentation regarding containers and the `run` method. Specifically
the `cpuset_cpus` option from more detail. 
- `max-jobs` is an _integer_ value that sets the maximum number of containers (jobs) to be running
at a given time.
- `mpi-np` is an _integer_ value that sets the number of mpi processes each container will run.
- `image` is a _string_ that will determine what docker image is used to run the containers.

### Using fromList
An alternative way of interfacing with DJS is through using the class method
`fromList`. This method requires two parameters, `primary_directory` and `altered_domain_files`.

- `primary_directory` is a path to the primary directory. Currently, it is advised to use the
absolute path to that directory instead of the relative path. 
- `alterned_domain_files` is a list of paths to perturbed (non-default) domain parameter files. 

Altering which docker image to use, the number of cpus, and the number of max jobs should be set
by the user within the script used for calling DJS. 

Below is an example python script to interface with this class method:
```python
#!/usr/bin/python3
from os.path import realpath
import sys
sys.path.append('../framework/JobScheduler')
from scheduler import *

primary_path = realpath('primary')
altered_domain_files = [
    "Route_Link.nc",
    "Route_Link_1.nc",
    "Route_Link_2.nc",
    "Route_Link_3.nc",
    "Route_Link_4.nc"
]
# Map full file system path name to altered domain files
altered_domain_files = map(lambda f: realpath(f), altered_domain_files)
schedule = Scheduler.fromList(primary_path, altered_domain_files)
schedule.max_jobs = 2
schedule.mpi_np = 2
schedule.max_cpus = '0-2'
schedule.startJobs()
```

### DJS Settable Attributes
These attributes can be set via their properties: image_tag, max_jobs, max_cpus, mpi_np.

- `image_tag` is a _string_ that will determine what docker image is used to run the containers.
- `max_cpus` is a _string_ denoting the cpu threads that the containers have access to (i.e., '0-4').
See the docker python api documentation regarding containers and the `run` method. Specifically
the `cpuset_cpus` option from more detail. 
- `max_jobs` is an _integer_ value that sets the maximum number of containers (jobs) to be running
at a given time.
- `mpi_np` is an _integer_ value that sets the number of mpi processes each container will run.

See the [Using fromList](#using-fromlist) example to see these attributes implemented.

### Additional Information
Currently a CLI has not been implemented to wrap runtime
options. However, class methods have been used to easily
interface with DJS. Also, it would be fairly trivial to
implement other class methods for example, from a csv file.
If these methods are of interest to you, please either create
pull request after adding in the feature or contact me at
[aaraney@crimson.ua.edu](mailto:aaraney@crimson.ua.edu).

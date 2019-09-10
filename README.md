# A Reproducible Framework to Generate Parameter based NWM Ensemble

We developed a generalized framework to efficiently generate performance based NWM ensemble outputs. The framework uses a pseudo random Latin hypercube approach to scale channel parameters, utilizes Docker to deploy and manage asynchronous NWM containers, and creates a weighted average ensemble output based on a rank system. These three tasks have been coded with modularity in mind, these three units have been named, the perturbation engine, the dockerized job scheduler (DJS), and the ensemble generator.

## Pocono Test Case
Easily use our framework using [this](https://github.com/aaraney/NWM-Docker-Ensemble-Framework/tree/master/pocono_test_case/) test case.

## Updates:
### 7/30/19
#### Test Case
- Thorough documentation was added to readme to explain the two test cases.
- To showcase the new class method, fromYaml in DJS a test case was added to accomplish showing the features added. 
- The prior test case was moved to a new script implementation, `list_run.py` where the properties for adjusting containers are showcased.

#### DJS:
- A new class method `fromYaml` was implemented in the Scheduler. This allows for a user to interface with DJS in a new way. Find the details of these changes [here](./pocono_test_case/README.md#fromyaml-test-case). 
- DJS docker containers can now more easily be controlled with the class properties: image_tag, max_jobs, max_cpus, and mpi_np

#### Docker
- Docker images saw a major change in this commit. Prior images for NWM were 473 mb but have now been reduced to 274 mb. Containers internal structure was also updated to be more general and match naming conventions found across the whole platform. Previous the model was compiled in a directory `/nwm` in this commit this was changed to `/model`. Other naming conventions within the images were also changed, `/slave` is now `/replica`. 
 
### 7/9/19
- Three six month runs of NWM 1.2 over Sipsey Wilderness, AL Domain with three differing channel width
scalars. Please find the hydroshare resource [here](https://www.hydroshare.org/resource/bde5162056a84381a8bc56c20d86f4d7/).

### 6/28/19
- Added completed year run of NWM v2 in the Sipsey Wilderness to
  hydroshare. See it [here](https://www.hydroshare.org/resource/0e015316da5b429fb6652d403e6decbe/)

Contributors: [Austin Raney](mailto:aaraney@crimson.ua.edu), [Iman Maghami](mailto:im3vp@virginia.edu), [Yenchia Feng](mailto:yenchia@stanford.edu)

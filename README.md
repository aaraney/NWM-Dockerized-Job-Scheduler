# A Reproducible Framework to Generate Parameter based NWM Ensemble

We developed a generalized framework to efficiently generate performance based NWM ensemble outputs. The framework uses a pseudo random Latin hypercube approach to scale channel parameters, utilizes Docker to deploy and manage asynchronous NWM containers, and creates a weighted average ensemble output based on a rank system.

## Pocono Test Case
Easily use our framework using [this](https://github.com/aaraney/NWM-Docker-Ensemble-Framework/tree/master/pocono_test_case) test case.

## Updates:
### 7/9/19
- Three six month runs of NWM 1.2 over Sipsey Wilderness, AL Domain with three differing channel width
scalars. Please find the hydroshare resource [here](https://www.hydroshare.org/resource/bde5162056a84381a8bc56c20d86f4d7/).

### 6/28/19
- Added completed year run of NWM v2 in the Sipsey Wilderness to
  hydroshare. See it [here](https://www.hydroshare.org/resource/0e015316da5b429fb6652d403e6decbe/)

Contributors: Austin Raney, Iman Maghami, Yenchia Feng

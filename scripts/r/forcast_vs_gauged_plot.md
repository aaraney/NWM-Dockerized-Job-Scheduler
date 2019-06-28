# Forcast vs Gauged Plot Creator

This script takes in a frxst_pts_out.txt and Route_Link.nc file
from, respectively, a run of the National Water Model/WRF-Hydro
and required domain file. Currently this is hard coded into the
script just after the library calls. 

The script looks for gauging stations listed within the Route_Link.nc
file and the run time duration from the frxst_pts_out.txt and
generates a forecast vs gauged plot by pulling gauging data from online
resources.


### Author: Austin Raney
### Date: June 28, 2019
